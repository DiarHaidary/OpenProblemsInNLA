import NLA.KE04.Intersection
import Lean.Util.FoldConsts
noncomputable section
open scoped BigOperators
open NLA.KE04
namespace KE04IntersectionExpected
def krylov_intersection_nonzero : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 1 ≤ k) (hfull : FullBlockDimension A V k)
    (hprev : FullBlockDimension A V (k - 1)) (E : Submodule ℝ (Vec n))
    (hE : E ≤ krylov A V k) (hdim : Module.finrank ℝ E = p + 1),
∃ x : Vec n, x ≠ 0 ∧ x ∈ E ∧ x ∈ krylov A V (k - 1)

end KE04IntersectionExpected
set_option leancert.trust "kernel"
set_option maxHeartbeats 1600000
#assert_trust kernel NLA.KE04._proved.krylov_intersection_nonzero
#print axioms NLA.KE04._proved.krylov_intersection_nonzero

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let targets : List (Name × Name) := [(``NLA.KE04._proved.krylov_intersection_nonzero, ``KE04IntersectionExpected.krylov_intersection_nonzero)]
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
    ``Submodule.finrank_sup_add_finrank_inf_eq,
    ``Submodule.finrank_mono, ``Module.finrank_pos_iff_exists_ne_zero,
    ``NLA.KE04.FullBlockDimension, ``NLA.KE04.krylov]
  for dep in required do
    unless used.contains dep do throwError "Missing material dependency {dep}"
    logInfo m!"MATERIAL_DEPENDENCY {dep}"
  logInfo m!"FINAL_COUNTS contracts={targets.length}, closure={seen.length}, material={required.length}"
