"""Validate the scoped RA20 helper evidence without rebuilding or changing dependencies."""
from pathlib import Path
import datetime, hashlib, json, os, platform, re, subprocess
E=Path(__file__).resolve().parent; P=E.parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
def check_files(base, entries):
 for name,v in entries.items():
  f=base/name; h=v if isinstance(v,str) else v['sha256']
  assert f.is_file() and sha(f)==h,(str(f),'hash')
  if isinstance(v,dict) and 'bytes' in v:assert f.stat().st_size==v['bytes'],str(f)
state=load(E/'development-state.json')
locks={'verification/proof-start.json':state['gate_sha256'],
 'verification/implementation-roles.json':state['roles_sha256'],
 'reviews/statement-freeze.json':state['statement_freeze_sha256']}
check_files(P,locks)
freeze=load(P/'reviews/statement-freeze.json');check_files(P,freeze['files'])
for name,h in freeze['source_files'].items():
 f=P/'verification/original-sources'/name; b=f.read_bytes()
 assert sha(f)==h,name
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==freeze['source_git_blobs'][name],name
nested={}
for name,base in [('reviews/statement-package-manifest.json',P),
 ('reviews/statement-referee-1-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-1-evidence'),
 ('reviews/statement-referee-2-evidence/EVIDENCE-MANIFEST.json',P/'reviews/statement-referee-2-evidence')]:
 d=load(P/name);check_files(base,d['files'])
 nested[name]={'sha256':sha(P/name),'bound_files':len(d['files'])}
source=(P/'Challenge.lean').read_text()
reference=source.replace('namespace NLA.RA20\n','namespace NLA.RA20.DifferentialReference\n').replace('end NLA.RA20\n','end NLA.RA20.DifferentialReference\n')
assert (E/'Reference.lean').read_text()==reference
attempts=load(E/'compile-attempts.json')['attempts']
for row in attempts:
 d=E/row['evidence'];assert sha(d/'source.lean.txt')==row['source_sha256']
 assert sha(d/'compile.log')==row['log_sha256']
assert len(attempts)==8 and sum(x['exit_code']==0 for x in attempts)==4
helper=[x for x in attempts if x['source']=='NLA/RA20/Differential.lean'][-1]
inspect=[x for x in attempts if x['source'].endswith('/Inspect.lean')][-1]
assert helper['exit_code']==inspect['exit_code']==0
assert helper['source_sha256']==sha(P/helper['source'])
assert inspect['source_sha256']==sha(P/inspect['source'])
log=(E/inspect['evidence']/'compile.log').read_text()
assert 'error:' not in log
assert len(re.findall(r'^EXACT_FROZEN_TYPE ',log,re.M))==3
assert len(re.findall(r'^RETAINED_DEPENDENCY ',log,re.M))==16
assert 'PROJECT_COUNTS declarations=45, required=16' in log
axs=re.findall(r'^ACTUAL_AXIOMS (\S+): \[([^\]]*)\]',log,re.M)
assert len(axs)==45
std={'propext','Classical.choice','Quot.sound'}
for n,a in axs:assert set(x.strip() for x in a.split(',') if x.strip())<=std,(n,a)
reports=0
for row in [helper,inspect]:
 t=(E/row['evidence']/'compile.log').read_text()
 rs=re.findall(r"depends on axioms: \[([^\]]*)\]",t)
 for a in rs:assert set(x.strip() for x in a.split(','))==std,a
 reports+=len(rs)
assert reports==9
helper_text=(P/'NLA/RA20/Differential.lean').read_text()
assert len(re.findall(r'^#assert_trust kernel ',helper_text,re.M))==3
assert len(re.findall(r'^#assert_trust kernel ',(E/'Inspect.lean').read_text(),re.M))==6
assert not re.search(r'\b(?:sorry|axiom|native_decide|unsafe)\b',helper_text)
assert 'Challenge' not in helper_text and 'DifferentialReference' not in helper_text
assert 'set_option leancert.trust "kernel"' in helper_text
before=load(E/'dependency-pins-before.json');after=[]
for row in before:
 f=Path(row['path'])
 rev=subprocess.check_output(['git','-C',str(f),'rev-parse','HEAD'],text=True).strip()
 status=subprocess.check_output(['git','-C',str(f),'status','--porcelain','--untracked-files=no'],text=True)
 assert rev==row['revision'] and status==row['status']=='',row['name']
 after.append({'name':row['name'],'revision':rev,'status':status,'path':str(f)})
(E/'dependency-pins-after.json').write_text(json.dumps(after,indent=2)+'\n')
C=Path(before[1]['path']); LC=Path(before[0]['path'])
apis=[C/'Mathlib/Analysis/Calculus/FDeriv/Linear.lean',
 C/'Mathlib/Analysis/Calculus/FDeriv/Add.lean',C/'Mathlib/Analysis/Calculus/FDeriv/Mul.lean',
 C/'Mathlib/Analysis/Calculus/FDeriv/Prod.lean',C/'Mathlib/Analysis/Calculus/FDeriv/Basic.lean',
 C/'Mathlib/Analysis/Matrix/Normed.lean',
 C/'Mathlib/Topology/Algebra/Module/ContinuousLinearMap/PiProd.lean',
 LC/'LeanCert/Tactic/Verification.lean',
 Path('/tmp/nla-lean-ra09-worktree/randomized-and-low-rank-approximation/RA-09/lean/reviews/final-referee-2-evidence/Inspect.lean')]
api_inventory={str(f):{'sha256':sha(f),'bytes':f.stat().st_size} for f in apis}
(E/'primary-api-inputs.json').write_text(json.dumps({'scope':'Primary Mathlib/LeanCert APIs and completed campaign inspector structure consulted; no dependency copied or changed.','files':api_inventory},indent=2)+'\n')
lean=Path(helper['command'][0]); tool={'platform':platform.platform(),'machine':platform.machine(),
 'lean_binary':str(lean),'lean_binary_sha256':sha(lean),
 'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),
 'python_version':platform.python_version(),'LEAN_PATH':load(E/'compile-attempts.json')['LEAN_PATH']}
(E/'tools.json').write_text(json.dumps(tool,indent=2)+'\n')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'role':'Scoped differential helper author; not independent final referee for RA20',
 'status':'PASS: contracts 5,6,8 only; no full-project or Linux acceptance',
 'helper_sha256':sha(P/'NLA/RA20/Differential.lean'),
 'frozen_project_inputs':len(freeze['files']),'original_sources':len(freeze['source_files']),
 'all_source_Git_blob_identities_preserved':True,'locks':locks,'nested_inventories':nested,
 'exact_elaborated_contracts':3,'safe_type_and_body_reached_project_declarations':45,
 'retained_required_dependencies':16,'successful_source_commands':4,'retained_failed_attempts':4,
 'successful_explicit_LeanCert_kernel_and_standard_three_reports':9,
 'implementation_errors_corrected':3,
 'inspector_error_corrected':'Attempt 007 expected reflexive matrixEntry_apply to survive elaboration. Definitional reduction erased it; replaced that expectation with the actual ContinuousLinearMap.proj dependency. No implementation change for this inspector correction.',
 'warnings':'The final helper has two nonblocking style suggestions to use let in place of letI. Reference warnings are intentional diagnostic admissions, forbidden from actual helper dependencies.',
 'scope_limits':'Local macOS direct-source helper build, read-only pinned MI22 packages. Not an independent final mathematical approval, Linux run, Comparator result, full RA20 proof or publication.'}
(E/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
