/- RA20 smoothness implementation audit. Imports the actual proved module, not Challenge.
The following consumer copies the exact frozen contract; no extra premise is added. -/
import NLA.RA20.Smooth
import Lean.Util.FoldConsts

namespace NLA.RA20.SmoothAudit

theorem exact_frozen_contract (X : Mat 3) :
    SmoothPoint 3 3 X ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧ ExactlyOneZero (X 0 1) (X 0 2) (X 1 2) :=
  algebraic_smooth_locus_proved X

#assert_trust kernel exact_frozen_contract
#print axioms exact_frozen_contract

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let some actual := env.find? ``NLA.RA20.algebraic_smooth_locus_proved |
    throwError "Missing actual theorem"
  let some expected := env.find? ``exact_frozen_contract | throwError "Missing exact consumer"
  liftTermElabM do
    unless ← Lean.Meta.isDefEq actual.type expected.type do throwError "Frozen contract type mismatch"
  logInfo "EXACT_FROZEN_CONTRACT_TYPE: PASS"
  let mut pending := [``NLA.RA20.algebraic_smooth_locus_proved]
  let mut seen : List Name := []
  let mut allUsed : List Name := []
  for _ in [:2000] do
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
        let next := used.filter (fun n => n.toString.startsWith "NLA.RA20.")
        logInfo m!"ACTUAL_PROOF_EDGE {name}: {next}"
        pending := next ++ pending
  unless pending.isEmpty do throwError "Incomplete proof traversal"
  for need in [``NLA.RA20.SmoothPoint, ``NLA.RA20.definingIdeal,
      ``NLA.RA20.variety, ``NLA.RA20.abc_smooth_locus_iff,
      ``NLA.RA20.abc_local_not_smooth, ``NLA.RA20.abc_local_smooth,
      ``NLA.RA20.triple_product_not_formallySmooth,
      ``NLA.RA20.abcLocalizationMap_surjective, ``NLA.RA20.abcLocalizationMap_ker,
      ``NLA.RA20.abcLocalChart_retraction, ``NLA.RA20.formallySmooth_of_retraction,
      ``NLA.RA20.abcPoint_comap, ``NLA.RA20.reducedPoint_comap,
      ``NLA.RA20.reducedCoordinateEquiv, ``NLA.RA20.definingIdeal_eq_comap_abcIdeal,
      ``NLA.RA20.abcIdeal_vanishing, ``NLA.RA20.abcPolynomial_squarefree,
      ``NLA.RA20.smoothLocus_comap_algEquiv,
      ``Algebra.smoothLocus, ``MvPolynomial.vanishingIdeal,
      ``MvPolynomial.pointToPoint, ``MvPolynomial.vanishingIdeal_zeroLocus_eq_radical,
      ``Algebra.FormallySmooth.iff_split_surjection,
      ``Algebra.FormallySmooth.of_comp_surjective,
      ``Algebra.FormallySmooth.comp_surjective,
      ``Algebra.FormallySmooth.iff_of_equiv,
      ``IsLocalization.algEquivOfAlgEquiv,
      ``IsLocalization.ker_map, ``IsLocalization.map_surjective_of_surjective,
      ``PrimeSpectrum.comap_injective_of_surjective] do
    unless allUsed.contains need do throwError "Missing material dependency {need}"
    logInfo m!"REQUIRED_MATERIAL_DEPENDENCY {need}"
  for forbidden in [``sorryAx] do
    if allUsed.contains forbidden then throwError "Forbidden body dependency {forbidden}"
  logInfo m!"ACTUAL_PROJECT_DECLARATIONS: {seen.length}"

set_option pp.all true in
#check NLA.RA20.algebraic_smooth_locus_proved
#check Algebra.FormallySmooth.iff_split_surjection
#check IsLocalization.ker_map
#check IsLocalization.map_surjective_of_surjective
#check IsLocalization.algEquivOfAlgEquiv
#check NLA.RA20.smoothLocus_comap_algEquiv

end NLA.RA20.SmoothAudit
