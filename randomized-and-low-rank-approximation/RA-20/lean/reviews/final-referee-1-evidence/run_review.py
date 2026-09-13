#!/usr/bin/env python3
"""Fresh final-referee-1 source replay. Reads shared dependencies; never rebuilds them."""
import datetime, hashlib, json, os, pathlib, platform, subprocess, time

E = pathlib.Path(__file__).resolve().parent
P = E.parent.parent
R = P.parents[2]
O = pathlib.Path('/tmp/nla-lean-formalization/independent-prefixes/ra20-final-referee1')
L = pathlib.Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
C = pathlib.Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, x): (E/name).write_text(json.dumps(x, indent=2) + '\n')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def raw(cmd, label, cwd=P):
    t=time.monotonic(); r=subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (E/(label+'.log')).write_bytes(r.stdout)
    rec={'utc':now(),'command':cmd,'cwd':str(cwd),'exit_code':r.returncode,'seconds':time.monotonic()-t}
    save(label+'.json',rec)
    if r.returncode: raise RuntimeError(rec)
    return r.stdout.decode()
def freeze_check():
    f=P/'verification/proof-freeze.json'
    assert sha(f)=='f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f'
    x=json.loads(f.read_text())
    assert len(x['files'])==521 and len(x['source_files'])==16
    for rel,h in x['files'].items(): assert sha(P/rel)==h,rel
    for rel,h in x['source_files'].items():
        assert sha(R/rel)==h,rel
        b=subprocess.check_output(['git','show',x['base']+':'+rel],cwd=R)
        assert hashlib.sha256(b).hexdigest()==h,rel
        g=subprocess.check_output(['git','rev-parse',x['base']+':'+rel],cwd=R).decode().strip()
        assert g==x['source_git_blobs'][rel],rel
    sf=json.loads((P/'reviews/statement-freeze.json').read_text())
    for rel,h in sf['files'].items(): assert sha(P/rel)==h,rel
    return {'utc':now(),'proof_freeze_sha256':sha(f),'proof_files':len(x['files']),
            'source_files_and_base_git_blobs':len(x['source_files']),'statement_files':len(sf['files'])}
def pins(phase):
    packages=json.loads((P/'lake-manifest.json').read_text())['packages']
    out=[]
    for p in packages:
        n=p['name']; d=C/n
        head=raw(['git','rev-parse','HEAD'],phase+'-'+n+'-head',d).strip()
        status=raw(['git','status','--porcelain','--untracked-files=no'],phase+'-'+n+'-status',d)
        assert head==p['rev'] and status=='',n
        out.append({'name':n,'rev':head,'tracked_status_clean':True})
    return out

if O.exists(): raise RuntimeError('Refusing an existing prefix; freshness would be ambiguous')
O.mkdir(parents=True)
save('preflight.json',{'utc':now(),'host':platform.platform(),'prefix':str(O),
                     'prefix_initial_files':list(O.iterdir()),'freeze':freeze_check(),
                     'pins':pins('before'),'toolchain':raw([str(L/'bin/lean'),'--version'],'lean-version').strip()})
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
env=os.environ.copy()
env['LEAN_PATH']=':'.join(map(str,[O,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
sources=['NLA/RA20/'+n+'.lean' for n in ['Definitions','Algebra','SmoothTransport','Smooth','Tangent','Differential','Generic','Critical','Count','Proof']]
sources+=['Solution.lean','reviews/final-referee-1-evidence/ReferenceChallenge.lean','reviews/final-referee-1-evidence/Inspect.lean']
records=[]
for k,rel in enumerate(sources,1):
    src=P/rel; dest=O/pathlib.Path(rel).with_suffix('');dest.parent.mkdir(parents=True,exist_ok=True)
    a=E/('attempt-%02d'%k);a.mkdir()
    (a/src.name).write_bytes(src.read_bytes())
    cmd=[str(L/'bin/lean'),'-o',str(dest.with_suffix('.olean')),'-i',str(dest.with_suffix('.ilean')),rel]
    rec={'utc':now(),'source':rel,'source_sha256':sha(src),'command':cmd,'cwd':str(P),'LEAN_PATH':env['LEAN_PATH']}
    (a/'command.json').write_text(json.dumps(rec,indent=2)+'\n')
    t=time.monotonic()
    with (a/'lean.log').open('wb') as f: result=subprocess.run(cmd,cwd=P,env=env,stdout=f,stderr=subprocess.STDOUT)
    rec.update(exit_code=result.returncode,seconds=time.monotonic()-t)
    (a/'result.json').write_text(json.dumps(rec,indent=2)+'\n');records.append(rec)
    save('commands.json',records)
    print(json.dumps({'attempt':k,'source':rel,'exit':result.returncode,'seconds':rec['seconds']}),flush=True)
    if result.returncode: raise RuntimeError('Elaboration failed; exact source and raw result retained at '+str(a))
save('postflight.json',{'utc':now(),'freeze':freeze_check(),'pins':pins('after'),'successful_commands':len(records),
                       'seconds':sum(r['seconds'] for r in records)})
print('FRESH_SOURCE_REPLAY_PASS',flush=True)
