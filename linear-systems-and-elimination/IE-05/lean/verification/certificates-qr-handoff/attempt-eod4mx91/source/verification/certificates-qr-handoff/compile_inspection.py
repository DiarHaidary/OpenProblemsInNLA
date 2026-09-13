#!/usr/bin/env python3
"""Fresh joint source check; owns only this evidence directory and its new prefix."""
from pathlib import Path
import datetime,hashlib,json,os,platform,shutil,subprocess,tempfile,time
E=Path(__file__).resolve().parent;P=E.parents[1]
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
T=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 A=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));S=A/'source';S.mkdir()
 B=Path(tempfile.mkdtemp(prefix='nla-ie05-certificates-qr-',dir='/tmp'))
 assert not list(B.iterdir())
 env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
 result={'role':'bounded helper completion, not independent final proof approval',
  'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),
  'prefix':str(B),'prefix_initial_files':[],'source_snapshots':{},'commands':[],
  'new_Linux_or_Comparator':False,'prior_attempts_reexecuted':False}
 bound=json.loads((E/'INPUTS.json').read_text())
 def boundary():
  for n,v in bound['files'].items():assert sha(P/n)==v['sha256'] and (P/n).stat().st_size==v['bytes'],n
  return {'file_count':len(bound['files']),'INPUTS_sha256':sha(E/'INPUTS.json'),'all_match':True}
 def command(label,cmd,cwd):
  t=time.monotonic();cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  (A/(label+'.stdout')).write_bytes(cp.stdout);(A/(label+'.stderr')).write_bytes(cp.stderr)
  rec={'label':label,'argv':cmd,'cwd':str(cwd),'exit_code':cp.returncode,'seconds':time.monotonic()-t,
    'stdout_sha256':sha(A/(label+'.stdout')),'stderr_sha256':sha(A/(label+'.stderr'))}
  result['commands'].append(rec);write(A/'result.json',result)
  assert cp.returncode==0,(label,cp.stderr.decode(),cp.stdout.decode()[-1500:])
  return cp.stdout.decode().strip()
 def pins(stage):
  rows=[]
  for pkg in json.loads((P/'lake-manifest.json').read_text())['packages']:
   d=C/pkg['name']
   head=command(stage+'-'+pkg['name']+'-head',['git','-c','core.fsmonitor=false','rev-parse','HEAD'],d)
   status=command(stage+'-'+pkg['name']+'-status',['git','-c','core.fsmonitor=false','status','--porcelain','--untracked-files=no'],d)
   built=(d/'.lake/build/lib/lean').is_dir()
   assert head==pkg['rev'] and status=='' and (built or pkg['name']=='Cli'),pkg['name']
   rows.append({'name':pkg['name'],'rev':head,'tracked_clean':True,'build_directory_present':built})
  assert len(rows)==10 and sum(r['build_directory_present'] for r in rows)==9
  return rows
 modules=['NLA/IE05/'+n+'.lean' for n in ['Definitions','Scaling','QR','IntegerQR','ExactCertificates']]
 modules+=['verification/certificates-qr-handoff/Inspect.lean']
 sources=modules+['Challenge.lean','lean-toolchain','lakefile.toml','lake-manifest.json','comparator.json',
    'verification/proof-start.json','verification/certificates-qr-handoff/compile_inspection.py',
    'verification/certificates-qr-handoff/expected-type-extraction.json']
 for n in sources:
  p=P/n;q=S/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
  result['source_snapshots'][n]={'sha256':sha(p),'bytes':p.stat().st_size}
 try:
  result['boundary_before']=boundary();result['pins_before']=pins('before')
  result['Lean_version']=command('lean-version',[str(T/'bin/lean'),'--version'],S)
  result['Lean_binary_sha256']=sha(T/'bin/lean')
  paths=[B]+[C/r['name']/'.lake/build/lib/lean' for r in result['pins_before'] if r['build_directory_present']]+[T/'lib/lean']
  env['LEAN_PATH']=os.pathsep.join(map(str,paths));result['LEAN_PATH']=env['LEAN_PATH']
  result['modules']=modules
  for n in modules:
   out=B/Path(n).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
   command(Path(n).stem,[str(T/'bin/lean'),'-o',str(out),'-i',str(out.with_suffix('.ilean')),n],S)
   print(json.dumps({'source':n,'exit_code':0}),flush=True)
  result['pins_after']=pins('after');result['boundary_after']=boundary()
  assert result['pins_before']==result['pins_after']
  assert all(sha(P/n)==v['sha256'] for n,v in result['source_snapshots'].items())
  result['sources_unchanged_after']=True;result['pass']=True
 except BaseException as exc:
  result['pass']=False;result['exception']=repr(exc)
  raise
 finally:
  objects={str(p.relative_to(B)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.rglob('*')) if p.is_file()}
  write(A/'objects-before-removal.json',objects)
  assert B.parent==Path('/tmp') and B.name.startswith('nla-ie05-certificates-qr-')
  assert all(not p.is_symlink() for p in B.rglob('*'))
  assert {str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()}==set(objects)
  for n,v in objects.items():assert sha(B/n)==v['sha256']
  shutil.rmtree(B);result['own_prefix_removed']=not B.exists()
  result['object_count']=len(objects);result['objects_sha256']=sha(A/'objects-before-removal.json')
  result['finish_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
  write(A/'result.json',result)
  write(E/'latest.json',{'attempt':A.name,'result_sha256':sha(A/'result.json'),'pass':result['pass']})
  print(json.dumps({'attempt':A.name,'pass':result['pass'],'own_prefix_removed':result['own_prefix_removed']}),flush=True)
if __name__=='__main__':main()
