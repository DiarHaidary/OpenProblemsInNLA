/- RA-20 algebra helper author's diagnostic checks. This is not an
independent final review, Linux run or Comparator result. Traversal structure is
adapted from the completed RA-09 referee-2 inspector; every result is rerun here.
The reference changes the frozen Challenge namespace only. -/
import NLA.RA20.Algebra
import verification.«algebra-development».Reference
import Lean.Util.FoldConsts

set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.RA20.hollow_variety_semantics_proved,
      ``NLA.RA20.AlgebraReference.hollow_variety_semantics),
    (``NLA.RA20.reduced_coordinate_ring_proved,
      ``NLA.RA20.AlgebraReference.reduced_coordinate_ring)]
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual theorem {actual}"
    let some b := env.find? reference | throwError "Missing frozen reference {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Actual export is not a theorem {actual}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type b.type do
        throwError "Frozen signature mismatch {actual}"
    unless (← liftCoreM <| collectAxioms reference).contains ``sorryAx do
      throwError "Expected diagnostic reference admission {reference}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.RA20." ||
    n.toString.startsWith "_private.NLA.RA20."
  let mut pending := pairs.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.RA20.AlgebraReference." then
          throwError "Actual proof reached admitted reference {name}"
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
  let required := [``NLA.RA20.hollow_rank_le_two, ``NLA.RA20.hollow_det,
    ``NLA.RA20.hollow_mem_variety_iff, ``NLA.RA20.matrix_eq_hollow_of_mem,
    ``NLA.RA20.abcPolynomial_squarefree, ``NLA.RA20.abcIdeal_isRadical,
    ``NLA.RA20.abcIdeal_vanishing, ``NLA.RA20.definingIdeal_eq_comap_abcIdeal,
    ``NLA.RA20.hollowQuotientMap_ker, ``NLA.RA20.reducedCoordinateEquiv,
    ``NLA.RA20.hollowPullback, ``NLA.RA20.offDiagonalPullback,
    ``NLA.RA20.variety, ``NLA.RA20.definingIdeal, ``NLA.RA20.hollow,
    ``Matrix.rank_mul_le_left, ``Matrix.rank_le_width, ``Matrix.rank_of_det_ne_zero,
    ``MvPolynomial.X_prime, ``squarefree_mul_iff, ``Squarefree.isRadical,
    ``MvPolynomial.vanishingIdeal_zeroLocus_eq_radical,
    ``Ideal.quotientKerAlgEquivOfSurjective, ``Ideal.quotientEquivAlgOfEq]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.RA20.hollow_variety_semantics_proved
#assert_trust kernel NLA.RA20.reduced_coordinate_ring_proved
#assert_trust kernel NLA.RA20.hollow_rank_le_two
#assert_trust kernel NLA.RA20.abcPolynomial_squarefree
#assert_trust kernel NLA.RA20.abcIdeal_vanishing
#assert_trust kernel NLA.RA20.definingIdeal_eq_comap_abcIdeal
#print axioms NLA.RA20.hollow_variety_semantics_proved
#print axioms NLA.RA20.reduced_coordinate_ring_proved
#print axioms NLA.RA20.hollow_rank_le_two
#print axioms NLA.RA20.abcPolynomial_squarefree
#print axioms NLA.RA20.abcIdeal_vanishing
#print axioms NLA.RA20.definingIdeal_eq_comap_abcIdeal
set_option pp.all true in
#print NLA.RA20.variety
set_option pp.all true in
#print NLA.RA20.definingIdeal
set_option pp.all true in
#print NLA.RA20.reducedCoordinateEquiv
set_option pp.proofs true in
#print NLA.RA20.hollow_variety_semantics_proved
set_option pp.proofs true in
#print NLA.RA20.abcIdeal_vanishing
set_option pp.proofs true in
#print NLA.RA20.definingIdeal_eq_comap_abcIdeal
set_option pp.proofs true in
#print NLA.RA20.reduced_coordinate_ring_proved
