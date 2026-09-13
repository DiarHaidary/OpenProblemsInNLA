#!/usr/bin/env python3
"""LU author evidence audit; direct reads only except the scoped result file."""
from pathlib import Path
import hashlib,json,re,datetime,subprocess
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
PACKAGES=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):return {'sha256':sha(p),'bytes':p.stat().st_size}
F=json.loads((P/'reviews/statement-freeze.json').read_text());assert len(F['files'])==733
for rel,h in F['files'].items():assert sha(P/rel)==h,rel
originals={}
for rel,h in F['source_files'].items():
 b=(P/F['source_snapshot_directory']/rel).read_bytes()
 assert hashlib.sha256(b).hexdigest()==h
 blob=subprocess.check_output(['git','-C','/tmp/nla-lean-ra20-worktree','rev-parse',F['base']+':'+rel],text=True).strip()
 assert blob==F['source_git_blobs'][rel]
 assert subprocess.check_output(['git','-C','/tmp/nla-lean-ra20-worktree','show',F['base']+':'+rel])==b
 originals[rel]={'sha256':h,'git_blob':blob,'bytes':len(b)}
L=json.loads((E/'latest.json').read_text());A=E/L['attempt'];assert sha(A/'result.json')==L['result_sha256']
R=json.loads((A/'result.json').read_text());assert R['pass'] and len(R['commands'])==4
for rel,d in R['inputs'].items():assert sha(P/rel)==d['sha256'],rel
logs={}
for c in R['commands']:
 assert c['exit_code']==0 and sha(A/c['log'])==c['log_sha256']
 logs[c['source']]=(A/c['log']).read_text()
assert R['pins_before']==R['pins_after'] and len(R['pins_after'])==10
for pin in R['pins_after']:
 q=PACKAGES/pin['name']
 assert subprocess.check_output(['git','-C',str(q),'rev-parse','HEAD'],text=True).strip()==pin['rev']
 assert not subprocess.check_output(['git','-C',str(q),'status','--porcelain','--untracked-files=no'],text=True)
I=logs['verification/lu-development/Inspect.lean']
assert len(re.findall(r'^EXACT_FROZEN_TYPE ',I,re.M))==1
assert len(re.findall(r'^ACTUAL_AXIOMS ',I,re.M))==42
assert len(re.findall(r'^PROJECT_EDGE ',I,re.M))==42
assert len(re.findall(r'^RETAINED_DEPENDENCY ',I,re.M))==29
assert 'PROJECT_COUNTS declarations=42, required=29' in I
for atoms in re.findall(r'^ACTUAL_AXIOMS .*?: \[([^\]]*)\]',I,re.M):
 assert set(filter(None,atoms.split(', ')))<={'propext','Classical.choice','Quot.sound'}
reports={k:len(re.findall(r"depends on axioms: \[propext, Classical.choice, Quot.sound\]",v))for k,v in logs.items()}
assert list(reports.values())==[0,5,9,9]
assert all(not re.search(r'^.*:\d+:\d+: error:',s,re.M)for s in logs.values())
assert all(not re.search(r'^.*:\d+:\d+: warning:',s,re.M)for k,s in logs.items()if k!='verification/lu-development/Inspect.lean')
warning_count=len(re.findall(r'^.*:\d+:\d+: warning:',I,re.M))
# No diagnostic assumptions are imported into the actual proof module.
S=(P/'NLA/IE05/LUTrajectory.lean').read_text()
assert sha(P/'NLA/IE05/LUTrajectory.lean')=='96d71b7a46ec692f9e84e6450adacfa71b9c79ef69ff17222e44173f3e6abcbb'
# This module has only ordinary non-nested comments; remove them before token checks.
code=re.sub(r'/\-.*?\-/','',S,flags=re.S);code=re.sub(r'--[^\n]*','',code)
assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|partial)\b',code)
assert not re.search(r'^import .*Challenge',code,re.M)
X=json.loads((E/'expected-type-extraction.json').read_text())
assert X['exact_header']==re.search(r'^theorem scaledLU_trajectory\b(.*?) := by sorry$',(P/'Challenge.lean').read_text(),re.M|re.S).group(1)
assert X['inspector_sha256']==sha(E/'Inspect.lean')
imports=[]
for rel,base,expected in [('verification/gepp-development/EVIDENCE-MANIFEST.json',P,150),('verification/qr-scaling-handoff/EVIDENCE-MANIFEST.json',P/'verification/qr-scaling-handoff',847)]:
 M=json.loads((P/rel).read_text());assert len(M['files'])==expected
 for name,d in M['files'].items():assert sha(base/name)==d['sha256'],name
 imports.append({'manifest':rel,'sha256':sha(P/rel),'verified_bound_files':expected})
attempts={}
for a in sorted(E.glob('attempt-*')):
 r=json.loads((a/'result.json').read_text());assert r['own_prefix_removed'] and not Path(r['prefix']).exists()
 for rel,d in r['inputs'].items():assert sha(a/'source'/rel)==d['sha256']
 for c in r['commands']:assert sha(a/c['log'])==c['log_sha256']
 attempts[a.name]={'pass':r['pass'],'result':record(a/'result.json'),'commands':[(c['source'],c['exit_code'])for c in r['commands']]}
assert len(attempts)==3
api_paths=['Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean','Mathlib/Analysis/Real/Sqrt.lean','Mathlib/Data/List/MinMax.lean','Mathlib/Data/List/FinRange.lean']
api={rel:record(PACKAGES/'mathlib'/rel)for rel in api_paths}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'scope':'Exact generic LU helper author validation, not complete IE05/final review/Linux verification','source':record(P/'NLA/IE05/LUTrajectory.lean'),'selected_attempt':A.name,'selected_result':record(A/'result.json'),'total_seconds':sum(c['elapsed_seconds']for c in R['commands']),'platform':R['platform'],'toolchain':R['toolchain_version'],'exact_contracts':1,'safe_actual_project_declarations':42,'material_dependencies':29,'kernel_assertions':23,'standard_three_reports':reports,'mathematical_warnings':0,'expected_type_unused_binder_warnings':warning_count,'preserved_statement_files':733,'originals':originals,'prior_complete_handoffs':imports,'clean_pins':R['pins_after'],'primary_API_sources':api,'attempts':attempts,'all_own_generated_prefixes_hashed_and_removed':True,'independent_review':False,'actual_linux_comparator':False,'canonical_status_or_git_changes':False}
(E/'audit-result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k]for k in ['pass','selected_attempt','total_seconds','safe_actual_project_declarations','material_dependencies','kernel_assertions','expected_type_unused_binder_warnings']}))
