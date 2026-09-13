from pathlib import Path
import hashlib, json, re
from collections import deque

OWN=Path(__file__).resolve().parent; ROOT=OWN.parents[1]
d=json.loads((OWN/'inspection-001/run-003/actual-environment.json').read_text())
inventory=json.loads((OWN/'inspection-001/all-project-declarations.json').read_text())
g={x['name']:x for x in d['transitive_graph']}
assert len(g)==d['transitive_count'] and len(d['contracts'])==17
assert d['project_declaration_count']==184 and len(d['source_seed_names'])==157
assert all(not x['unsafe'] and not x['partial'] for x in g.values())
allowed={'propext','Classical.choice','Quot.sound'}
assert {n for n,x in g.items() if x['kind']=='axiom'}<=allowed
assert all(set(x['axioms'])<=allowed for x in d['project_declarations'])
assert all(n in g for row in g.values() for n in row['all_references'])
assert all(x['definitional_equality'] for x in d['contracts'])
assert not any('Challenge' in x for x in d['imported_modules'])
assert not any('Referee' in x for x in g)
assert all(g[x['name']]['kind']=='theorem' for x in d['contracts'])

def closure(seeds,field='all_references'):
    seen=set(); q=list(seeds)
    while q:
        n=q.pop()
        if n in seen: continue
        seen.add(n); q.extend(g[n][field])
    return seen
root_names=[x['name'] for x in d['contracts']]
contract_closure=closure(root_names)
assert len(contract_closure)==29594
project_contract=sorted(n for n in contract_closure if g[n]['module'].startswith('NLA.IE05.'))
assert len(project_contract)==181
extras=[x for x in inventory if x['name'] not in g]
assert len(extras)==42
assert {x['name'] for x in extras if x['partial']}=={'NLA.IE05.trajectory._unsafe_rec','NLA.IE05.firstTrajectory._unsafe_rec'}
assert not any(x['unsafe'] for x in extras)
assert set(d['source_seed_names'])<=set(g)

def path(a,b):
    queue=deque([[a]]); seen=set()
    while queue:
        p=queue.popleft(); n=p[-1]
        if n==b: return p
        if n in seen: continue
        seen.add(n)
        for child in g[n]['body_references']: queue.append(p+[child])
    raise AssertionError(('missing actual body dependency',a,b))

prefix='NLA.IE05.'; proved=prefix+'_proved.'
requirements={
 prefix+'orthogonalExtremizerConjecture':[proved+'supremum_strict_gap',proved+'witness_strict_growth',proved+'numerical_gap_positive',proved+'integer_entry_certificates',proved+'integer_factor_certificates'],
 proved+'supremum_strict_gap':['le_csSup',prefix+'orthogonalGrowthSet_bounded_proved',proved+'witness_orthogonal_path'],
 prefix+'firstPath_semantics':[prefix+'activeInjective_schur_proved',prefix+'activeInjective_nonzero_column_proved',prefix+'firstPivotIndex_spec_proved'],
 prefix+'candidate_positiveQR':[proved+'normalizedQRQ_positiveQR',proved+'normalizedQRQ_eq_of_positiveQR','InnerProductSpace.gramSchmidtNormed_orthonormal','InnerProductSpace.gramSchmidt_ne_zero'],
 prefix+'canonical_integer_identification':[proved+'normalizedQRQ_of_gram_lu',proved+'normalizedQRQ_eq_of_positiveQR',proved+'real_factor_certificates'],
 prefix+'scaledLU_trajectory':[proved+'scaled_tail_schur',proved+'scaled_tail_firstAvailable',prefix+'firstPath_eq_of_firstAvailable_proved'],
 prefix+'bounded_growth_data':[proved+'witness_final_pivot',proved+'candidate_peak_upper',proved+'castIntegerMatrix_tailProduct',proved+'abs_div_sqrt_le',proved+'abs_div_sqrt_le_sqrt'],
}
paths=[{'from':a,'to':b,'body_path':path(a,b)} for a,targets in requirements.items() for b in targets]
assertions=[]
for f in sorted((ROOT/'NLA/IE05').glob('*.lean')):
    ns=re.search(r'^namespace (\S+)',f.read_text(),re.M)[1]
    for line,s in enumerate(f.read_text().splitlines(),1):
        m=re.match(r'#assert_trust kernel (\S+)',s)
        if m:
            n=m[1] if m[1].startswith('NLA.') else ns+'.'+m[1]
            assertions.append({'file':str(f.relative_to(ROOT)),'line':line,'name':n,'kind':'kernel'})
assert len(assertions)==89
assert all(a['name'] in g for a in assertions)
checks=re.findall(r'^#assert_trust kernel (\S+)',(OWN/'inspection-001/run-003/RefereeInspect.lean').read_text(),re.M)
assert len(checks)==17 and set(checks)==set(root_names)
for cmd in (OWN/'attempt-001/commands').iterdir():
    result=json.loads((cmd/'result.json').read_text()); assert result['exit_code']==0
    text=(cmd/'stdout').read_text()+(cmd/'stderr').read_text()
    assert not re.search(r'\berror:|declaration uses .sorry.|declaration uses .admit.',text)
assert (ROOT/'Solution.lean').read_text()=='import NLA.IE05.Proof\n'
report={'status':'PASS','types':17,'source_math_declarations':157,'source_math_closure_project':184,
        'source_math_transitive_declarations':29597,'export_closure_project':181,
        'export_transitive_declarations':29594,'allowed_axioms':sorted(allowed),
        'all_project_environment_inventory':len(inventory),'exact_outside_body_closure':extras,
        'outside_closure_explanation':'These exact 42 generated environment declarations are absent from the type/body dependency graph of every source mathematical declaration; no name/basename trust exception is applied.',
        'material_body_paths':paths,'source_kernel_assertions':assertions,'additional_inspector_kernel_assertions':checks,
        'total_executed_kernel_assertions_final_success':106,
        'project_contract_closure':project_contract,'complete_environment_sha256':hashlib.sha256((OWN/'inspection-001/run-003/actual-environment.json').read_bytes()).hexdigest()}
(OWN/'audit-result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('Independent actual-environment PASS: 17 types; 181 project / 29594 total export closure; all 157 source declarations covered; 106 successful kernel assertions; '+str(len(paths))+' material body paths')
