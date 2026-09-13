"""Fresh author validation of the complete RA20 Smooth helper, with raw evidence.
Adapts the sealed NLA statement-review runner; no dependency mutation or copying.
"""
from pathlib import Path
import datetime, hashlib, json, os, platform, re, shutil, subprocess, tempfile, time
E=Path(__file__).resolve().parent; P=E.parents[1]
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
W=Path('/Users/georgestepaniants/Research/OpenProblemsInNLA')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
start=json.loads((E/'START.json').read_text()); imported=json.loads((E/'IMPORTED-HELPERS.json').read_text())
def preserve():
 for n,h in start['preserved_frozen_files'].items(): assert sha(P/n)==h,n
 for n,h in imported['files'].items(): assert sha(P/n)==h,n
 for n,r in start['preserved_original_sources'].items():
  raw=subprocess.check_output(['git','show','5830ed4fb06da0659414a3deb2a40ad327aca052:'+n],cwd=W)
  assert hashlib.sha256(raw).hexdigest()==r['sha256'] and (P/r['snapshot']).read_bytes()==raw,n
 return {'statement_inputs':68,'original_Git_sources':16,'imported_helpers':imported['files']}
def pins():
 out=[]
 for d in json.loads((P/'lake-manifest.json').read_text())['packages']:
  path=C/d['name']; rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=path).decode().strip()
  assert rev==d['rev'] and not subprocess.check_output(['git','status','--porcelain=v1'],cwd=path),d['name']
  out.append({'name':d['name'],'revision':rev,'clean':True,'read_only_path':str(path)})
 return out
A=Path(tempfile.mkdtemp(prefix='final-',dir=E));(A/'final_check.py.txt').write_bytes(Path(__file__).read_bytes())
prefix=Path(tempfile.mkdtemp(prefix='ra20-smooth-final-',dir='/tmp/nla-lean-formalization/independent-prefixes'))
assert not list(prefix.iterdir())
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
pinset=pins();identity=preserve()
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'implementation author validation, not independent referee or Ubuntu verification','prefix':str(prefix),'initially_empty':True,'no_old_project_objects':True,'LEAN_PATH':env['LEAN_PATH'],'pins':pinset,'identity_before':identity,'toolchain':subprocess.check_output([str(L/'bin/lean'),'--version']).decode().strip(),'platform':platform.platform(),'commands':[],'verdict':'RUNNING'}
mods=['NLA/RA20/Definitions.lean','NLA/RA20/Algebra.lean','NLA/RA20/SmoothTransport.lean','NLA/RA20/Smooth.lean','Challenge.lean','verification/smooth-development/Inspect.lean']
try:
 for rel in mods:
  s=P/rel;(A/(rel.replace('/','-')+'.txt')).write_bytes(s.read_bytes())
  out=prefix/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
  cmd=[str(L/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),str(s)]
  t=time.monotonic();c=subprocess.run(cmd,cwd=P,env=env,capture_output=True);log=A/(rel.replace('/','-')+'.log');log.write_bytes(c.stdout+c.stderr)
  text=log.read_text(); row={'source':rel,'source_sha256':sha(s),'command':cmd,'exit_code':c.returncode,'seconds':time.monotonic()-t,'log':log.name,'log_sha256':sha(log),'explicit_kernel_assertions_in_source':s.read_text().count('#assert_trust kernel'),'standard_three_reports':len(re.findall(r'depends on axioms: \[propext, Classical.choice, Quot.sound\]',text))}
  r['commands'].append(row);(A/'result.json').write_text(json.dumps(r,indent=2)+'\n')
  print(rel,c.returncode,round(row['seconds'],2),flush=True)
  if c.returncode: print(text[-16000:],flush=True)
  assert c.returncode==0,rel
  if rel=='Challenge.lean': assert text.count('warning: declaration uses `sorry`')==12 and text.count('warning:')==12
  else: assert 'warning:' not in text and 'error:' not in text
  for ax in re.findall(r'depends on axioms: \[(.*?)\]',text): assert set(ax.split(', '))<={'propext','Classical.choice','Quot.sound'}
  if rel.endswith('/Inspect.lean'):
   assert 'EXACT_FROZEN_CONTRACT_TYPE: PASS' in text
   r['actual_project_declarations']=int(re.search(r'ACTUAL_PROJECT_DECLARATIONS: (\d+)',text).group(1))
   r['required_material_dependencies']=re.findall(r'REQUIRED_MATERIAL_DEPENDENCY ([^\n]+)',text)
 r['identity_after']=preserve(); assert pins()==pinset
 r['explicit_kernel_assertions']=sum(c['explicit_kernel_assertions_in_source'] for c in r['commands'])
 r['standard_three_reports']=sum(c['standard_three_reports'] for c in r['commands'])
 r['verdict']='PASS'
except BaseException as ex:
 r['verdict']='FAIL';r['failure']=repr(ex)
finally:
 r['own_objects_hashed_before_cleanup']=[{'path':str(x.relative_to(prefix)),'sha256':sha(x),'bytes':x.stat().st_size}for x in sorted(prefix.rglob('*'))if x.is_file()]
 shutil.rmtree(prefix);r['own_generated_prefix_only_removed']=True
 (A/'result.json').write_text(json.dumps(r,indent=2)+'\n')
 (E/'FINAL.json').write_text(json.dumps({'attempt':str(A),'result_sha256':sha(A/'result.json'),'verdict':r['verdict']},indent=2)+'\n')
print(r['verdict'],A,flush=True)
raise SystemExit(0 if r['verdict']=='PASS' else 1)
