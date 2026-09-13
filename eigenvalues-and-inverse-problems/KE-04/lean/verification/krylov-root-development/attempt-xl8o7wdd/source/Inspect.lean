import NLA.KE04.Krylov
import Lean.Util.FoldConsts
noncomputable section
open scoped BigOperators
open NLA.KE04
namespace KE04KrylovExpected
def krylov_range_semantics : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ),
krylov A V ell = LinearMap.range (krylovCombination A V ell) ∧
      (∀ x, x ∈ krylov A V ell ↔ ∃ c : Fin ell × Fin p → ℝ,
        x = ∑ rc, c rc • column (A ^ rc.1.val * V) rc.2) ∧
      Module.finrank ℝ (krylov A V ell) ≤ ell * p

def krylov_nesting_and_shift : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p),
krylov A V 0 = ⊥ ∧ Monotone (krylov A V) ∧
      ∀ ell x, x ∈ krylov A V ell → act A x ∈ krylov A V (ell + 1)

def fullBlockDimension_iff_independent : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ),
(FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell)) ∧
      (FullColumnRank V ↔ FullBlockDimension A V 1)

def fullBlockDimension_prefix : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (s : ℕ) (hs : FullBlockDimension A V s),
∀ ell, ell ≤ s → FullBlockDimension A V ell ∧
      Function.Injective (krylovCombination A V ell)

def lastFullBlockIteration_exists : Prop := ∀ {n p : ℕ} (hp : 0 < p)
    (A : Mat n) (V : Rect n p) (hV : FullColumnRank V),
∃ s, 1 ≤ s ∧ LastFullBlockIteration A V s

end KE04KrylovExpected
set_option leancert.trust "kernel"
set_option maxHeartbeats 1600000
#assert_trust kernel NLA.KE04._proved.krylov_range_semantics
#print axioms NLA.KE04._proved.krylov_range_semantics
#assert_trust kernel NLA.KE04._proved.krylov_nesting_and_shift
#print axioms NLA.KE04._proved.krylov_nesting_and_shift
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_iff_independent
#print axioms NLA.KE04._proved.fullBlockDimension_iff_independent
#assert_trust kernel NLA.KE04._proved.fullBlockDimension_prefix
#print axioms NLA.KE04._proved.fullBlockDimension_prefix
#assert_trust kernel NLA.KE04._proved.lastFullBlockIteration_exists
#print axioms NLA.KE04._proved.lastFullBlockIteration_exists

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let targets : List (Name × Name) := [(``NLA.KE04._proved.krylov_range_semantics, ``KE04KrylovExpected.krylov_range_semantics), (``NLA.KE04._proved.krylov_nesting_and_shift, ``KE04KrylovExpected.krylov_nesting_and_shift), (``NLA.KE04._proved.fullBlockDimension_iff_independent, ``KE04KrylovExpected.fullBlockDimension_iff_independent), (``NLA.KE04._proved.fullBlockDimension_prefix, ``KE04KrylovExpected.fullBlockDimension_prefix), (``NLA.KE04._proved.lastFullBlockIteration_exists, ``KE04KrylovExpected.lastFullBlockIteration_exists)]
  for (actual, expected) in targets do
    let some ci := env.find? actual | throwError "Missing actual proof {actual}"
    let some expectedCI := env.find? expected | throwError "Missing exact target"
    let some expectedType := expectedCI.value? (allowOpaque := true) | throwError "Missing expected type"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq ci.type expectedType do throwError "Frozen type mismatch {actual}"
    logInfo m!"EXACT_CONTRACT {actual}: {ci.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." || n.toString.startsWith "_private.NLA.KE04."
  let mut pending := targets.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:6000] do
    match pending with
    | [] => pure ()
    | n :: rest =>
      pending := rest
      unless seen.contains n do
        seen := n :: seen
        let some ci := env.find? n | throwError "Missing project declaration {n}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial declaration {n}"
        let axs ← liftCoreM <| collectAxioms n
        for ax in axs do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonstandard actual axiom {n}: {ax}"
        let some body := ci.value? (allowOpaque := true) | throwError "Bodyless declaration {n}"
        let ds := ci.type.getUsedConstants.toList ++ body.getUsedConstants.toList
        used := ds ++ used
        pending := ds.filter isProject ++ pending
        logInfo m!"ACTUAL_PROJECT {n}: axioms={axs.toList}; dependencies={ds}"
  unless pending.isEmpty do throwError "Incomplete actual traversal"
  for bad in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains bad then throwError "Forbidden dependency {bad}"
  let required := [``Fintype.range_linearCombination, ``finrank_range_le_card,
    ``Submodule.span_induction, ``Submodule.span_mono,
    ``linearIndependent_iff_card_eq_finrank_span,
    ``LinearIndependent.comp,
    ``linearIndependent_iff_injective_fintypeLinearCombination,
    ``Submodule.finrank_le, ``Nat.findGreatest_spec, ``Nat.le_findGreatest,
    ``NLA.KE04.FullBlockDimension, ``NLA.KE04.krylovColumns,
    ``NLA.KE04.krylovCombination, ``NLA.KE04.act]
  for dep in required do
    unless used.contains dep do throwError "Missing material dependency {dep}"
    logInfo m!"MATERIAL_DEPENDENCY {dep}"
  logInfo m!"FINAL_COUNTS contracts={targets.length}, closure={seen.length}, material={required.length}"
