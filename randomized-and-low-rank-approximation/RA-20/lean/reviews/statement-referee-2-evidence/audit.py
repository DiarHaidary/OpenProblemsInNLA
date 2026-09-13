"""Independent RA20 final statement/source/attempt inventory review. Read-only inputs.
No author's PASS is accepted without its actual hashes, result codes and logs.
"""
from pathlib import Path
import datetime,hashlib,json,re,subprocess
E=Path(__file__).resolve().parent;P=E.parents[1]
W=Path('/Users/georgestepaniants/Research/OpenProblemsInNLA')
C=Path('/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
f=json.loads((P/'reviews/statement-freeze.json').read_text());outer=json.loads((P/'reviews/statement-package-manifest.json').read_text())
assert len(f['files'])==68 and len(outer['files'])==70
for n,h in f['files'].items():assert sha(P/n)==h,n
for n,r in outer['files'].items():assert sha(P/n)==r['sha256'] and (P/n).stat().st_size==r['bytes'],n
source=json.loads((P/'verification/original-source-inventory.json').read_text())
for n,r in source['files'].items():
 raw=subprocess.check_output(['git','show',source['base']+':'+n],cwd=W)
 assert hashlib.sha256(raw).hexdigest()==r['sha256'] and (P/r['snapshot']).read_bytes()==raw,n
 assert subprocess.check_output(['git','rev-parse',source['base']+':'+n],cwd=W).decode().strip()==r['git_blob'],n
assert len(source['files'])==16
cfg=json.loads((P/'comparator.json').read_text())
names=re.findall(r'^theorem\s+(\w+)',(P/'Challenge.lean').read_text(),re.M)
assert cfg['theorem_names']==['NLA.RA20.'+n for n in names] and len(names)==12
assert cfg['definition_names']==[] and cfg['permitted_axioms']==['propext','Classical.choice','Quot.sound']
assert (P/'Challenge.lean').read_text().count('\n  sorry')==12
assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe)\b',(P/'NLA/RA20/Definitions.lean').read_text())
assert not (P/'Solution.lean').exists() and not list((P/'NLA').rglob('Proof.lean'))
attempts=[]
for path in sorted((P/'verification/statement-checks').glob('attempt-*/result.json')):
 r=json.loads(path.read_text());rows=[]
 for cmd in r['commands']:
  log=path.parent/cmd['log'];assert sha(log)==cmd['log_sha256'];text=log.read_text()
  snap=path.parent/(cmd['source'].replace('/','-')+'.txt');assert sha(snap)==cmd['source_sha256']
  rows.append({'source':cmd['source'],'actual_exit_code':cmd['exit_code'],'source_snapshot_sha256':sha(snap),
   'log_sha256':sha(log),'errors':[s for s in text.splitlines() if ': error' in s],
   'warning_count':text.count('warning:'),'standard_axiom_lines':[s for s in text.splitlines() if 'depends on axioms:' in s]})
 attempts.append({'result':str(path.relative_to(P)),'sha256':sha(path),'stored_state':r.get('result'),
                  'actual_commands':rows})
assert len(attempts)==4 and sum(all(c['actual_exit_code']==0 for c in a['actual_commands']) for a in attempts)==2
fresh=json.loads((E/'latest.json').read_text());res=Path(fresh['attempt'])/'result.json';r=json.loads(res.read_text())
assert sha(res)==fresh['result_sha256'] and r['verdict']=='PASS' and len(r['commands'])==3
for c in r['commands']:
 assert c['exit_code']==0 and sha(P/c['source'])==c['source_sha256']
 assert sha(res.parent/c['log'])==c['log_sha256']
inspect=res.parent/r['commands'][2]['log'];txt=inspect.read_text()
assert 'INSPECTED_TARGET_DEFINITIONS: 19' in txt
assert len(re.findall(r'^REQUIRED_DEFINITION:',txt,re.M))==14
assert len(re.findall('depends on axioms:',txt))==19 and txt.count('does not depend on any axioms')==1
apis=json.loads((P/'verification/primary-library-inventory.json').read_text())['files']
for name in ['mathlib/Mathlib/Analysis/Calculus/FDeriv/Defs.lean',
             'mathlib/Mathlib/RingTheory/Smooth/Basic.lean','mathlib/Mathlib/Topology/Instances/Matrix.lean']:
 package,rel=name.split('/',1);rev='0df444a360eaa60ab8c11dca51a86af692955474';file=C/package/rel
 apis[name]={'package_rev':rev,'sha256':sha(file),'bytes':file.stat().st_size,
            'git_blob':subprocess.check_output(['git','rev-parse',rev+':'+rel],cwd=C/package).decode().strip()}
for name,row in apis.items():
 package,rel=name.split('/',1);file=C/package/rel
 raw=subprocess.check_output(['git','show',row['package_rev']+':'+rel],cwd=C/package)
 assert file.read_bytes()==raw and sha(file)==row['sha256']
assert json.loads((E/'reconstruction.json').read_text())['verdict']=='PASS independent exact reconstruction'
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS independent statement evidence audit',
 'reviewer':'/root/leancert_examples, AI agent; no RA20 mathematical/design contribution',
 'frozen68_preserved':True,'author_package70_plus_outer_preserved':True,'original16_Git_sources_preserved':True,
 'freeze_sha256':sha(P/'reviews/statement-freeze.json'),'package_sha256':sha(P/'reviews/statement-package-manifest.json'),
 'handoff_sha256':sha(P/'reviews/statement-handoff.md'),'exact_comparator_exports':cfg['theorem_names'],
 'original_author_attempts_all_retained_and_inspected':attempts,
 'fresh_result':str(res.relative_to(P)),'fresh_result_sha256':sha(res),'independent_commands':3,
 'definition_kernel_checks':20,'standard_three_reports':19,'axiom_free_reports':1,
 'actual_target_definition_traversal':19,'required_actual_semantic_dependencies':14,
 'primary_library_identity_audit':apis,'ten_clean_pins_before_and_after':r['pins'],
 'independent_reconstruction_sha256':sha(E/'reconstruction.json'),
 'primary_paper_read':{'url':'https://arxiv.org/pdf/2010.15636v2','version':'v2 2022-01-29',
  'sections':'Section 2.2 complex bilinear/smooth/generic definitions; Section 5 Conjecture5.6/Table7 printed page21',
  'access_method':'Actual web open/read during this independent review; no local PDF hash or complete-paper review claim'},
 'reviewer_diagnostic_correction':'Initial own inspector asked for unscoped matrix norm/completeness instances, which this topological-vector-space derivative does not require. Replaced only own diagnostic by actual product topology/Hausdorff/addition/scalar instances. Both independent attempts remain; source and Challenge unchanged.',
 'scope':'Statement approval evidence only; all twelve mathematical contracts remain unproved. Pure kernel LeanCert trust auditing approved; no artificial interval certificate. No worktree, source edit, metadata, status, Git or publication action.'}
(E/'audit.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS 68+16, 70+outer, all4authorattempts,3freshcommands,20definitiontrustchecks')
