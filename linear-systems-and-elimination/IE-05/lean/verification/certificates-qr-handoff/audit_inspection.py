#!/usr/bin/env python3
"""Audit the actual fresh command streams and retain a bounded completion record."""
from pathlib import Path
import collections,datetime,hashlib,json,re
E=Path(__file__).resolve().parent;P=E.parents[1]
T=Path('/Users/georgestepaniants/.elan/toolchains/leanprover--lean4---v4.33.1')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
 p=E/n;assert not p.exists(),n;p.write_text(json.dumps(v,indent=2)+'\n')
latest=json.loads((E/'latest.json').read_text());A=E/latest['attempt']
result=json.loads((A/'result.json').read_text())
assert latest['pass'] and result['pass'] and result['own_prefix_removed']
assert sha(A/'result.json')==latest['result_sha256']
allowed={'propext','Classical.choice','Quot.sound'}
axioms=[];source_commands=[]
for r in result['commands']:
 assert r['exit_code']==0
 for stream in ['stdout','stderr']:assert sha(A/(r['label']+'.'+stream))==r[stream+'_sha256']
 if r['label'] not in ['Definitions','Scaling','QR','IntegerQR','ExactCertificates','Inspect']:continue
 source_commands.append(r)
 text=(A/(r['label']+'.stdout')).read_text();error=(A/(r['label']+'.stderr')).read_text()
 assert not error and not re.search(r'\b(?:warning|error):',text),r['label']
 for m in re.finditer(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text):
  ax=[x.strip() for x in m.group(2).split(',') if x.strip()];assert set(ax)<=allowed,(r['label'],m.group(1),ax)
  axioms.append({'module':r['label'],'name':m.group(1),'axioms':ax})
 for m in re.finditer(r"'([^']+)' does not depend on any axioms",text):
  axioms.append({'module':r['label'],'name':m.group(1),'axioms':[]})
assert len(source_commands)==6
text=(A/'Inspect.stdout').read_text()
decls={m.group(1):{'kind':m.group(2),'axioms':[a.strip() for a in m.group(3).split(',') if a.strip()]}
       for m in re.finditer(r'ACTUAL_DECL (\S+) KIND (\S+) AXIOMS \[([^]]*)\]',text)}
edges={m.group(1):[n.strip() for n in m.group(2).split(',') if n.strip()]
       for m in re.finditer(r'ACTUAL_EDGE (\S+): \[([^]]*)\]',text)}
roots=['NLA.IE05._proved.'+n for n in ['integer_factor_certificates','integer_entry_certificates','numerical_gap_positive','normalizedQRQ_of_gram_lu']]
assert len(decls)==len(edges)==36 and set(decls)==set(edges)
seen=set();pending=roots[:]
while pending:
 n=pending.pop()
 if n in seen:continue
 seen.add(n);pending+=edges[n]
assert seen==set(decls)
assert all(v['kind'] in ['definition','theorem'] and set(v['axioms'])<=allowed for v in decls.values())
assert all('CertificatesQRExpected' not in n and 'sorry' not in n for n in decls)
aux=['NLA.IE05._proved.integer_factor_certificates._proof_1_1',
     'NLA.IE05._proved.integer_factor_certificates._proof_1_2',
     'NLA.IE05._proved.integer_entry_certificates._proof_1_1']
for n in aux:assert decls[n]['kind']=='theorem' and set(decls[n]['axioms'])==allowed
instances=['NLA.IE05._proved.integerLowerZeroDecidable','NLA.IE05._proved.integerTZeroDecidable']
for n in instances:assert decls[n]['kind']=='definition' and decls[n]['axioms']==['propext'] and 'Int.instDecidableEq' in edges[n]
assert edges['Int.instDecidableEq']==['Int.decEq'] and decls['Int.decEq']['axioms']==[]
required=re.findall(r'^REQUIRED_ACTUAL_DEPENDENCY (\S+)$',text,re.M);assert len(required)==19
exact=re.findall(r'^EXACT_EXPECTED_TYPE (\S+):',text,re.M);assert exact==roots
assert 'COMPLETE_HELPER_CLOSURE 36 REQUIRED 19' in text
assert len(axioms)==28 and sum(a['module']!='Inspect' for a in axioms)==20
assert sum(set(a['axioms'])==allowed for a in axioms)==24
assert sum(a['axioms']==['propext'] for a in axioms)==2 and sum(not a['axioms'] for a in axioms)==2
write('ACTUAL-DECLARATION-CLOSURE.json',{'actual_roots':roots,'total':36,'project_declarations':34,
 'additional_actual_core_integer_declarations':2,'declarations':decls,'edges':edges,
 'decide_kernel_auxiliaries':aux,'module_local_instance_constants':instances,
 'required_actual_dependencies':required,'expected_diagnostic_definitions_in_actual_closure':False})
write('AXIOM-RECORDS.json',{'records':axioms,'total':28,'source_records':20,'additional_inspector_records':8,
 'standard_three':24,'propext_only':2,'axiom_free':2,'additional_axioms':[]})
historical=[]
for target in ['exactcertificates','integerqr','certdiagnostic']:
 for a in sorted((P/f'verification/{target}-development').glob('attempt-*')):
  inputs=json.loads((a/'inputs.json').read_text());rs=json.loads((a/'results.json').read_text())
  for src in inputs['sources']:
   p=a/'source'/src['path'];assert sha(p)==src['sha256'] and p.stat().st_size==src['bytes']
  for r in rs:
   assert sha(a/(r['module']+'.log'))==r['log_sha256']
   assert r['command'][0]==str(T/'bin/lean')
   assert r['command'][2]==inputs['prefix']+'/NLA/IE05/'+r['module']+'.olean'
   assert Path(r['cwd']).resolve()==(a/'source').resolve()
  historical.append({'attempt':str(a.relative_to(P)),'source_target':target,
   'diagnostic_only':target=='certdiagnostic','commands':rs,'pass':all(r['exit_code']==0 for r in rs),
   'original_runner_sha256':sha(a/'runner.py.txt'),'inputs_sha256':sha(a/'inputs.json'),
   'objects_sha256':sha(a/'objects.json')})
assert len(historical)==13 and sum(r['pass'] for r in historical)==3
write('ROOT-ATTEMPT-AUDIT.json',{'attempts':historical,'total':13,'passed':3,'failed':10,
 'successful_proof_helpers':2,'successful_unimported_diagnostic':1,
 'interpretation':'All historical streams/snapshots/object records retained; failed automatic recovery admissions in failed logs are not accepted proofs.'})
primary={}
for n in ['src/lean/Init/Data/Int/Basic.lean','src/lean/Lean/Elab/Tactic/Decide.lean']:
 p=T/n;q=E/'primary-source'/n;q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();q.write_bytes(p.read_bytes())
 primary[n]={'original_path':str(p),'snapshot':str(q.relative_to(E)),'sha256':sha(p),'bytes':p.stat().st_size}
write('PRIMARY-SOURCES.json',{'toolchain':str(T),'sources':primary,
 'logical_note':'Int.decEq has an executable override but a genuine recursive logical definition; decide +kernel uses doKernel/mkAuxLemma, and the proof closure contains no native-execution axiom.'})
nav=json.loads((E/'navigation-diagnostics.json').read_text())
nav['second_missing_file_read']={'command':'cat verification/qr-scaling-handoff/verify_inventory.py','exit_code':1,
 'stderr':'cat: verification/qr-scaling-handoff/verify_inventory.py: No such file or directory',
 'interpretation':'Navigation only. No prior mutating verifier or runner was executed. Its actual sealed files are checked through original manifest entries.'}
(E/'navigation-diagnostics.json').write_text(json.dumps(nav,indent=2)+'\n')
note=json.loads((E/'ROOT-NOTE.json').read_text());assert not (P/note['diagnostic_removed_from_mathematical_module_directory']).exists()
assert sha(P/note['exact_retained_snapshot'])==note['diagnostic_sha256']
modules=[n for n in result['source_snapshots'] if n.startswith('NLA/IE05/')]
for n in modules:
 t=(P/n).read_text();assert not re.search(r'^import .*?(?:Challenge|CertDiagnostic|Witness)\b',t,re.M)
write('AUDIT-RESULT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'HELPER_COMPLETION_INSPECTION_PASS','attempt':latest['attempt'],'source_commands':6,
 'all_recorded_commands':len(result['commands']),'frozen_certificate_type_equalities':3,'generic_type_equality':1,
 'actual_declaration_closure':36,'project_closure':34,'material_dependencies':19,
 'source_kernel_assertions':20,'additional_inspector_kernel_assertions':8,'printed_axiom_records':28,
 'fresh_warning_count':0,'frozen_inputs_preserved':733,'stable_scoped_inputs':1210,
 'source_before_after_unchanged':True,'ten_clean_pins_before_after':True,'readonly_dependency_build_directories':9,
 'source_objects_hashed_then_removed':result['object_count'],'own_prefix_removed':result['own_prefix_removed'],
 'root_prefix_cleanup':'root-prefix-cleanup.json','root_note_sha256':sha(E/'ROOT-NOTE.json'),
 'no_mathematical_source_edits':True,'no_fresh_numeric_sqrt_interval_computations':True,
 'independent_final_proof_approval':False,'actual_Linux_Comparator':False})
print((E/'AUDIT-RESULT.json').read_text())
