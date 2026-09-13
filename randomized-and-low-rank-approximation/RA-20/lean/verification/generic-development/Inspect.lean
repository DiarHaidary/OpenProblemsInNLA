/- RA20 Generic helper packager/inspector. Already an RA20 implementation
contributor: this is not an independent final mathematical review. Actual
term/type traversal is adapted from the scoped Differential inspector. -/
import NLA.RA20.Generic
import verification.«generic-development».Reference
import Lean.Util.FoldConsts

set_option leancert.trust "kernel"
set_option maxHeartbeats 1200000

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let actual := ``NLA.RA20.generic_data_intersection_proved
  let reference := ``NLA.RA20.GenericHelperReference.generic_data_intersection
  let some a := env.find? actual | throwError "Missing actual theorem"
  let some b := env.find? reference | throwError "Missing exact reference"
  match a with
  | .thmInfo _ => pure ()
  | _ => throwError "Actual result is not a theorem"
  liftTermElabM do
    unless ← Lean.Meta.isDefEq a.type b.type do
      throwError "Frozen generic-data contract mismatch"
  unless (← liftCoreM <| collectAxioms reference).contains ``sorryAx do
    throwError "Expected diagnostic-only reference admission"
  logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.RA20." ||
    n.toString.startsWith "_private.NLA.RA20."
  let mut pending := [actual]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.RA20.GenericHelperReference." then
          throwError "Actual proof reached admitted reference {name}"
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing declaration {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial declaration {name}"
        let axs ← liftCoreM <| collectAxioms name
        for ax in axs do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonstandard transitive axiom {name}: {ax}"
        logInfo m!"ACTUAL_AXIOMS {name}: {axs.toList}"
        let body ← match ci.value? (allowOpaque := true) with
          | some v => pure v.getUsedConstants.toList
          | none => match ci with
            | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
            | _ => throwError "Unexplained bodyless project declaration {name}"
        let ds := ci.type.getUsedConstants.toList ++ body
        used := ds ++ used
        let next := ds.filter isProject
        logInfo m!"PROJECT_EDGE {name}: {next}"
        pending := next ++ pending
  unless pending.isEmpty do throwError "Incomplete traversal"
  let required := [``NLA.RA20.GenericData, ``NLA.RA20.symmetricParameterIndex,
    ``NLA.RA20.symmetricParameter, ``NLA.RA20.symmetricDataCoordinates,
    ``NLA.RA20.symmetricParameter_isSymm, ``NLA.RA20.symmetricParameter_reconstruct,
    ``NLA.RA20.eval_rename_symmetricParameter, ``MvPolynomial.rename,
    ``MvPolynomial.eval, ``MvPolynomial.eval_rename, ``MvPolynomial.funext,
    ``MvPolynomial.X_ne_zero, ``mul_ne_zero]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.RA20.generic_data_intersection_proved
#print axioms NLA.RA20.generic_data_intersection_proved
set_option pp.all true in
#print NLA.RA20.GenericData
set_option pp.all true in
#print NLA.RA20.symmetricParameter
set_option pp.all true in
#print NLA.RA20.symmetricDataCoordinates
set_option pp.proofs true in
#print NLA.RA20.generic_data_intersection_proved
