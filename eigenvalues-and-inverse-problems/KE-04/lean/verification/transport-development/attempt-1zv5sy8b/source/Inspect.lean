import NLA.KE04.Transport
import Lean.Util.FoldConsts
noncomputable section
open scoped BigOperators
open NLA.KE04
namespace KE04TransportExpected
def quadratic_forms_agree : Prop := ∀ {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j)
    (Qk : Rect n (k * p)) (Qj : Rect n (j * p))
    (hQk : IsKrylovBasis A V k Qk) (hQj : IsKrylovBasis A V j Qj)
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (a b : ℝ),
form (compressedQuadratic A Qk a b) x =
      form (compressedQuadratic A Qj a b) x

def later_quadratic_identity : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j) (Qj : Rect n (j * p))
    (hQj : IsKrylovBasis A V j Qj) (x : Vec n)
    (hx : x ∈ krylov A V (k - 1)) (a b : ℝ),
act (compressedQuadratic A Qj a b) x = act (quadraticMatrix A a b) x

def interval_index_validity : Prop := ∀ (k p i : ℕ) (hk : 1 ≤ k)
    (hi : 1 ≤ i) (hu : i ≤ (k - 1) * p),
2 ≤ k ∧ 0 < p ∧ i - 1 < k * p ∧ i + p - 1 < k * p

def fullPrefix_implies_canonical : Prop := FullPrefixBlockLanczosClaim → BlockLanczosConjecture

end KE04TransportExpected
set_option leancert.trust "kernel"
set_option maxHeartbeats 1600000
#assert_trust kernel NLA.KE04._proved.quadratic_forms_agree
#print axioms NLA.KE04._proved.quadratic_forms_agree
#assert_trust kernel NLA.KE04._proved.later_quadratic_identity
#print axioms NLA.KE04._proved.later_quadratic_identity
#assert_trust kernel NLA.KE04._proved.interval_index_validity
#print axioms NLA.KE04._proved.interval_index_validity
#assert_trust kernel NLA.KE04._proved.fullPrefix_implies_canonical
#print axioms NLA.KE04._proved.fullPrefix_implies_canonical

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let targets : List (Name × Name) := [(``NLA.KE04._proved.quadratic_forms_agree, ``KE04TransportExpected.quadratic_forms_agree), (``NLA.KE04._proved.later_quadratic_identity, ``KE04TransportExpected.later_quadratic_identity), (``NLA.KE04._proved.interval_index_validity, ``KE04TransportExpected.interval_index_validity), (``NLA.KE04._proved.fullPrefix_implies_canonical, ``KE04TransportExpected.fullPrefix_implies_canonical)]
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
  let required := [``NLA.KE04._proved.krylov_mono,
    ``NLA.KE04._proved.act_mem_krylov_succ,
    ``NLA.KE04._proved.frameProjection_fixed_iff,
    ``NLA.KE04._proved.frame_inner,
    ``NLA.KE04._proved.compression_action_coordinates,
    ``NLA.KE04._proved.quadratic_semantics,
    ``NLA.KE04._proved.inner_act_transpose,
    ``NLA.KE04.compressedQuadratic, ``NLA.KE04.quadraticMatrix,
    ``NLA.KE04.form, ``NLA.KE04.krylov, ``NLA.KE04.IsKrylovBasis,
    ``NLA.KE04.FullPrefixBlockLanczosClaim, ``NLA.KE04.BlockLanczosConjecture]
  for dep in required do
    unless used.contains dep do throwError "Missing material dependency {dep}"
    logInfo m!"MATERIAL_DEPENDENCY {dep}"
  logInfo m!"FINAL_COUNTS contracts={targets.length}, closure={seen.length}, material={required.length}"
