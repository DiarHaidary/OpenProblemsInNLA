"""Validate the root-authored Generic helper and scoped inspection evidence."""
from pathlib import Path
import datetime,hashlib,json,platform,re,subprocess
E=Path(__file__).resolve().parent;P=E.parents[1]
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
load=lambda f:json.loads(Path(f).read_text())
expected='47676372aa8e028a2c12bf6c23951b0edf5b7404a18abd24487d36399b7fb007'
assert sha(P/'NLA/RA20/Generic.lean')==expected
role=load(E/'packaging-inspection-role.json');state=load(E/'inspection-state.json')
assert state['role_receipt_sha256']==sha(E/'packaging-inspection-role.json')
assert role['source_changes_authorized'] is False
assert sha(P/'verification/proof-start.json')==role['proof_start_gate_sha256']=='9fe55d622e50390cb3ed439989b9393455fa48eb50d42d84fb33c20fd8c883f3'
assert sha(P/'reviews/statement-freeze.json')==role['statement_freeze_sha256']=='6bd2bbf4a6d787fd4e0c5c8b19aad74dac73b7e79c9552e537544136a4812aa8'
freeze=load(P/'reviews/statement-freeze.json')
def check_files(base,entries):
 for n,r in entries.items():
  f=base/n;assert sha(f)==(r if isinstance(r,str) else r['sha256']),n
  if isinstance(r,dict) and 'bytes' in r:assert f.stat().st_size==r['bytes'],n
check_files(P,freeze['files'])
assert len(freeze['files'])==68 and len(freeze['source_files'])==16
for n,h in freeze['source_files'].items():
 f=P/'verification/original-sources'/n;b=f.read_bytes()
 assert sha(f)==h and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==freeze['source_git_blobs'][n],n
nested={}
for name,base in [('reviews/statement-package-manifest.json',P),
 ('reviews/statement-referee-1-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-1-evidence'),
 ('reviews/statement-referee-2-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-2-evidence')]:
 d=load(P/name);check_files(base,d['files']);nested[name]={'sha256':sha(P/name),'bound_files':len(d['files'])}
std={'propext','Classical.choice','Quot.sound'}
author=[]
for n in ['attempt-dueo3o_u','attempt-wwp2k0kt']:
 A=E/n;r=load(A/'result.json');d=load(A/'Definitions-result.json')
 assert d['exit_code']==0 and d['source_sha256']==sha(A/'Definitions.lean.txt')==sha(P/'NLA/RA20/Definitions.lean')
 assert d['log_sha256']==sha(A/'Definitions.log')
 assert r['source_sha256']==sha(A/'source.lean.txt') and r['raw_log_sha256']==sha(A/'lean.log')
 assert sha(A/'runner.py')==sha(E/'root-author-runner.py.txt')
 assert r['gate_ownership_sha256']==sha(E/'gate-and-ownership.json')
 assert r['pins_before']==r['pins_after'] and len(r['pins_before'])==10
 for f in r['generated_objects_hashed_then_removed']:
  assert not (Path(r['fresh_prefix'])/f['path']).exists()
 if n=='attempt-wwp2k0kt':
  assert r['source_sha256']==expected and r['exit_code']==0 and r['actual_explicit_kernel_and_standard_three_reports']==4
  logs=(A/'lean.log').read_text();assert 'error:' not in logs and 'warning:' not in logs
  reports=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',logs);assert len(reports)==4
  for a in reports:assert set(x.strip() for x in a.split(','))==std
 else:
  assert r['exit_code']==1 and 'Type mismatch' in (A/'lean.log').read_text()
  assert 'sorryAx' in (A/'lean.log').read_text()
 author.append({'attempt':n,'Definitions_command':d['command'],'Definitions_exit_code':d['exit_code'],
  'Generic_command':r['command'],'Generic_exit_code':r['exit_code'],'Generic_source_sha256':r['source_sha256'],
  'result_sha256':sha(A/'result.json'),'Definitions_result_sha256':sha(A/'Definitions-result.json')})
latest=load(E/'latest.json');assert latest['attempt']=='attempt-wwp2k0kt' and latest['result_sha256']==sha(E/'attempt-wwp2k0kt/result.json')
rows=load(E/'inspection-attempts.json')['attempts'];assert len(rows)==4
for r in rows:
 assert r['exit_code']==0
 A=E/r['evidence'];assert sha(A/'source.lean.txt')==r['source_sha256']==sha(P/r['source'])
 assert sha(A/'compile.log')==r['log_sha256'] and sha(A/'runner.py.txt')==sha(E/'compile_inspection.py')
challenge=(P/'Challenge.lean').read_text()
reference=challenge.replace('namespace NLA.RA20\n','namespace NLA.RA20.GenericHelperReference\n').replace('end NLA.RA20\n','end NLA.RA20.GenericHelperReference\n')
assert (E/'Reference.lean').read_text()==reference
log=(E/rows[-1]['evidence']/'compile.log').read_text()
assert 'EXACT_FROZEN_TYPE NLA.RA20.generic_data_intersection_proved:' in log
assert 'PROJECT_COUNTS declarations=15, required=13' in log
assert len(re.findall(r'^RETAINED_DEPENDENCY ',log,re.M))==13
axs=re.findall(r'^ACTUAL_AXIOMS (\S+): \[([^\]]*)\]',log,re.M);assert len(axs)==15
for n,a in axs:assert set(x.strip() for x in a.split(',') if x.strip())<=std,(n,a)
inspection_reports=0
for r in rows:
 t=(E/r['evidence']/'compile.log').read_text()
 if r['source'].endswith('/Reference.lean'):continue
 assert 'error:' not in t and 'warning:' not in t
 for a in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',t):
  assert set(x.strip() for x in a.split(','))==std;inspection_reports+=1
assert inspection_reports==5
text=(P/'NLA/RA20/Generic.lean').read_text()
assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|unsafe)\b',text)
assert 'Challenge' not in text and 'GenericHelperReference' not in text
assert len(re.findall(r'^#assert_trust kernel ',text,re.M))==4
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
pins=load(P/'lake-manifest.json')['packages'];post=[]
for p in pins:
 repo=C/p['name'];rev=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
 status=subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True)
 assert rev==p['rev'] and not status,p['name'];post.append({'name':p['name'],'revision':rev,'status':status})
assert len(post)==10
(E/'dependency-pins-after-inspection.json').write_text(json.dumps({'scope':'Packager post-inspection read-only current pin/status check. Original root attempts separately record before/after checks. No packager pre-inspection pin sample is claimed.','packages':post},indent=2)+'\n')
apis=[C/'mathlib/Mathlib/Algebra/MvPolynomial/Funext.lean',C/'mathlib/Mathlib/Algebra/MvPolynomial/Rename.lean',C/'leancert/LeanCert/Tactic/Verification.lean']
(E/'primary-api-inputs.json').write_text(json.dumps({'scope':'Primary infinite-domain polynomial funext, rename and LeanCert kernel trust APIs','files':{str(f):{'sha256':sha(f),'bytes':f.stat().st_size} for f in apis}},indent=2)+'\n')
lean=Path(rows[0]['command'][0])
(E/'tools.json').write_text(json.dumps({'platform':platform.platform(),'lean_binary':str(lean),'lean_binary_sha256':sha(lean),'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),'python_version':platform.python_version(),'LEAN_PATH':load(E/'inspection-attempts.json')['LEAN_PATH']},indent=2)+'\n')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS scoped Generic helper packaging/inspection, exact contract 9 only','implementation_author':'/root','packager_inspector':'/root/mf16_final_referee','independent_final_mathematical_approval':False,'helper_source_sha256':expected,
 'frozen_inputs':68,'original_source_Git_blobs':16,'nested_statement_inventories':nested,
 'author_attempts':author,'author_successful_attempt_commands':2,'author_successful_attempt_trust_reports':4,
 'author_retained_failed_attempt':{'Definitions_commands_passed':1,'Generic_commands_failed':1,'partial_failed_module_reports_not_counted_as_acceptance':True},
 'packager_successful_fresh_source_commands':4,'packager_trust_reports':5,'exact_frozen_contract_types':1,'actual_safe_project_declarations':15,'material_dependencies':13,'source_changes':False,
 'scope':'Local macOS source-only prefix and read-only pinned ten-package MI22 dependencies. No artificial interval; no whole-project result, independent final review, Linux, Comparator or publication claim.'}
(E/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
