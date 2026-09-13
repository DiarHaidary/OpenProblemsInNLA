#!/usr/bin/env python3
"""Build admission-free expected types from the unchanged first five contracts.
Traversal diagnostics adapt the campaign RA20 conclusion inspector. No theorem
is imported or assumed from Challenge.lean; its text supplies Prop definitions.
"""
from pathlib import Path
import hashlib,json,re
project=Path(__file__).resolve().parents[2]
evidence=Path(__file__).resolve().parent
text=(project/'Challenge.lean').read_text()
assert hashlib.sha256(text.encode()).hexdigest()=='0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e'
names=['entryMax_semantics','schurStep_bound','gepp_growth_bound','firstPath_semantics','orthogonalGrowthSet_bounded']
headers={}
defs=[]
for name in names:
    match=re.search(r'^theorem '+name+r'\b(.*?) := by sorry$',text,re.M|re.S)
    assert match is not None,name
    header=match.group(1)
    binders,conclusion=header.split(' :\n',1)
    headers[name]=header
    defs.append('def '+name+' : Prop :=\n  ∀'+binders+',\n'+conclusion+'\n')
pairs=',\n    '.join('(``NLA.IE05._proved.'+n+', ``NLA.IE05.GEPPExpected.'+n+')' for n in names)
required_project=['entryMax_semantics_proved','schurStep_bound_proved','gepp_growth_bound_proved','firstPath_semantics_proved','orthogonalGrowthSet_bounded_proved','entryMaxNN','entryMax','activeMaxNN','activeMax','growth','peakMax','AdmissiblePivot','AdmissiblePath','FirstAvailablePivot','FirstAvailablePath','trajectory','firstTrajectory','firstPath','firstPivotIndex','schurStep','rowSwap','Orthogonal','orthogonalGrowthSet','ActiveInjective','firstPivotIndex_spec_proved','firstPivotIndex_eq_of_firstAvailable_proved','firstPivotIndex_firstAvailable_proved','firstPath_eq_of_firstAvailable_proved','gepp_stage_bound_proved','activeInjective_initial_proved','activeInjective_nonzero_column_proved','activeInjective_rowSwap_proved','schurStep_mulVec_proved','activeInjective_schur_proved','firstTrajectory_activeInjective_proved']
required_external=['List.argmax','List.le_of_mem_argmax','List.index_of_argmax','List.idxOf_finRange','Finset.sup','Finset.exists_max_image','Matrix.mulVec','Matrix.isUnit_iff_isUnit_det','Matrix.mulVec_injective_iff_isUnit','Matrix.mulVec_single_one','Equiv.swap','Matrix.det']
required=',\n    '.join('``'+n for n in ['NLA.IE05.'+n for n in required_project]+required_external)
source='''/- IE05 scoped GEPP author inspection, not an independent referee or Linux
Comparator. Expected types are Prop-valued definitions mechanically extracted
from the exact frozen headers; there are no diagnostic proof admissions. -/
import NLA.IE05.GEPP
import Lean.Util.FoldConsts
set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.GEPPExpected
'''+ '\n'.join(defs)+'''
end NLA.IE05.GEPPExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := ['''+pairs+''']
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual theorem {actual}"
    let some b := env.find? reference | throwError "Missing expected type {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Actual export is not a theorem {actual}"
    let some expected := b.value? | throwError "Expected type has no value {reference}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type expected do
        throwError "Frozen signature mismatch {actual}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.IE05." ||
    n.toString.startsWith "_private.NLA.IE05."
  let mut pending := pairs.map Prod.fst ++ [``NLA.IE05._proved.firstPivotIndex_spec, ``NLA.IE05._proved.firstPivotIndex_eq_of_firstAvailable, ``NLA.IE05._proved.firstPivotIndex_firstAvailable, ``NLA.IE05._proved.trajectory_firstPath_eq, ``NLA.IE05._proved.firstPath_eq_of_firstAvailable]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.IE05.GEPPExpected." then
          throwError "Actual proof reached diagnostic type {name}"
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing declaration {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial declaration {name}"
        let axioms ← liftCoreM <| collectAxioms name
        for ax in axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Forbidden transitive axiom {name}: {ax}"
        logInfo m!"ACTUAL_AXIOMS {name}: {axioms.toList}"
        let body ← match ci.value? (allowOpaque := true) with
          | some b => pure b.getUsedConstants.toList
          | none => match ci with
            | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
            | _ => throwError "Unexplained bodyless declaration {name}"
        let deps := ci.type.getUsedConstants.toList ++ body
        used := deps ++ used
        let follow := deps.filter isProject
        logInfo m!"PROJECT_EDGE {name}: {follow}"
        pending := follow ++ pending
  unless pending.isEmpty do throwError "Incomplete traversal"
  let required := ['''+required+''']
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

'''
for name in names:
    source+='#assert_trust kernel NLA.IE05._proved.'+name+'\n#print axioms NLA.IE05._proved.'+name+'\n'
for name in ['ActiveInjective','firstPath','growth','orthogonalGrowthSet']:
    source+='set_option pp.all true in\n#print NLA.IE05.'+name+'\n'
for name in ['activeInjective_schur_proved','gepp_growth_bound_proved','firstPath_semantics_proved','orthogonalGrowthSet_bounded_proved']:
    source+='set_option pp.proofs true in\n#print NLA.IE05.'+name+'\n'
(evidence/'Inspect.lean').write_text(source)
(evidence/'expected-type-extraction.json').write_text(json.dumps({'frozen_challenge_sha256':hashlib.sha256(text.encode()).hexdigest(),'headers':headers,'expected_types_are_prop_definitions':True,'no_reference_proofs_or_admissions':True,'inspector_sha256':hashlib.sha256(source.encode()).hexdigest(),'required_project':required_project,'required_external':required_external},indent=2)+'\n')
print(hashlib.sha256(source.encode()).hexdigest())
