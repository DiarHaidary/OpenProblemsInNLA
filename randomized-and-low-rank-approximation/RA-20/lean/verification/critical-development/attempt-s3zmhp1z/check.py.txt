"""RA20 Critical development. Exact MI22 dependencies read-only, own initially empty prefix.
Adapted from the completed Smooth helper's development runner; all attempts retained.
"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,tempfile,time
E=Path(__file__).resolve().parent;P=E.parents[1];sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
start=json.loads((E/'START.json').read_text());prefix=Path(start['prefix'])
for n,h in start['frozen_files'].items():assert sha(P/n)==h,n
for n,h in start['imports'].items():assert sha(P/n)==h,n
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
A=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));(A/'check.py.txt').write_bytes(Path(__file__).read_bytes())
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'/root/leancert_examples','scope':'Author development; no old target objects, dependencies read-only, no Lake/cache copy/download','prefix':str(prefix),'LEAN_PATH':env['LEAN_PATH'],'commands':[],'verdict':'RUNNING'}
try:
 for rel in sys.argv[1:]:
  s=P/rel;(A/(rel.replace('/','-')+'.txt')).write_bytes(s.read_bytes());out=prefix/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
  cmd=[str(L/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),str(s)]
  t=time.monotonic();c=subprocess.run(cmd,cwd=P,env=env,capture_output=True);log=A/(rel.replace('/','-')+'.log');log.write_bytes(c.stdout+c.stderr)
  row={'source':rel,'source_sha256':sha(s),'command':cmd,'exit_code':c.returncode,'seconds':time.monotonic()-t,'log':log.name,'log_sha256':sha(log)}
  r['commands'].append(row);(A/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(rel,c.returncode,round(row['seconds'],2),flush=True)
  if c.returncode:print(log.read_text()[-20000:],flush=True);raise RuntimeError('Lean command failed')
 for n,h in start['frozen_files'].items():assert sha(P/n)==h,n
 for n,h in start['imports'].items():assert sha(P/n)==h,n
 r['verdict']='PASS'
except BaseException as ex:r['verdict']='FAIL';r['failure']=repr(ex)
finally:
 r['own_objects']=[{'path':str(x.relative_to(prefix)),'sha256':sha(x),'bytes':x.stat().st_size}for x in sorted(prefix.rglob('*'))if x.is_file()]
 (A/'result.json').write_text(json.dumps(r,indent=2)+'\n');(E/'latest.json').write_text(json.dumps({'attempt':str(A),'result_sha256':sha(A/'result.json')},indent=2)+'\n')
print(r['verdict'],A,flush=True)
raise SystemExit(0 if r['verdict']=='PASS' else 1)
