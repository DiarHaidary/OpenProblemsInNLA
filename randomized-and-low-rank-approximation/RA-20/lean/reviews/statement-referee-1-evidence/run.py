from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,tempfile,os,time,re
P=Path('/tmp/nla-lean-formalization/next-ra-statements-draft/RA-20/lean');D=P/'reviews/statement-referee-1-evidence';assert not D.exists();D.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=P/'reviews/statement-freeze.json';assert sha(freeze)=='6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8';F=json.loads(freeze.read_text());assert len(F['files'])==68 and len(F['source_files'])==16
R=Path('/tmp/nla-lean-ra09-worktree')
for r,h in F['files'].items():assert sha(P/r)==h,r
for r,h in F['source_files'].items():
 data=subprocess.check_output(['git','show',F['base']+':'+r],cwd=R);assert hashlib.sha256(data).hexdigest()==h and (P/'verification/original-sources'/r).read_bytes()==data,r
names=['variety','definingIdeal','SmoothPoint','TangentVector','fullFrobeniusDistance','SmoothCriticalPoint','HasCriticalCount','HasGenericCriticalCount','predictedCount','criticalCountConjecture']
inspect='import NLA.RA20.Definitions\nimport LeanCert.Tactic.Verification\n\n/-! Root independent definition/statement boundary inspection; no Challenge import or theorem proof. -/\n'
for n in names:inspect+='\n#print NLA.RA20.'+n+'\n#assert_trust kernel NLA.RA20.'+n+'\n#print axioms NLA.RA20.'+n+'\n'
inspect+='\n#print Algebra.IsSmoothAt\n#print Algebra.smoothLocus\n#check MvPolynomial.vanishingIdeal\n#check MvPolynomial.pointToPoint\n#check Matrix.rank\n#check fderiv\n#check Cardinal.mk\n#synth IsAlgClosed ℂ\n#synth FiniteDimensional ℂ (NLA.RA20.Mat 3)\n#reduce (NLA.RA20.predictedCount 3 1, NLA.RA20.predictedCount 3 2, NLA.RA20.predictedCount 3 3, NLA.RA20.predictedCount 4 4)\n'
(D/'Inspect.lean').write_text(inspect);(D/'run.py').write_bytes(Path(__file__).read_bytes())
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages');L=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1');prefix=Path(tempfile.mkdtemp(prefix='root-ra20-statements-',dir='/tmp/nla-lean-formalization/independent-prefixes'))
pins=json.loads((P/'lake-manifest.json').read_text())['packages']
def pincheck():
 for x in pins:
  d=C/x['name'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=d).decode().strip()==x['rev'];assert not subprocess.check_output(['git','status','--porcelain'],cwd=d)
pincheck();assert len(pins)==10
order=['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib','leancert'];env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[prefix,*[C/n/'.lake/build/lib/lean' for n in order],L/'lib/lean']))
res={'utc':datetime.now(timezone.utc).isoformat(),'reviewer':'/root','role':'Independent RA20 statement referee1; no statement/proof contribution','scope':'Local macOS statement/definitions only; no claimed proof or Linux result','freeze_sha256':sha(freeze),'prefix':str(prefix),'initial_prefix_empty':not list(prefix.rglob('*')),'LEAN_PATH':env['LEAN_PATH'],'pins':pins,'commands':[]}
try:
 for name in ['NLA/RA20/Definitions.lean','Challenge.lean','reviews/statement-referee-1-evidence/Inspect.lean']:
  src=P/name;dest=prefix/Path(name).with_suffix('.olean');dest.parent.mkdir(parents=True,exist_ok=True);snap=name.replace('/','-');(D/(snap+'.txt')).write_bytes(src.read_bytes());cmd=[str(L/'bin/lean'),'-o',str(dest),'-i',str(dest.with_suffix('.ilean')),str(src)];start=time.monotonic();r=subprocess.run(cmd,cwd=P,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=D/(snap+'.log');log.write_bytes(r.stdout)
  row=dict(source=name,sha256=sha(src),command=cmd,exit_code=r.returncode,seconds=time.monotonic()-start,log=log.name,log_sha256=sha(log));res['commands'].append(row);(D/'result.json').write_text(json.dumps(res,indent=2)+'\n');print(name,r.returncode,flush=True);assert r.returncode==0,r.stdout.decode()
  txt=r.stdout.decode();reports=re.findall(r"'([^']+)' depends on axioms:\s*\[(.*?)\]",txt,re.S);row['axiom_reports']=len(reports)
  for _,x in reports:assert {a.strip() for a in x.split(',') if a.strip()}<={'propext','Classical.choice','Quot.sound'}
  if name=='Challenge.lean':assert txt.count('warning:')==12 and txt.count('declaration uses `sorry`')==12
  else:assert 'warning:' not in txt and 'error:' not in txt
 assert '(4, 7, 4, 28)' in (D/'reviews-statement-referee-1-evidence-Inspect.lean.log').read_text()
 pincheck();res['ten_pins_after_clean']=True
 for r,h in F['files'].items():assert sha(P/r)==h,r
 assert not (P/'Solution.lean').exists() and not list((P/'NLA').rglob('Proof.lean'))
 res['status']='PASS fresh exact statement and definition checks';res['all_68_frozen_inputs_and_16_source_blobs_preserved']=True
finally:
 res['generated_objects']=[dict(path=str(f.relative_to(prefix)),sha256=sha(f),bytes=f.stat().st_size) for f in prefix.rglob('*') if f.is_file()]
 (D/'result.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'status':res['status'],'reports':sum(r.get('axiom_reports',0) for r in res['commands']),'result_sha256':sha(D/'result.json')},indent=2))
