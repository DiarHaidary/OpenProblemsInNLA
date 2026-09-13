#!/usr/bin/env python3
"""Independent committed RA20 source binding. No Lean, cache, network or Git mutation.
RA09 operational audits were consulted for navigation; all RA20 inputs are checked here.
"""
from pathlib import Path
import ast, datetime, hashlib, json, os, re, subprocess, time

E = Path(__file__).resolve().parent
P = E.parents[1]
G = P.parents[2]
REL = str(P.relative_to(G))
HEAD = '43603b173beb294c2588d83f936a8a96246fd5f0'
BASE = '5830ed4fb06da0659414a3deb2a40ad327aca052'
OLD = '7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50'
SHARED = Path('/tmp/nla-lean-formalization/fetched-tool-source-check')
counter = 0


def sha(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d = {}
    for k,v in pairs:
        assert k not in d, ('duplicate key',k)
        d[k] = v
    return d
def load(p): return json.loads(p.read_text(), object_pairs_hook=unique)
def save(p,d): p.write_text(json.dumps(d,indent=2)+'\n')
def cmd(args,stdin=None):
    global counter
    counter += 1
    d = E/'commands'/('source-%03d'%counter)
    d.mkdir()
    env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
    rec={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':args,'cwd':str(G),
         'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}}
    if stdin is not None:
        (d/'stdin').write_bytes(stdin);rec['stdin_sha256']=sha(stdin)
    save(d/'command.json',rec)
    start=time.monotonic()
    with (d/'stdout').open('wb') as out,(d/'stderr.log').open('wb') as err:
        r=subprocess.run(args,cwd=G,env=env,input=stdin,stdout=out,stderr=err)
    rec.update(exit_code=r.returncode,seconds=time.monotonic()-start,
               stdout_sha256=sha((d/'stdout').read_bytes()),stderr_sha256=sha((d/'stderr.log').read_bytes()))
    save(d/'result.json',rec)
    assert r.returncode==0,(d,r.returncode)
    return (d/'stdout').read_bytes()


assert cmd(['git','rev-parse','HEAD']).decode().strip()==HEAD
tree=cmd(['git','ls-tree','-r','-z',HEAD,'--',REL])
entries=[]
for e in tree.split(b'\0'):
    if not e: continue
    header, rawname=e.split(b'\t',1)
    mode,kind,oid=header.decode().split();name=rawname.decode()
    rel=str(Path(name).relative_to(REL))
    assert kind=='blob' and mode in {'100644','100755'}
    assert '.lake' not in Path(rel).parts and Path(rel).suffix not in {'.olean','.ilean','.o','.so','.a'}
    entries.append((rel,mode,oid))
assert len(entries)==1092
batch=cmd(['git','cat-file','--batch'],(''.join(oid+'\n' for _,_,oid in entries)).encode())
offset=0; inputs={}
for rel,mode,oid in entries:
    end=batch.index(b'\n',offset);head=batch[offset:end].decode().split()
    assert head[0]==oid and head[1]=='blob'
    size=int(head[2]); data=batch[end+1:end+1+size];offset=end+2+size
    assert batch[end+1+size:end+2+size]==b'\n'
    assert (P/rel).is_file() and not (P/rel).is_symlink() and (P/rel).read_bytes()==data
    assert hashlib.sha1(b'blob '+str(size).encode()+b'\0'+data).hexdigest()==oid
    inputs[rel]={'sha256':sha(data),'bytes':size,'git_blob':oid,'mode':mode}
assert offset==len(batch)
commit=cmd(['git','cat-file','commit',HEAD])
assert re.search(rb'^author George Stepaniants <> ',commit,re.M)
assert re.search(rb'^committer George Stepaniants <> ',commit,re.M)
assert not cmd(['git','diff','--name-only','HEAD','--',REL])

receipts={}
for src,name in [('/tmp/nla-lean-formalization/RA-20-candidate-commit.json','root-commit.json'),
                 ('/tmp/nla-lean-formalization/ra20-candidate-push-2026-09-13/result.json','root-push.json'),
                 ('/tmp/nla-lean-formalization/ra20-candidate-push-2026-09-13/candidate-tree-inputs.json','root-tree-inputs.json')]:
    source=Path(src);target=E/name;target.write_bytes(source.read_bytes())
    receipts[name]={'sha256':sha(target.read_bytes()),'bytes':target.stat().st_size}
root_tree=load(E/'root-tree-inputs.json')
assert root_tree['head']==HEAD
assert root_tree['files']=={REL+'/'+n:{'sha256':v['sha256'],'bytes':v['bytes']} for n,v in inputs.items()}
assert load(E/'root-commit.json')['candidate']==load(E/'root-push.json')['candidate']==HEAD

def check(path, expected, historical=False):
    path=path.resolve();h=expected if isinstance(expected,str) else expected['sha256']
    if historical and path==P/'README.md' and h==OLD:
        path=P/'verification/pre-candidate-README.md'
    assert path.is_file() and not path.is_symlink() and sha(path.read_bytes())==h,str(path)
    if isinstance(expected,dict) and 'bytes' in expected:
        assert path.stat().st_size==expected['bytes'],str(path)
    if path.is_relative_to(P):
        assert inputs[str(path.relative_to(P))]['sha256']==h
    return path

proof=load(P/'verification/proof-freeze.json');statement=load(P/'reviews/statement-freeze.json')
assert proof['base']==statement['base']==BASE
for f,c in [(proof,521),(statement,68)]:
    assert len(f['files'])==c
    for name,expected in f['files'].items():check(P/name,expected,True)
assert proof['source_files']==statement['source_files']
assert proof['source_git_blobs']==statement['source_git_blobs'] and len(proof['source_files'])==16
originals={}
for name,h in proof['source_files'].items():
    data=cmd(['git','show',BASE+':'+name])
    assert sha(data)==h and (G/name).read_bytes()==data
    assert cmd(['git','show',HEAD+':'+name])==data
    check(P/'verification/original-sources'/name,h)
    oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert oid==proof['source_git_blobs'][name]
    originals[name]={'sha256':h,'bytes':len(data),'git_blob':oid}

nested={}
for name in inputs:
    if name.endswith('EVIDENCE-MANIFEST.json') or name=='reviews/statement-package-manifest.json':
        path=P/name;m=load(path)
        parent=P if name=='reviews/statement-package-manifest.json' else path.parent
        for n,h in m['files'].items():check(parent/n,h,True)
        if 'file_count' in m:assert m['file_count']==len(m['files'])
        nested[name]={'sha256':inputs[name]['sha256'],'bound_files':len(m['files'])}
assert len(nested)==17
for name,count,h in [
    ('reviews/final-referee-1-evidence/EVIDENCE-MANIFEST.json',699,'360b0d841ebd8cb7219b39997e0b0a2617be32abfef461866d0f022ca134f70d'),
    ('reviews/final-referee-2-evidence/EVIDENCE-MANIFEST.json',793,'7fc642361790960be2d3a584d2842dc688d13511d93220907abc0d7ab951318c'),
    ('verification/linux-candidate-2026-09-13/EVIDENCE-MANIFEST.json',1010,'60f056cd293d2b093786a34e55b670975dd6b27e7e927acdbf8513438c28b381'),
    ('verification/candidate-packaging-referee-2026-09-13/EVIDENCE-MANIFEST.json',1102,'7cbac7459fca07b95fc8b511b6c21daa03e631178ea07da8f7d872f35c3f9605'),
    ('verification/root-candidate-2026-09-13/EVIDENCE-MANIFEST.json',10,'19a363307931a42bc7ae27e2d1ce039f6a1829e888415edbb18ae00498e0c6ba')]:
    assert nested[name]=={'sha256':h,'bound_files':count}
root=load(P/'verification/root-candidate-2026-09-13/ROOT-CHECKS.json')
check(P/'verification/root-candidate-2026-09-13/ROOT-CHECKS.json','f66c8d37518cf1d21c8d21963fe72faf5b0b4ef03423ce653888145611f75b7f')
assert len(root['prior_inputs'])==root['prior_input_count']==1081
for name,h in root['prior_inputs'].items():check(P/name,h)
rootfiles={n for n in inputs if n.startswith('verification/root-candidate-2026-09-13/')}
assert len(rootfiles)==11 and not set(root['prior_inputs'])&rootfiles
assert set(root['prior_inputs'])|rootfiles==set(inputs)
assert len(root['exact_hash_bound_whitespace_exceptions'])==14
gate=load(P/'verification/final-review-acceptance.json')
assert len(gate['reports'])==2
for r,c in zip(gate['reports'],[699,793]):
    check(P/r['report'],r['sha256']);check(P/r['evidence']['file'],r['evidence']['sha256'])
    assert nested[r['evidence']['file']]['bound_files']==c
    assert r['successful_fresh_source_commands']==13 and r['failed_Lean_commands']==0
    assert r['source_kernel_assertions']==61 and r['additional_kernel_assertions']==12
    assert r['actual_standard_three_reports']==69
check(P/'verification/final-review-acceptance.json','a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb')

config=load(P/'comparator.json');names=config['theorem_names']
assert len(names)==12 and config['definition_names']==[]
assert config['permitted_axioms']==['propext','Classical.choice','Quot.sound']
def headers(path):
    text=path.read_text()
    return {m.group(1):' '.join(text[m.end():text.index(':=',m.end())].split())
            for m in re.finditer(r'^theorem\s+(\w+)\s+',text,re.M)}
assert headers(P/'Challenge.lean')==headers(P/'Solution.lean')
assert ['NLA.RA20.'+n for n in headers(P/'Solution.lean')]==names
scan={}
for file in sorted((P/'NLA/RA20').glob('*.lean'))+[P/'Solution.lean']:
    text=re.sub(r'/\-.*?\-/','',file.read_text(),flags=re.S)
    text=re.sub(r'--[^\n]*','',text)
    assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe)\b',text),str(file)
    assert not re.search(r'^import\s+Challenge\b',text,re.M)
    assertions=re.findall(r'^#assert_trust kernel\s+(\S+)',text,re.M)
    prints=re.findall(r'^#print axioms\s+(\S+)',text,re.M)
    scan[str(file.relative_to(P))]={'sha256':sha(file.read_bytes()),'kernel_assertions':assertions,'printed_axioms':prints}
assert len(scan)==11
assert sum(len(v['kernel_assertions']) for v in scan.values())==61
assert sum(len(v['printed_axioms']) for v in scan.values())==57
assert '**Status:** Solved' in (P.parent/'README.md').read_text()

# Preserve only the small pinned checker sources, never dependency/build objects.
lock=load(G/'tools/lean/source-lock.json')
assert len(lock['files'])==58 and lock['commit']=='8d1b0c0545a77b40245e84705aa7d273e6c81e62'
assert lock['lean_toolchain']=='leanprover/lean4:v4.33.1'
checker={}
for item in lock['files']:
    data=(SHARED/item['destination']).read_bytes()
    assert len(data)==item['bytes'] and sha(data)==item['sha256']
    target=E/'checker-source'/item['destination'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    checker[item['destination']]={'sha256':sha(data),'bytes':len(data),'source':item['source']}
infrastructure={}
infra=['tools/lean/harness.py','tools/lean/source-lock.json','tools/lean/bootstrap.sh','tools/lean/selftest.sh',
       'tools/lean/verify.sh','tools/lean/projects.py','tools/lean/validate_manifest.py','tools/lean/HARNESS.md',
       '.github/workflows/lean-verification.yml','docs/lean/schema/v0.4.schema.json','problem_ids.json','AGENTS.md']
infra += [str(p.relative_to(G)) for p in (G/'.github/workflows').glob('*') if p.is_file() and 'problem_ids.py' in p.read_text()]
for name in dict.fromkeys(infra):
    data=cmd(['git','show',HEAD+':'+name]);assert data==(G/name).read_bytes()
    target=E/'infrastructure'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    infrastructure[name]={'sha256':sha(data),'bytes':len(data)}
harness=(G/'tools/lean/harness.py').read_text()
node=next(n for n in ast.parse(harness).body if isinstance(n,ast.FunctionDef) and n.name=='ci_probe_source')
ns={'Path':Path,'HarnessError':RuntimeError}
exec(compile(ast.Module(body=[node],type_ignores=[]),'audited_ci_probe_derivation','exec'),ns)
probe=ns['ci_probe_source'](SHARED).encode();(E/'checker-source/sandbox_probe_ci.py').write_bytes(probe)
assert len(load(G/'problem_ids.json'))==217
save(E/'source-binding.json',{
    'status':'PASS independent committed source binding; runtime acceptance remains separate',
    'reviewer':'/root/ra20_final_referee2','candidate':HEAD,'base':BASE,'project':REL,
    'candidate_inputs':inputs,'candidate_input_count':1092,'original_sources':originals,
    'proof_inputs':521,'statement_inputs':68,'complete_nested_manifests':nested,
    'archive_rule':{'exact_original_path':'README.md','only_expected_sha256':OLD,'archive':'verification/pre-candidate-README.md'},
    'root_prior_inputs':1081,'root_evidence_files_including_outer':11,
    'config':config,'source_trust_scan':scan,'source_kernel_assertions':61,'source_printed_axiom_reports':57,
    'final_referee_count_distinction':'Each historical final referee separately adds12 inspector assertions and12 prints; authoritative source build has61/57.',
    'source_lock_sha256':sha((G/'tools/lean/source-lock.json').read_bytes()),'checker_source_files':checker,
    'derived_ci_probe_sha256':sha(probe),'repository_infrastructure':infrastructure,
    'private_root_receipts':receipts,'blank_author_and_committer_email':True,
    'source_commands_recorded':counter,'new_Lean_builds':0,'new_dependencies_or_cache_copies':0,
    'canonical_status':'Solved, unchanged','new_mathematical_approval':False})
print(json.dumps({'status':'SOURCE_BINDING_PASS','candidate_inputs':1092,'nested_inventories':17,
                  'source_kernel_assertions':61,'source_printed_axioms':57,'recorded_source_commands':counter}))
