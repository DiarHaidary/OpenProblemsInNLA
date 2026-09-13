#!/usr/bin/env python3
"""Direct source-only witness checks. Development reuses only hash-verified own
compiled immutable dependencies; --fresh --inspect rebuilds in an empty prefix.
All actual attempts are retained. Never invokes Lake/network or copies caches.
"""
from pathlib import Path
import datetime,hashlib,json,os,platform,shutil,subprocess,tempfile,time,sys
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
PK=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
TC=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
ORDER=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert']
DEPS=['NLA/IE05/Definitions.lean','NLA/IE05/Scaling.lean','NLA/IE05/QR.lean','NLA/IE05/IntegerQR.lean','NLA/IE05/Pivot.lean','NLA/IE05/LUTrajectory.lean','NLA/IE05/ExactCertificates.lean']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):return {'sha256':sha(p),'bytes':p.stat().st_size}
def pins():
 ps=[]
 for d in json.loads((P/'lake-manifest.json').read_text())['packages']:
  q=PK/d['name'];head=subprocess.check_output(['git','-C',str(q),'rev-parse','HEAD'],text=True).strip()
  assert head==d['rev'] and not subprocess.check_output(['git','-C',str(q),'status','--porcelain','--untracked-files=no'],text=True)
  has=(q/'.lake/build/lib/lean').is_dir();assert has or d['name']=='Cli'
  ps.append({'name':d['name'],'rev':head,'tracked_clean':True,'object_directory_present':has})
 assert len(ps)==10
 return ps
def cleanup(prefix):
 assert prefix.parent==Path('/tmp') and prefix.name.startswith('nla-ie05-witness-')
 r={str(p.relative_to(prefix)):rec(p)for p in prefix.rglob('*')if p.is_file()}
 shutil.rmtree(prefix);return {'prefix':str(prefix),'objects':r,'removed':not prefix.exists()}
def main():
 fresh='--fresh'in sys.argv; inspect='--inspect'in sys.argv
 attempt=Path(tempfile.mkdtemp(prefix='attempt-',dir=E));snapshot=attempt/'source';snapshot.mkdir()
 statefile=E/'development-state.json';state=json.loads(statefile.read_text())if statefile.exists()else{}
 prior_cleanup=None
 if fresh and state.get('prefix'):
  prior_cleanup=cleanup(Path(state['prefix']));state={}
 if state.get('prefix'): prefix=Path(state['prefix']);assert prefix.is_dir()
 else:prefix=Path(tempfile.mkdtemp(prefix='nla-ie05-witness-',dir='/tmp'));state={'prefix':str(prefix),'compiled_dependencies':{}}
 mods=DEPS+['NLA/IE05/Witness.lean']+(['verification/witness-development/Inspect.lean']if inspect else[])
 source_rels=mods+['lean-toolchain','lakefile.toml','lake-manifest.json','comparator.json','verification/proof-start.json','verification/witness-development/compile.py']
 inputs={}
 for rel in source_rels:
  dst=snapshot/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/rel,dst);inputs[rel]=rec(P/rel)
 env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(prefix)]+[str(PK/x/'.lake/build/lib/lean')for x in ORDER]+[str(TC/'lib/lean')]);env['PATH']=str(TC/'bin')+os.pathsep+env.get('PATH','')
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'witness author direct-source validation','platform':platform.platform(),'toolchain':subprocess.check_output([str(TC/'bin/lean'),'--version'],text=True).strip(),'fresh':fresh,'inspect':inspect,'prefix':str(prefix),'prior_own_prefix_cleanup':prior_cleanup,'inputs':inputs,'commands':[],'reused_own_immutable_dependency_objects':[],'lean_path':env['LEAN_PATH'],'independent_review':False,'actual_linux_comparator':False}
 try:
  F=json.loads((P/'reviews/statement-freeze.json').read_text())
  for rel,h in F['files'].items():assert sha(P/rel)==h,rel
  result['frozen_inputs_before']=len(F['files']);result['pins_before']=pins()
  gate=json.loads((E/'gate-and-ownership.json').read_text())
  for rel,h in gate['immutable_imports'].items():assert sha(P/rel)==h,rel
  result['immutable_imports']=gate['immutable_imports']
  for rel in mods:
   o=prefix/Path(rel).with_suffix('.olean');i=o.with_suffix('.ilean');old=state['compiled_dependencies'].get(rel)
   if rel in DEPS and old and old['source']==inputs[rel] and o.is_file() and i.is_file() and rec(o)==old['olean'] and rec(i)==old['ilean']:
    result['reused_own_immutable_dependency_objects'].append({'source':rel,**old});continue
   o.parent.mkdir(parents=True,exist_ok=True);cmd=[str(TC/'bin/lean'),'-o',str(o),'-i',str(i),rel];start=time.monotonic()
   cp=subprocess.run(cmd,cwd=snapshot,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=240)
   log=attempt/(Path(rel).stem+'.log');log.write_text(cp.stdout)
   c={'source':rel,'argv':cmd,'exit_code':cp.returncode,'seconds':time.monotonic()-start,'log':log.name,'log_sha256':sha(log)};result['commands'].append(c);print(json.dumps(c),flush=True)
   if cp.returncode:break
   if rel in DEPS:state['compiled_dependencies'][rel]={'source':inputs[rel],'olean':rec(o),'ilean':rec(i),'producing_attempt':attempt.name}
  result['pins_after']=pins()
  for rel,h in F['files'].items():assert sha(P/rel)==h,rel
  for rel,h in gate['immutable_imports'].items():assert sha(P/rel)==h,rel
  result['frozen_inputs_after']=len(F['files']);result['source_unchanged']=all(rec(P/r)==d for r,d in inputs.items())
  result['pass']=len(result['commands'])+len(result['reused_own_immutable_dependency_objects'])==len(mods) and all(c['exit_code']==0 for c in result['commands']) and result['source_unchanged']
 finally:
  result['own_generated_objects_before_exit']={str(p.relative_to(prefix)):rec(p) for p in prefix.rglob('*') if p.is_file()}
  if fresh:
   result['own_prefix_cleanup']=cleanup(prefix);state={}
  else:result['own_prefix_retained_for_bounded_development']=str(prefix)
  statefile.write_text(json.dumps(state,indent=2)+'\n')
  (attempt/'result.json').write_text(json.dumps(result,indent=2)+'\n');(E/'latest.json').write_text(json.dumps({'attempt':attempt.name,'result_sha256':sha(attempt/'result.json')},indent=2)+'\n')
 print(json.dumps({'attempt':attempt.name,'pass':result.get('pass',False)}),flush=True)
 raise SystemExit(0 if result.get('pass') else 1)
if __name__=='__main__':main()
