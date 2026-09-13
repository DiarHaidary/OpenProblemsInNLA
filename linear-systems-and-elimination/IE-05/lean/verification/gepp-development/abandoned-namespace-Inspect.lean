/- IE05 scoped GEPP author inspection, not an independent referee or Linux
Comparator. Expected types are Prop-valued definitions mechanically extracted
from the exact frozen headers; there are no diagnostic proof admissions. -/
import NLA.IE05.GEPP
import Lean.Util.FoldConsts
set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.IE05.GEPPExpected
def entryMax_semantics : Prop :=
  ∀ {n : ℕ} (hn : 1 ≤ n) (A : Mat n),
    0 ≤ entryMax A ∧ (∀ i j, |A i j| ≤ entryMax A) ∧
      ∃ i j, entryMax A = |A i j|

def schurStep_bound : Prop :=
  ∀ {n : ℕ} (S : Mat n) (k p : Fin n)
    (hp : AdmissiblePivot S k p),
    activeMax (schurStep S k p) (k.val + 1) ≤ 2 * activeMax S k.val

def gepp_growth_bound : Prop :=
  ∀ {n : ℕ} (hn : 1 ≤ n) (A : Mat n)
    (path : PivotPath n) (hp : AdmissiblePath A path),
    0 < entryMax A ∧ 1 ≤ growth A path ∧ growth A path ≤ (2 : ℝ) ^ (n - 1)

def firstPath_semantics : Prop :=
  ∀ {n : ℕ} (A : Mat n) (hA : A.det ≠ 0),
    FirstAvailablePath A (firstPath A) ∧
      (∀ k, trajectory A (firstPath A) k = firstTrajectory A k) ∧
      ∀ path, FirstAvailablePath A path → path = firstPath A

def orthogonalGrowthSet_bounded : Prop :=
  ∀ (n : ℕ) (hn : 2 ≤ n),
    (orthogonalGrowthSet n).Nonempty ∧ BddAbove (orthogonalGrowthSet n) ∧
      ∀ r ∈ orthogonalGrowthSet n, 1 ≤ r ∧ r ≤ (2 : ℝ) ^ (n - 1)

end NLA.IE05.GEPPExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.IE05._proved.entryMax_semantics, ``NLA.IE05.GEPPExpected.entryMax_semantics),
    (``NLA.IE05._proved.schurStep_bound, ``NLA.IE05.GEPPExpected.schurStep_bound),
    (``NLA.IE05._proved.gepp_growth_bound, ``NLA.IE05.GEPPExpected.gepp_growth_bound),
    (``NLA.IE05._proved.firstPath_semantics, ``NLA.IE05.GEPPExpected.firstPath_semantics),
    (``NLA.IE05._proved.orthogonalGrowthSet_bounded, ``NLA.IE05.GEPPExpected.orthogonalGrowthSet_bounded)]
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
  let required := [``NLA.IE05.entryMax_semantics_proved,
    ``NLA.IE05.schurStep_bound_proved,
    ``NLA.IE05.gepp_growth_bound_proved,
    ``NLA.IE05.firstPath_semantics_proved,
    ``NLA.IE05.orthogonalGrowthSet_bounded_proved,
    ``NLA.IE05.entryMaxNN,
    ``NLA.IE05.entryMax,
    ``NLA.IE05.activeMaxNN,
    ``NLA.IE05.activeMax,
    ``NLA.IE05.growth,
    ``NLA.IE05.peakMax,
    ``NLA.IE05.AdmissiblePivot,
    ``NLA.IE05.AdmissiblePath,
    ``NLA.IE05.FirstAvailablePivot,
    ``NLA.IE05.FirstAvailablePath,
    ``NLA.IE05.trajectory,
    ``NLA.IE05.firstTrajectory,
    ``NLA.IE05.firstPath,
    ``NLA.IE05.firstPivotIndex,
    ``NLA.IE05.schurStep,
    ``NLA.IE05.rowSwap,
    ``NLA.IE05.Orthogonal,
    ``NLA.IE05.orthogonalGrowthSet,
    ``NLA.IE05.ActiveInjective,
    ``NLA.IE05.firstPivotIndex_spec_proved,
    ``NLA.IE05.firstPivotIndex_eq_of_firstAvailable_proved,
    ``NLA.IE05.firstPivotIndex_firstAvailable_proved,
    ``NLA.IE05.firstPath_eq_of_firstAvailable_proved,
    ``NLA.IE05.gepp_stage_bound_proved,
    ``NLA.IE05.activeInjective_initial_proved,
    ``NLA.IE05.activeInjective_nonzero_column_proved,
    ``NLA.IE05.activeInjective_rowSwap_proved,
    ``NLA.IE05.schurStep_mulVec_proved,
    ``NLA.IE05.activeInjective_schur_proved,
    ``NLA.IE05.firstTrajectory_activeInjective_proved,
    ``List.argmax,
    ``List.le_of_mem_argmax,
    ``List.index_of_argmax,
    ``List.idxOf_finRange,
    ``Finset.sup,
    ``Finset.exists_max_image,
    ``Matrix.mulVec,
    ``Matrix.isUnit_iff_isUnit_det,
    ``Matrix.mulVec_injective_iff_isUnit,
    ``Matrix.mulVec_single_one,
    ``Equiv.swap,
    ``Matrix.det]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.IE05._proved.entryMax_semantics
#print axioms NLA.IE05._proved.entryMax_semantics
#assert_trust kernel NLA.IE05._proved.schurStep_bound
#print axioms NLA.IE05._proved.schurStep_bound
#assert_trust kernel NLA.IE05._proved.gepp_growth_bound
#print axioms NLA.IE05._proved.gepp_growth_bound
#assert_trust kernel NLA.IE05._proved.firstPath_semantics
#print axioms NLA.IE05._proved.firstPath_semantics
#assert_trust kernel NLA.IE05._proved.orthogonalGrowthSet_bounded
#print axioms NLA.IE05._proved.orthogonalGrowthSet_bounded
set_option pp.all true in
#print NLA.IE05.ActiveInjective
set_option pp.all true in
#print NLA.IE05.firstPath
set_option pp.all true in
#print NLA.IE05.growth
set_option pp.all true in
#print NLA.IE05.orthogonalGrowthSet
set_option pp.proofs true in
#print NLA.IE05.activeInjective_schur_proved
set_option pp.proofs true in
#print NLA.IE05.gepp_growth_bound_proved
set_option pp.proofs true in
#print NLA.IE05.firstPath_semantics_proved
set_option pp.proofs true in
#print NLA.IE05.orthogonalGrowthSet_bounded_proved
