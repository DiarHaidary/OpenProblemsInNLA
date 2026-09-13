/- RA20 Critical implementation audit; no Challenge import. The exact contract below
is copied from the frozen Challenge. All proof terms are inspected after fresh elaboration. -/
import NLA.RA20.Critical
import Lean.Util.FoldConsts

namespace NLA.RA20.CriticalAudit

theorem exact_frozen_contract (U : Mat 3) (hU : GenericData U) :
    criticalSet 3 3 U = Set.range (candidate U) ∧ Function.Injective (candidate U) :=
  generic_critical_locus_proved U hU

#assert_trust kernel exact_frozen_contract
#print axioms exact_frozen_contract

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let some actual := env.find? ``NLA.RA20.generic_critical_locus_proved |
    throwError "Missing actual theorem"
  let some expected := env.find? ``exact_frozen_contract | throwError "Missing exact consumer"
  liftTermElabM do
    unless ← Lean.Meta.isDefEq actual.type expected.type do throwError "Frozen contract mismatch"
  logInfo "EXACT_FROZEN_CONTRACT_TYPE: PASS"
  let mut pending := [``NLA.RA20.generic_critical_locus_proved]
  let mut seen : List Name := []
  let mut allUsed : List Name := []
  for _ in [:4000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        seen := name :: seen
        let some ci := env.find? name | throwError "Missing declaration {name}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial declaration {name}"
        let some body := ci.value? (allowOpaque := true) | throwError "Bodyless declaration {name}"
        let used := ci.type.getUsedConstants.toList ++ body.getUsedConstants.toList
        allUsed := used ++ allUsed
        for ax in (← liftCoreM <| collectAxioms name) do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Forbidden axiom: {name}: {ax}"
        let next := used.filter (fun n => n.toString.startsWith "NLA.RA20." ||
          n.toString.startsWith "_private.NLA.RA20.")
        logInfo m!"ACTUAL_PROOF_EDGE {name}: {next}"
        pending := next ++ pending
  unless pending.isEmpty do throwError "Incomplete proof traversal"
  for need in [``NLA.RA20.GenericData, ``NLA.RA20.criticalSet,
      ``NLA.RA20.SmoothCriticalPoint, ``NLA.RA20.SmoothPoint,
      ``NLA.RA20.TangentVector, ``NLA.RA20.fullFrobeniusDistance,
      ``NLA.RA20.generic_critical_exhaustion, ``NLA.RA20.generic_candidate_critical,
      ``NLA.RA20.generic_candidate_injective, ``NLA.RA20.smoothCritical_hollow_iff,
      ``NLA.RA20.critical_first_plane, ``NLA.RA20.critical_second_plane,
      ``NLA.RA20.critical_third_plane, ``NLA.RA20.hollow_frobenius_differential,
      ``NLA.RA20.algebraic_smooth_locus_proved, ``NLA.RA20.algebraic_tangent_space_proved,
      ``NLA.RA20.polyDirectional_hollowPullback, ``NLA.RA20.full_frobenius_differential_proved,
      ``NLA.RA20.hasFDerivAt_sum_squares, ``NLA.RA20.hasFDerivAt_affine_square,
      ``NLA.RA20.definingIdeal_eq_comap_abcIdeal, ``NLA.RA20.abcIdeal_vanishing,
      ``NLA.RA20.abcPolynomial_squarefree, ``NLA.RA20.triple_product_not_formallySmooth,
      ``NLA.RA20.abcLocalChart_retraction, ``NLA.RA20.smoothLocus_comap_algEquiv,
      ``fderiv, ``MvPolynomial.pderiv, ``MvPolynomial.pderiv_mul,
      ``MvPolynomial.vanishingIdeal, ``MvPolynomial.vanishingIdeal_zeroLocus_eq_radical,
      ``Algebra.smoothLocus, ``Algebra.FormallySmooth.iff_split_surjection,
      ``Algebra.FormallySmooth.of_comp_surjective, ``IsLocalization.ker_map,
      ``IsLocalization.algEquivOfAlgEquiv, ``ContinuousLinearMap.proj,
      ``HasFDerivAt.fun_sum, ``HasFDerivAt.mul] do
    unless allUsed.contains need do throwError "Missing material dependency {need}"
    logInfo m!"REQUIRED_MATERIAL_DEPENDENCY {need}"
  if allUsed.contains ``sorryAx then throwError "Admission in proof dependency"
  logInfo m!"ACTUAL_PROJECT_DECLARATIONS: {seen.length}"

#check NLA.RA20.generic_critical_locus_proved
#check NLA.RA20.smoothCritical_hollow_iff
#check NLA.RA20.algebraic_tangent_space_proved
#check NLA.RA20.full_frobenius_differential_proved
#check NLA.RA20.generic_critical_exhaustion

end NLA.RA20.CriticalAudit
