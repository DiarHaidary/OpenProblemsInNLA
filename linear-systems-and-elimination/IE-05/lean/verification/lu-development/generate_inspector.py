#!/usr/bin/env python3
"""Admission-free frozen-type and actual closure inspector for the LU helper.
Uses the already sealed GEPP inspection mechanics, adapted to this exact root.
"""
from pathlib import Path
import re,hashlib,json
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
C=(P/'Challenge.lean').read_text();assert hashlib.sha256(C.encode()).hexdigest()=='0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e'
header=re.search(r'^theorem scaledLU_trajectory\b(.*?) := by sorry$',C,re.M|re.S).group(1)
binders,conclusion=header.split(' :\n',1)
base=(P/'verification/gepp-development/Inspect.lean').read_text()
assert hashlib.sha256(base.encode()).hexdigest()=='7ebe5d8839736904ab897c305345cebd6382587c6ee29f135addc15a7e355df3'
body=base[base.index('open Lean Elab Command in\nrun_cmd do'):base.index('\n#assert_trust kernel NLA.IE05.entryMax_semantics_proved')]
start=body.index('  let pairs := [');end=body.index('  for (actual, reference)',start)
body=body[:start]+'''  let pairs := [(``NLA.IE05._proved.scaledLU_trajectory,
    ``NLA.IE05.LUExpected.scaledLU_trajectory)]
'''+body[end:]
body=body.replace('NLA.IE05.GEPPExpected.','NLA.IE05.LUExpected.')
roots=['tailProduct_zero','tailProduct_terminal','tailProduct_pivot_row','tailProduct_pivot_column','tailProduct_split','scaled_tail_schur','scaled_tail_firstAvailable','scaled_noSwap_trajectory','scaledLU_trajectory']
body=body.replace('  let mut pending := pairs.map Prod.fst', '  let mut pending := ['+', '.join('``NLA.IE05._proved.'+n for n in roots)+']')
req=['NLA.IE05._proved.'+n for n in roots if n not in ['tailProduct_terminal','scaledLU_trajectory']]
req+=['NLA.IE05.'+n for n in ['firstPath_eq_of_firstAvailable_proved','firstPivotIndex_eq_of_firstAvailable_proved','firstPivotIndex_spec_proved','tailProduct','scaledColumns','UnitLower','UpperTriangular','AdmissiblePivot','FirstAvailablePivot','FirstAvailablePath','noSwapPath','trajectory','firstPath','rowSwap','schurStep']]
req+=['Real.sqrt','Real.sqrt_pos','Finset.sum_eq_single','Finset.sum_congr','Finset.sum_add_distrib','List.argmax','List.index_of_argmax']
start=body.index('  let required := [');end=body.index('  for need in required',start)
body=body[:start]+'  let required := ['+',\n    '.join('``'+n for n in req)+']\n'+body[end:]
s='''/- LU helper author diagnostic, not an independent referee or Linux Comparator.
Expected contract is an admission-free Prop definition from the frozen header. -/
import NLA.IE05.LUTrajectory
import Lean.Util.FoldConsts
set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.LUExpected
def scaledLU_trajectory : Prop :=
  ∀'''+binders+',\n'+conclusion+'''
end NLA.IE05.LUExpected

'''+body+'\n'
for n in roots:s+='#assert_trust kernel NLA.IE05._proved.'+n+'\n#print axioms NLA.IE05._proved.'+n+'\n'
for n in ['UnitLower','UpperTriangular','tailProduct','scaledColumns','noSwapPath','schurStep']:
 s+='set_option pp.all true in\n#print NLA.IE05.'+n+'\n'
for n in ['scaled_tail_schur','scaled_tail_firstAvailable','scaled_noSwap_trajectory','scaledLU_trajectory']:
 s+='set_option pp.proofs true in\n#print NLA.IE05._proved.'+n+'\n'
(E/'Inspect.lean').write_text(s)
(E/'expected-type-extraction.json').write_text(json.dumps({'frozen_challenge_sha256':hashlib.sha256(C.encode()).hexdigest(),'exact_header':header,'expected_definition_contains_no_proof':True,'actual_roots':['NLA.IE05._proved.'+n for n in roots],'required_material_dependencies':req,'inspector_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2)+'\n')
print(hashlib.sha256(s.encode()).hexdigest())
