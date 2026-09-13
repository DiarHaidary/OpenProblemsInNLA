/- LU helper author diagnostic, not an independent referee or Linux Comparator.
Expected contract is an admission-free Prop definition from the frozen header. -/
import NLA.IE05.LUTrajectory
import Lean.Util.FoldConsts
set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.LUExpected
def scaledLU_trajectory : Prop :=
  ∀ {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hLb : ∀ i j, j < i → |L i j| ≤ 1)
    (hT : UpperTriangular T) (hTp : ∀ i, 0 < T i i) (hd : ∀ j, 0 < d j),
    FirstAvailablePath (scaledColumns (L * T) d) (noSwapPath n) ∧
      firstPath (scaledColumns (L * T) d) = noSwapPath n ∧
      ∀ k, k ≤ n → trajectory (scaledColumns (L * T) d) (noSwapPath n) k =
        scaledColumns (tailProduct L T k) d
end NLA.IE05.LUExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.IE05._proved.scaledLU_trajectory,
    ``NLA.IE05.LUExpected.scaledLU_trajectory)]
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
  let mut pending := [``NLA.IE05._proved.tailProduct_zero, ``NLA.IE05._proved.tailProduct_terminal, ``NLA.IE05._proved.tailProduct_pivot_row, ``NLA.IE05._proved.tailProduct_pivot_column, ``NLA.IE05._proved.tailProduct_split, ``NLA.IE05._proved.scaled_tail_schur, ``NLA.IE05._proved.scaled_tail_firstAvailable, ``NLA.IE05._proved.scaled_noSwap_trajectory, ``NLA.IE05._proved.scaledLU_trajectory]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.IE05.LUExpected." then
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
  let required := [``NLA.IE05._proved.tailProduct_zero,
    ``NLA.IE05._proved.tailProduct_pivot_row,
    ``NLA.IE05._proved.tailProduct_pivot_column,
    ``NLA.IE05._proved.tailProduct_split,
    ``NLA.IE05._proved.scaled_tail_schur,
    ``NLA.IE05._proved.scaled_tail_firstAvailable,
    ``NLA.IE05._proved.scaled_noSwap_trajectory,
    ``NLA.IE05.firstPath_eq_of_firstAvailable_proved,
    ``NLA.IE05.firstPivotIndex_eq_of_firstAvailable_proved,
    ``NLA.IE05.firstPivotIndex_spec_proved,
    ``NLA.IE05.tailProduct,
    ``NLA.IE05.scaledColumns,
    ``NLA.IE05.UnitLower,
    ``NLA.IE05.UpperTriangular,
    ``NLA.IE05.AdmissiblePivot,
    ``NLA.IE05.FirstAvailablePivot,
    ``NLA.IE05.FirstAvailablePath,
    ``NLA.IE05.noSwapPath,
    ``NLA.IE05.trajectory,
    ``NLA.IE05.firstPath,
    ``NLA.IE05.rowSwap,
    ``NLA.IE05.schurStep,
    ``Real.sqrt,
    ``Real.sqrt_pos,
    ``Finset.sum_eq_single,
    ``Finset.sum_congr,
    ``Finset.sum_add_distrib,
    ``List.argmax,
    ``List.index_of_argmax]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.IE05._proved.tailProduct_zero
#print axioms NLA.IE05._proved.tailProduct_zero
#assert_trust kernel NLA.IE05._proved.tailProduct_terminal
#print axioms NLA.IE05._proved.tailProduct_terminal
#assert_trust kernel NLA.IE05._proved.tailProduct_pivot_row
#print axioms NLA.IE05._proved.tailProduct_pivot_row
#assert_trust kernel NLA.IE05._proved.tailProduct_pivot_column
#print axioms NLA.IE05._proved.tailProduct_pivot_column
#assert_trust kernel NLA.IE05._proved.tailProduct_split
#print axioms NLA.IE05._proved.tailProduct_split
#assert_trust kernel NLA.IE05._proved.scaled_tail_schur
#print axioms NLA.IE05._proved.scaled_tail_schur
#assert_trust kernel NLA.IE05._proved.scaled_tail_firstAvailable
#print axioms NLA.IE05._proved.scaled_tail_firstAvailable
#assert_trust kernel NLA.IE05._proved.scaled_noSwap_trajectory
#print axioms NLA.IE05._proved.scaled_noSwap_trajectory
#assert_trust kernel NLA.IE05._proved.scaledLU_trajectory
#print axioms NLA.IE05._proved.scaledLU_trajectory
set_option pp.all true in
#print NLA.IE05.UnitLower
set_option pp.all true in
#print NLA.IE05.UpperTriangular
set_option pp.all true in
#print NLA.IE05.tailProduct
set_option pp.all true in
#print NLA.IE05.scaledColumns
set_option pp.all true in
#print NLA.IE05.noSwapPath
set_option pp.all true in
#print NLA.IE05.schurStep
set_option pp.proofs true in
#print NLA.IE05._proved.scaled_tail_schur
set_option pp.proofs true in
#print NLA.IE05._proved.scaled_tail_firstAvailable
set_option pp.proofs true in
#print NLA.IE05._proved.scaled_noSwap_trajectory
set_option pp.proofs true in
#print NLA.IE05._proved.scaledLU_trajectory
