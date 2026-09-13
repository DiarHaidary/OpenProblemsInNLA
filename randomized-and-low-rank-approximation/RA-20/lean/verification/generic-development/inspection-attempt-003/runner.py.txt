"""Fresh target-only RA20 generic helper inspection compilation; all attempts are retained."""
from pathlib import Path
import json,hashlib,os,subprocess,sys,time,datetime
E=Path(__file__).resolve().parent;P=E.parents[1]
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
frozen=json.loads((P/'reviews/statement-freeze.json').read_text())
for name,h in frozen['files'].items():assert sha(P/name)==h,name
prefix=Path(json.loads((E/'inspection-state.json').read_text())['prefix'])
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
record=E/'inspection-attempts.json'
j=json.loads(record.read_text()) if record.exists() else {'owner':'/root/mf16_final_referee','platform':subprocess.check_output(['uname','-a']).decode().strip(),'prefix':str(prefix),'LEAN_PATH':env['LEAN_PATH'],'scope':'Direct source inspection of root-owned Generic helper and frozen Definitions; shared exact MI22 artifacts read-only; no Lake, copy, download or Linux claim.','attempts':[]}
for src in sys.argv[1:]:
 f=P/src;attempt=E/('inspection-attempt-'+str(len(j['attempts'])+1).zfill(3));attempt.mkdir()
 (attempt/'source.lean.txt').write_bytes(f.read_bytes());(attempt/'runner.py.txt').write_bytes(Path(__file__).read_bytes())
 out=prefix/Path(src).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
 cmd=[str(L/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),str(f)]
 start=time.monotonic();r=subprocess.run(cmd,cwd=P,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=attempt/'compile.log';log.write_bytes(r.stdout)
 row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':src,'source_sha256':sha(f),'command':cmd,'exit_code':r.returncode,'seconds':time.monotonic()-start,'evidence':str(attempt.relative_to(E)),'log_sha256':sha(log)}
 j['attempts'].append(row);record.write_text(json.dumps(j,indent=2)+'\n')
 print(json.dumps(row),flush=True)
 print(r.stdout.decode(),flush=True)
 if r.returncode:sys.exit(r.returncode)
for name,h in frozen['files'].items():assert sha(P/name)==h,name
