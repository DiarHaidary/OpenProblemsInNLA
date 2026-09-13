#!/usr/bin/env python3
"""Validate exact independent outputs and extract readable copies; no Lean execution."""
from pathlib import Path
import hashlib, json, re

E=Path(__file__).resolve().parent
K=E.parent.parent
A=E/'attempt-nglj5yvu'
I=E/'input-audit-039929qi'
sha=lambda b:hashlib.sha256(b).hexdigest()
def row(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
baseline=json.loads((E/'baseline.json').read_text())['files']
assert len(baseline)==168
for p,v in baseline.items():assert row(K/p)==v,p
defs=re.findall(r'^(?:def|abbrev) (\w+)',(K/'NLA/KE04/Definitions.lean').read_text(),re.M)
targets=['NLA.KE04.'+n for n in re.findall(r'^theorem (\w+)',(K/'Challenge.lean').read_text(),re.M)]
assert len(defs)==27 and len(targets)==24
r=json.loads((A/'result.json').read_text())
assert r['success'] and r['baseline_before']==r['baseline_after']==168
assert len(r['modules'])==4 and len(r['commands'])==79
assert len(r['private_object_identities'])==4 and r['private_objects_removed']
assert not Path(r['private_output']).exists()
assert r['pins_before']==r['pins_after'] and len(r['pins_before'])==10
for p,v in r['source_identities'].items():assert row(K/p)==v and row(A/'source'/p)==v
for c in r['commands']:
    assert c['exit_code']==0
    assert row(A/c['stdout'])==c['stdout_identity'] and row(A/c['stderr'])==c['stderr_identity']
dt=(A/'command-057-compile-InspectDefinitions.stdout').read_text()
tt=(A/'command-058-compile-InspectContracts.stdout').read_text()
ct=(A/'command-056-compile-Challenge.stdout').read_text()
assert ct.count('warning:')==24 and ct.count('declaration uses `sorry`')==24
assert not (A/'command-055-compile-NLA-KE04-Definitions.stdout').read_bytes()
assert 'warning:' not in dt+tt and 'error:' not in dt+tt
closure=[]
split=lambda s:[x.strip() for x in s.split(',') if x.strip()]
for n,axs,local,imported in re.findall(r'^DEFINITION_CLOSURE (.*?): axioms=\[(.*?)\]; project=\[(.*?)\]; imported=\[(.*?)\]',dt,re.M|re.S):
    entry={'declaration':n,'axioms':split(axs),'project_dependencies':split(local),'imported_dependencies':split(imported)}
    assert set(entry['axioms'])<= {'propext','Classical.choice','Quot.sound'}
    closure.append(entry)
assert len(closure)==33 and len({r['declaration'] for r in closure})==33
assert {f'NLA.KE04.{n}' for n in defs} <= {r['declaration'] for r in closure}
helpers=sorted({r['declaration'] for r in closure}-{f'NLA.KE04.{n}' for n in defs})
assert len(helpers)==6 and all('._proof_' in n for n in helpers)
all_local={r['declaration'] for r in closure}
for item in closure:assert set(item['project_dependencies']) <=all_local
external={n for r in closure for n in r['imported_dependencies']}
material=['EuclideanSpace','Fin.rev','Fin.revPerm','Fintype.linearCombination','Inner.inner','LinearIndependent',
          'LinearMap.IsSymmetric','LinearMap.IsSymmetric.eigenvalues','LinearMap.IsSymmetric.eigenvectorBasis',
          'Matrix.IsHermitian','Matrix.isHermitian_conjTranspose_mul_mul','Matrix.isSymmetric_toEuclideanLin_iff',
          'Matrix.toEuclideanLin','Module.finrank','OrthonormalBasis.reindex','Polynomial.C','Polynomial.X',
          'Submodule.span','finrank_euclideanSpace_fin']
assert set(material)<=external
assert not {'sorryAx','Lean.ofReduceBool','Lean.ofReduceNat','Lean.trustCompiler'} & external
axioms=re.findall(r"^'(NLA\.KE04\.[^']+)' depends on axioms: \[(.*?)\]",dt,re.M|re.S)
assert len(axioms)==27 and {n for n,_ in axioms}=={f'NLA.KE04.{n}' for n in defs}
for _,axs in axioms:assert set(split(axs))=={'propext','Classical.choice','Quot.sound'}
ds=(A/'source/InspectDefinitions.lean').read_text()
assert ds.count('#assert_trust kernel NLA.KE04.')==27
assert 'import Challenge' not in ds and 'import LeanCert.Tactic.Verification' in ds
assert 'set_option leancert.trust "kernel"' in ds
admitted=re.findall(r'^CONTRACT_ADMITTED ([^:]+): \[(.*?)\]',tt,re.M|re.S)
assert len(admitted)==24 and {n for n,_ in admitted}==set(targets)
for _,axs in admitted:assert 'sorryAx' in split(axs)
direct=re.findall(r'^CONTRACT_TYPE_DIRECT ([^:]+): \[(.*?)\]',tt,re.M|re.S)
assert len(direct)==24 and {n for n,_ in direct}==set(targets)
for n,dep in direct:
    assert not set(split(dep)) & set(targets),n
readable_types=tt[tt.rfind('@NLA.KE04.real_matrix_semantics'):]
readable_defs=dt[dt.rfind('def NLA.KE04.Vec'):]
assert len(re.findall(r'^@?NLA\.KE04\.\w+ :',readable_types,re.M))==24
assert len(re.findall(r'^(?:@\[reducible\] )?def NLA\.KE04\.\w+ :',readable_defs,re.M))==27
(E/'actual-contract-types.txt').write_text(readable_types)
(E/'actual-definition-values.txt').write_text(readable_defs)
write(E/'actual-definition-closure.json',closure)
write(E/'actual-contract-type-dependencies.json',[{'declaration':n,'direct_dependencies':split(v)} for n,v in direct])
ia=json.loads((I/'result.json').read_text());assert ia['success'] and len(ia['commands'])==56
assert len(ia['api_files'])==33 and len(ia['tauceti_7_git_trees'])==7
for c in ia['commands']:
    assert c['exit_code'] in [0,1]
    assert row(I/c['stdout'])==c['stdout_identity'] and row(I/c['stderr'])==c['stderr_identity']
additional=json.loads((E/'additional-api/result.json').read_text());assert additional['success'] and len(additional['files'])==3
attempts=[]
command_count=0; object_count=0; outcomes={}
for folder in sorted(E.iterdir()):
    if folder.is_dir() and (folder/'result.json').is_file() and (folder.name.startswith('attempt-') or folder.name.startswith('input-audit')):
        data=json.loads((folder/'result.json').read_text())
        count=len(data['commands']);command_count+=count
        object_count+=len(data.get('private_object_identities',{}))
        for cmd in data['commands']:
            key=str(cmd['exit_code']);outcomes[key]=outcomes.get(key,0)+1
        attempts.append({'path':str(folder.relative_to(E)),'success':data['success'],'result':row(folder/'result.json'),'commands':count,'error':data.get('error')})
assert command_count==405 and object_count==10
allfiles={str(p.relative_to(K)) for p in K.rglob('*') if p.is_file()}
unexpected=allfiles-set(baseline)-{str(p.relative_to(K)) for p in E.rglob('*') if p.is_file()}-{'reviews/statement-referee-1.md'}
assert not unexpected,unexpected
# All original public source bytes are kept; do not add George's contact email.
email=re.compile(rb'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
for p in K.rglob('*'):
    if p.is_file():
        for hit in email.findall(p.read_bytes()):
            assert b'stepaniants' not in hit.lower(),str(p.relative_to(K))
result={'verdict':'APPROVE','phase':'independent statement review only','reviewer':'/root/ra20_final_referee2',
        'definitions':27,'definition_closure':33,'generated_helpers':helpers,'material_imports_confirmed':material,
        'kernel_trust_commands':27,'printed_definition_axiom_reports':27,'contracts':24,'challenge_admissions':24,
        'independently_compiled_modules':4,'accepted_attempt':str(A.relative_to(K)),'accepted_attempt_result':row(A/'result.json'),
        'accepted_provenance_audit':str(I.relative_to(K)),'accepted_provenance_result':row(I/'result.json'),
        'all_attempts':attempts,'recorded_child_commands':408,'main_attempt_child_commands':command_count,
        'additional_source_git_commands':3,'main_attempt_exit_code_counts':outcomes,'own_objects_hashed_and_removed':object_count,
        'original_inputs_unchanged':168,'original_git_sources':17,'api_sources_git_or_archive_bound':36,
        'all_actual_27_values_and_24_types_read':True,'source_proof_unchanged_from_original_submission':True,
        'source_definitions_or_contracts_changed':False,'proof_implemented':False,'statement_frozen':False,
        'linux_comparator_run':False,'raw_default_kernel_run':False,'second_approval_and_root_acceptance_still_required':True}
write(E/'RESULT.json',result)
print(json.dumps({k:result[k] for k in ['verdict','definitions','definition_closure','contracts','kernel_trust_commands','recorded_child_commands','own_objects_hashed_and_removed','original_inputs_unchanged']},indent=2))
