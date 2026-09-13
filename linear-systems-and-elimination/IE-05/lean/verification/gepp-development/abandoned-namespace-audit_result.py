#!/usr/bin/env python3
"""Read-only mathematical-input and author evidence audit for the GEPP handoff.
This script writes only its scoped audit result; it does not build dependencies.
"""
from pathlib import Path
import hashlib,json,re,subprocess,datetime,sys
P=Path(__file__).resolve().parents[2]; E=Path(__file__).resolve().parent
GIT=Path('/tmp/nla-lean-ra20-worktree')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lean_code(source):
    # Erase nested Lean comments and quoted strings, preserving other code.
    out=[]; i=0; depth=0
    while i<len(source):
        if depth:
            if source.startswith('/-',i): depth+=1;i+=2
            elif source.startswith('-/',i): depth-=1;i+=2
            else: i+=1
        elif source.startswith('/-',i): depth=1;i+=2;out.append(' ')
        elif source.startswith('--',i):
            end=source.find('\n',i);i=len(source) if end<0 else end
            out.append(' ')
        elif source[i]=='"':
            i+=1
            while i<len(source):
                if source[i]=='\\': i+=2
                elif source[i]=='"':i+=1;break
                else:i+=1
            out.append(' ')
        else:out.append(source[i]);i+=1
    assert depth==0
    return ''.join(out)
freeze_path=P/'reviews/statement-freeze.json'
assert sha(freeze_path)=='bd329885eb323bd4f3fd40879649b56c201918d8c2bd6f63fbd0e86f48ca770c'
F=json.loads(freeze_path.read_text())
assert len(F['files'])==733
for rel,h in F['files'].items(): assert sha(P/rel)==h,rel
sources={}
for rel,h in F['source_files'].items():
    b=(P/F['source_snapshot_directory']/rel).read_bytes()
    actual=subprocess.check_output(['git','-C',str(GIT),'show',F['base']+':'+rel])
    blob=subprocess.check_output(['git','-C',str(GIT),'rev-parse',F['base']+':'+rel],text=True).strip()
    assert b==actual and hashlib.sha256(b).hexdigest()==h and blob==F['source_git_blobs'][rel],rel
    sources[rel]={'sha256':h,'git_blob':blob,'bytes':len(b)}
latest=json.loads((E/'latest.json').read_text()); A=E/latest['attempt']
assert sha(A/'result.json')==latest['result_sha256']
R=json.loads((A/'result.json').read_text())
assert R['pass'] and len(R['commands'])==4 and all(c['exit_code']==0 for c in R['commands'])
assert R['own_prefix_removed'] and not Path(R['prefix']).exists()
assert R['source_unchanged'] and R['frozen_inputs_after']==733
for rel,d in R['inputs'].items(): assert sha(P/rel)==d['sha256'],rel
for c in R['commands']: assert sha(A/c['log'])==c['log_sha256'],c['source']
assert R['pins_before']==R['pins_after'] and len(R['pins_after'])==10
for pin in R['pins_after']:
    path=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')/pin['name']
    assert subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()==pin['rev']
    assert not subprocess.check_output(['git','-C',str(path),'status','--porcelain','--untracked-files=no'],text=True)
logs={c['source']:(A/c['log']).read_text() for c in R['commands']}
I=logs['verification/gepp-development/Inspect.lean']
assert len(re.findall(r'^EXACT_FROZEN_TYPE ',I,re.M))==5
assert len(re.findall(r'^ACTUAL_AXIOMS ',I,re.M))==70
assert len(re.findall(r'^PROJECT_EDGE ',I,re.M))==70
assert len(re.findall(r'^RETAINED_DEPENDENCY ',I,re.M))==42
assert 'PROJECT_COUNTS declarations=70, required=42' in I
assert not re.search(r'^.*:\d+:\d+: error:',I,re.M)
assert len(re.findall(r'^.*:\d+:\d+: warning:',I,re.M))==6
axiom_lists=re.findall(r'^ACTUAL_AXIOMS .*?: \[([^\]]*)\]',I,re.M)
for atoms in axiom_lists:
    assert set(filter(None,atoms.split(', '))) <= {'propext','Classical.choice','Quot.sound'}
standard_three={k:len(re.findall(r"depends on axioms: \[propext, Classical.choice, Quot.sound\]",v)) for k,v in logs.items()}
assert list(standard_three.values())==[0,5,11,5]
math_paths=['NLA/IE05/Pivot.lean','NLA/IE05/GEPP.lean']
for rel in math_paths:
    s=lean_code((P/rel).read_text())
    assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|unsafe|partial)\b',s),rel
    assert not re.search(r'^import .*Challenge',s,re.M),rel
assert sha(P/math_paths[0])=='89a404945ce5fc2c04d06dd971f7a155d7ef1a48c3c331082bdea9df89dc6f69'
assert sha(P/math_paths[1])=='f9cfa58bd03aa49748bfde358147197bf73b165701cb67b58e1af2ec926c8b98'
# Literal header extraction remains independently reproducible from the frozen file.
X=json.loads((E/'expected-type-extraction.json').read_text())
challenge=(P/'Challenge.lean').read_text()
for name,header in X['headers'].items():
    assert re.search(r'^theorem '+name+r'\b(.*?) := by sorry$',challenge,re.M|re.S).group(1)==header
assert sha(E/'Inspect.lean')==X['inspector_sha256']
# Every retained attempt remains immutable and its own generated prefix was removed.
attempts={}
for a in sorted(E.glob('attempt-*')):
    r=json.loads((a/'result.json').read_text())
    assert r['own_prefix_removed'] and not Path(r['prefix']).exists()
    for c in r['commands']: assert sha(a/c['log'])==c['log_sha256']
    for rel,d in r['inputs'].items(): assert sha(a/'source'/rel)==d['sha256']
    attempts[a.name]={'pass':r['pass'],'commands':[(c['source'],c['exit_code']) for c in r['commands']], 'result_sha256':sha(a/'result.json')}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,
 'scope':'bounded author validation of first five IE05 contracts; not a full proof, independent final review, or Linux Comparator',
 'fresh_final_attempt':A.name,'fresh_result_sha256':sha(A/'result.json'),'fresh_elapsed_seconds':sum(c['elapsed_seconds'] for c in R['commands']),
 'frozen_inputs_preserved':733,'original_source_count':len(sources),'original_sources':sources,
 'math_sources':{rel:{'sha256':sha(P/rel),'bytes':(P/rel).stat().st_size}for rel in math_paths},
 'exact_frozen_types':5,'safe_project_declarations':70,'retained_material_dependencies':42,
 'kernel_assertions_in_fresh_sources':21,'standard_three_reports':standard_three,
 'diagnostic_expected_type_unused_binder_warnings':6,'math_source_warnings':0,
 'pins':R['pins_after'],'platform':R['platform'],'toolchain':R['toolchain_version'],
 'attempts':attempts,'all_own_prefixes_removed':True,'no_shared_cache_mutation':True,
 'canonical_or_git_mutation':False,'independent_final_review':False,'authoritative_linux_verification':False}
(E/'audit-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['pass','fresh_final_attempt','frozen_inputs_preserved','original_source_count','safe_project_declarations','retained_material_dependencies']}))
