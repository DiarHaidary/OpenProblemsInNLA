#!/usr/bin/env python3
"""Witness author's admission-free frozen-type and actual semantic closure check."""
from pathlib import Path
import re,hashlib,json
P=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
C=(P/'Challenge.lean').read_text();assert hashlib.sha256(C.encode()).hexdigest()=='0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e'
contracts=['canonical_integer_identification','witness_orthogonal_path'];headers={};definitions=[]
for n in contracts:
 h=re.search(r'^theorem '+n+r'\b(.*?) := by sorry$',C,re.M|re.S).group(1);headers[n]=h
 binders,conclusion=h.split(' :\n',1);assert not binders.strip()
 definitions.append('def '+n+' : Prop :=\n'+conclusion+'\n')
base=(P/'verification/lu-development/Inspect.lean').read_text()
assert hashlib.sha256(base.encode()).hexdigest()=='376d5329b1721614133b70e73c364d7788ea12b0a2de2d6722afd9c7d3b3d691'
body=base[base.index('open Lean Elab Command in\nrun_cmd do'):base.index('\n#assert_trust kernel NLA.IE05._proved.tailProduct_zero')]
a=body.index('  let pairs := [');b=body.index('  for (actual, reference)',a)
body=body[:a]+'  let pairs := ['+',\n    '.join('(``NLA.IE05._proved.'+n+', ``NLA.IE05.WitnessExpected.'+n+')'for n in contracts)+']\n'+body[b:]
body=body.replace('NLA.IE05.LUExpected.','NLA.IE05.WitnessExpected.')
roots=['castIntegerMatrix_transpose','castIntegerMatrix_mul','castIntegerMatrix_diagonal','castIntegerMatrix_tailProduct','castIntegerMatrix_unitLower','castIntegerMatrix_upper','castIntegerMatrix_lower_bound','real_factor_certificates','normalizedInteger_orthogonal','normalizedInteger_path_trajectory','normalizedInteger_trajectory_entry','normalizedInteger_firstGrowth','integerLower_false_prescribed']+contracts
start=body.index('  let mut pending := [');end=body.index('\n  let mut seen',start)
body=body[:start]+'  let mut pending := ['+', '.join('``NLA.IE05._proved.'+n for n in roots)+']'+body[end:]
req=['NLA.IE05._proved.'+n for n in ['castIntegerMatrix_transpose','castIntegerMatrix_mul','castIntegerMatrix_diagonal','castIntegerMatrix_tailProduct','castIntegerMatrix_unitLower','castIntegerMatrix_upper','castIntegerMatrix_lower_bound','real_factor_certificates','normalizedInteger_orthogonal','normalizedInteger_path_trajectory','integerLower_false_prescribed','integer_factor_certificates','integerLowerZeroDecidable','integerTZeroDecidable','normalizedQRQ_of_gram_lu','normalizedQRQ_eq_of_positiveQR','gramSchmidt_eq_of_positiveQR','scaledColumns_orthogonal','scaledLU_trajectory','scaled_noSwap_trajectory','scaled_tail_schur','scaled_tail_firstAvailable']]
req+=['NLA.IE05.'+n for n in ['firstPath_eq_of_firstAvailable_proved','candidateQ','prescribedLower','normalizedQRQ','euclideanColumns','PositiveQR','Orthogonal','castIntegerMatrix','integerH','integerT','integerD','integerLower','witnessQ','normalizedInteger','tailProduct','scaledColumns','growth','firstGrowth','noSwapPath','trajectory','rowSwap','schurStep','firstPath','FirstAvailablePath','FirstAvailablePivot','AdmissiblePath','AdmissiblePivot']]
req+=['of_decide_eq_true','Int.instDecidableEq','InnerProductSpace.gramSchmidtNormed','Real.sqrt','Matrix.mul_nonsing_inv','Matrix.invertibleOfIsUnitDet','Matrix.det_of_isUpperTriangular','Matrix.blockTriangular_inv_of_blockTriangular']
a=body.index('  let required := [');b=body.index('  for need in required',a)
body=body[:a]+'  let required := ['+',\n    '.join('``'+n for n in req)+']\n'+body[b:]
body=body.replace('  for need in required do\n    unless used.contains need do throwError "Missing material dependency {need}"\n    logInfo m!"RETAINED_DEPENDENCY {need}"\n', '  let mut missing : List Name := []\n  for need in required do\n    if used.contains need then\n      logInfo m!"RETAINED_DEPENDENCY {need}"\n    else\n      missing := need :: missing\n  unless missing.isEmpty do throwError "Missing material dependencies {missing}"\n')
s='''/- Witness author inspection only; expected types are Prop definitions from
exact frozen headers, never reference proofs or assumptions. -/
import NLA.IE05.Witness
import Lean.Util.FoldConsts
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.WitnessExpected
'''+ '\n'.join(definitions)+'''end NLA.IE05.WitnessExpected

'''+body+'\n'
for n in roots:s+='#assert_trust kernel NLA.IE05._proved.'+n+'\n#print axioms NLA.IE05._proved.'+n+'\n'
for n in ['normalizedQRQ','euclideanColumns','castIntegerMatrix','normalizedInteger','witnessQ']:
 s+='set_option pp.all true in\n#print NLA.IE05.'+n+'\n'
for n in ['real_factor_certificates','normalizedInteger_path_trajectory','normalizedInteger_trajectory_entry','canonical_integer_identification','witness_orthogonal_path']:
 s+='set_option pp.proofs true in\n#print NLA.IE05._proved.'+n+'\n'
(E/'Inspect.lean').write_text(s)
(E/'expected-type-extraction.json').write_text(json.dumps({'frozen_challenge_sha256':hashlib.sha256(C.encode()).hexdigest(),'headers':headers,'expected_types_are_Props_without_admissions':True,'actual_roots':['NLA.IE05._proved.'+n for n in roots],'required_dependencies':req,'inspector_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2)+'\n')
print(hashlib.sha256(s.encode()).hexdigest())
