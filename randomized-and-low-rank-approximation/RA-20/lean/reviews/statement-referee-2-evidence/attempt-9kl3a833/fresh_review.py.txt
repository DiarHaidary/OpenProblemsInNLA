"""Independent RA20 statement referee2. Fresh target objects; exact dependencies read-only.
Runner structure adapted from prior independent NLA reviews; statements never changed.
"""
from pathlib import Path
import datetime, hashlib, json, os, platform, re, shutil, subprocess, tempfile, time
E=Path(__file__).resolve().parent;P=E.parents[1]
W=Path('/Users/georgestepaniants/Research/OpenProblemsInNLA')
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
F=P/'reviews/statement-freeze.json';M=P/'reviews/statement-package-manifest.json'
assert sha(F)=='6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8'
assert sha(M)=='f703189ce7532af272df37e521ce9d703d01aaa9733cd7aa7d1f45813b0e5fa6'
f=json.loads(F.read_text());m=json.loads(M.read_text())
def preserve():
 for n,h in f['files'].items():assert sha(P/n)==h,n
 for n,r in m['files'].items():assert sha(P/n)==r['sha256'] and (P/n).stat().st_size==r['bytes'],n
 src=json.loads((P/'verification/original-source-inventory.json').read_text())
 for n,r in src['files'].items():
  raw=subprocess.check_output(['git','show',src['base']+':'+n],cwd=W)
  assert hashlib.sha256(raw).hexdigest()==r['sha256'] and (P/r['snapshot']).read_bytes()==raw,n
  assert subprocess.check_output(['git','rev-parse',src['base']+':'+n],cwd=W).decode().strip()==r['git_blob'],n
 assert not (P/'Solution.lean').exists() and not list((P/'NLA').rglob('Proof.lean'))
 return {'freeze_sha256':sha(F),'package_sha256':sha(M),'frozen_files':len(f['files']),
         'packaged_files':len(m['files']),'original_Git_sources':len(src['files'])}
def pins():
 out=[]
 for d in json.loads((P/'lake-manifest.json').read_text())['packages']:
  path=C/d['name'];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=path).decode().strip()
  assert head==d['rev'] and not subprocess.check_output(['git','status','--porcelain=v1'],cwd=path),d['name']
  out.append({'name':d['name'],'rev':head,'read_only_path':str(path),'clean':True})
 return out
identity=preserve();pinset=pins();prefix=Path(tempfile.mkdtemp(prefix='ra20-referee2-',dir='/tmp/nla-lean-formalization/independent-prefixes'))
assert not list(prefix.iterdir())
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
attempt=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));(attempt/'fresh_review.py.txt').write_bytes(Path(__file__).read_bytes())
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/leancert_examples',
 'scope':'Independent statement-only macOS source elaboration; no proof authoring, no Challenge import in diagnostic, no Lake/dependency copies/downloads, no Linux claim',
 'identity_before':identity,'pins':pinset,'prefix':str(prefix),'initially_empty':True,'LEAN_PATH':env['LEAN_PATH'],
 'platform':platform.platform(),'toolchain':subprocess.check_output([str(L/'bin/lean'),'--version']).decode().strip(),
 'commands':[],'verdict':'RUNNING'}
try:
 for rel in ['NLA/RA20/Definitions.lean','Challenge.lean','reviews/statement-referee-2-evidence/Inspect.lean']:
  s=P/rel;(attempt/(rel.replace('/','-')+'.txt')).write_bytes(s.read_bytes())
  out=prefix/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
  cmd=[str(L/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),str(s)]
  start=time.monotonic();c=subprocess.run(cmd,cwd=P,env=env,capture_output=True);log=attempt/(rel.replace('/','-').replace('.lean','.log'));log.write_bytes(c.stdout+c.stderr)
  row={'source':rel,'source_sha256':sha(s),'command':cmd,'exit_code':c.returncode,'seconds':time.monotonic()-start,'log':log.name,'log_sha256':sha(log)}
  r['commands'].append(row);(attempt/'result.json').write_text(json.dumps(r,indent=2)+'\n')
  print(rel,c.returncode,round(row['seconds'],2),flush=True)
  if c.returncode:print(log.read_text()[-12000:],flush=True)
  assert c.returncode==0,log
  text=log.read_text()
  if rel=='Challenge.lean':assert text.count('warning: declaration uses `sorry`')==12 and text.count('warning:')==12
  else:assert 'warning:' not in text and 'error:' not in text
  for ax in re.findall(r'depends on axioms: \[(.*?)\]',text):assert set(x.strip() for x in ax.split(','))- {''}<={'propext','Classical.choice','Quot.sound'}
 r['identity_after']=preserve();assert pins()==pinset;r['verdict']='PASS'
except BaseException as ex:
 r['verdict']='FAIL';r['failure']=repr(ex);raise
finally:
 r['own_objects_hashed_before_cleanup']=[{'path':str(x.relative_to(prefix)),'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(prefix.rglob('*')) if x.is_file()]
 shutil.rmtree(prefix);r['only_owned_generated_prefix_removed']=True
 (attempt/'result.json').write_text(json.dumps(r,indent=2)+'\n')
 (E/'latest.json').write_text(json.dumps({'attempt':str(attempt),'result_sha256':sha(attempt/'result.json')},indent=2)+'\n')
print('PASS',attempt,flush=True)
