from pathlib import Path
import hashlib, json, re, subprocess

import argparse
parser = argparse.ArgumentParser(description='Check the frozen KE-04 source revision in a read-only checkout.')
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--output', type=Path, default=Path('/tmp/ke04-source-boundaries.json'))
args = parser.parse_args()
ROOT = args.repo
P = ROOT / 'eigenvalues-and-inverse-problems/KE-04/lean'
BASE = '50838e37dd793830e2cecd1055cfc7e0349490f1'
HEAD = 'ecd7d63a22e40db0967a9cb8e785555a0fad6ca8'
assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip() == HEAD
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(s):
    # All actual project comments inspected; support nested Lean block comments.
    out=[]; i=0; depth=0
    while i < len(s):
        if s[i:i+2] == '/-': depth += 1; i += 2
        elif depth and s[i:i+2] == '-/': depth -= 1; i += 2
        elif depth: i += 1
        elif s[i:i+2] == '--':
            j=s.find('\n',i); i=len(s) if j<0 else j
        else: out.append(s[i]); i+=1
    assert not depth
    return ''.join(out)
def signatures(s):
    return {m[1]: re.sub(r'\s+', ' ',m[2]).strip() for m in re.finditer(r'\btheorem\s+(\w+)\s+(.+?)\s*:=',clean(s),re.S)}
challenge = signatures((P/'Challenge.lean').read_text())
proof = signatures((P/'NLA/KE04/Proof.lean').read_text())
config = json.loads((P/'comparator.json').read_text())
names = [x.removeprefix('NLA.KE04.') for x in config['theorem_names']]
assert len(names)==24 and len(set(names))==24
assert set(names)==set(challenge)==set(proof)
assert challenge==proof
assert config['definition_names']==[]
assert config['permitted_axioms']==['propext','Classical.choice','Quot.sound']
modules={}; external=set()
def walk(module):
    if module in modules: return
    f=P/(module.replace('.','/')+'.lean')
    s=clean(f.read_text())
    modules[module]={'sha256':sha(f),'lines':len(f.read_text().splitlines()),'imports':[]}
    assert not re.search(r'\b(sorry|sorryAx|admit|axiom|native_decide|unsafe)\b',s), module
    assert not re.search(r'\b(opaque|macro|syntax|elab|run_elab|initialize)\b',s), module
    for line in s.splitlines():
        if line.startswith('import '):
            for imp in line[7:].split():
                modules[module]['imports'].append(imp)
                assert imp != 'Challenge'
                if (P/(imp.replace('.','/')+'.lean')).exists(): walk(imp)
                else: external.add(imp)
walk('Solution')
assert len(modules)==11
assert set(modules)=={'Solution'}|{'NLA.KE04.'+p.stem for p in (P/'NLA/KE04').glob('*.lean')}
assert len(re.findall(r'\bsorry\b',clean((P/'Challenge.lean').read_text())))==24
assert re.findall(r'^import (.+)$',clean((P/'Challenge.lean').read_text()),re.M)==['NLA.KE04.Definitions']
for name in names:
    assert '#assert_trust kernel '+name in (P/'NLA/KE04/Proof.lean').read_text()
    assert '#print axioms '+name in (P/'NLA/KE04/Proof.lean').read_text()
def leaves(obj,path=()):
    if isinstance(obj,dict):
        for k,v in obj.items():
            yield from leaves(v,path+(k,))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): yield from leaves(v,path+(str(i),))
    else: yield path,obj
correspondence=sha(P/'SourceCorrespondence.md')
bound={}
for rel in ['DRAFT-INVENTORY.json','reviews/statement-freeze.json','reviews/proof-freeze.json']:
    data=json.loads((P/rel).read_text())
    matches=[{'location':'/'.join(k),'value':v} for k,v in leaves(data) if v==correspondence]
    assert matches,rel
    bound[rel]=matches
for p in ['reviews/statement-referee-1-evidence/attempt-nglj5yvu/source/SourceCorrespondence.md',
          'reviews/statement-referee-1-evidence/attempt-7tjmj3b0/source/SourceCorrespondence.md',
          'reviews/statement-referee-1-evidence/attempt-5t4u9ww4/source/SourceCorrespondence.md']:
    assert sha(P/p)==correspondence
old=subprocess.check_output(['git','show',BASE+':eigenvalues-and-inverse-problems/KE-04/README.md'],cwd=ROOT,text=True)
new=(P.parent/'README.md').read_text()
def target(s): return s.split('## Original problem statement\n',1)[1].split('\n## References',1)[0]
assert target(old)==target(new)
retained={}
for rel in ['solution.md','solution.tex','solution.pdf']:
    p=P.parent/rel
    oldbytes=subprocess.check_output(['git','show',BASE+':eigenvalues-and-inverse-problems/KE-04/'+rel],cwd=ROOT)
    assert oldbytes==p.read_bytes()
    retained[rel]=sha(p)
result={'result':'PASS','head':HEAD,'base':BASE,'proof_closure':modules,
        'external_direct_imports':sorted(external),'export_signatures_exact_after_whitespace_normalization':24,
        'placeholder_count_in_challenge_only':24,'proof_closure_placeholders_custom_axioms_or_native_decision':0,
        'frozen_source_correspondence_sha256':correspondence,'correspondence_bindings':bound,
        'canonical_target_byte_identical':True,'retained_original_manuscript_files':retained,
        'canonical_pdf_sha256':sha(P.parent/'problem.pdf'),'canonical_pdf_pages_visually_inspected':3,
        'coverage_limitation':'Source audit only; independent operational agent owns actual CI, Comparator and kernel evidence authentication.'}
out=args.output
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'result':result['result'],'exports':24,'closure_modules':len(modules),
                  'closure_lines':sum(x['lines'] for x in modules.values()),'correspondence_sha256':correspondence,
                  'canonical_pdf_sha256':result['canonical_pdf_sha256'],'report':str(out)},indent=2))
