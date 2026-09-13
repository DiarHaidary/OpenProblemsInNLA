/- RA20 fresh independent final referee 1. Structural traversal was inspected
and adapted from the assembly diagnostic, but all source is freshly compiled
and every result is independently rerun. This local comparison is NOT the Linux
Comparator. It adds raw structural equality of the two elaborated expressions. -/
import Solution
import reviews.«final-referee-1-evidence».ReferenceChallenge
import Lean.Util.FoldConsts

set_option maxHeartbeats 1200000
set_option leancert.trust "kernel"

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [(``NLA.RA20.hollow_variety_semantics, ``NLA.RA20.Referee1Reference.hollow_variety_semantics),
    (``NLA.RA20.reduced_coordinate_ring, ``NLA.RA20.Referee1Reference.reduced_coordinate_ring),
    (``NLA.RA20.algebraic_smooth_locus, ``NLA.RA20.Referee1Reference.algebraic_smooth_locus),
    (``NLA.RA20.algebraic_tangent_space, ``NLA.RA20.Referee1Reference.algebraic_tangent_space),
    (``NLA.RA20.full_frobenius_differential, ``NLA.RA20.Referee1Reference.full_frobenius_differential),
    (``NLA.RA20.hollow_distance_semantics, ``NLA.RA20.Referee1Reference.hollow_distance_semantics),
    (``NLA.RA20.generic_critical_locus, ``NLA.RA20.Referee1Reference.generic_critical_locus),
    (``NLA.RA20.component_hessians, ``NLA.RA20.Referee1Reference.component_hessians),
    (``NLA.RA20.generic_data_intersection, ``NLA.RA20.Referee1Reference.generic_data_intersection),
    (``NLA.RA20.generic_count_three, ``NLA.RA20.Referee1Reference.generic_count_three),
    (``NLA.RA20.generic_count_not_four, ``NLA.RA20.Referee1Reference.generic_count_not_four),
    (``NLA.RA20.not_criticalCountConjecture, ``NLA.RA20.Referee1Reference.not_criticalCountConjecture)]
  for (actual, reference) in pairs do
    let some a := env.find? actual | throwError "Missing actual theorem {actual}"
    let some b := env.find? reference | throwError "Missing frozen reference {reference}"
    match a with
    | .thmInfo _ => pure ()
    | _ => throwError "Actual export is not a theorem {actual}"
    unless a.type == b.type do
      throwError "Raw elaborated expression mismatch {actual}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq a.type b.type do
        throwError "Frozen signature mismatch {actual}"
    unless (← liftCoreM <| collectAxioms reference).contains ``sorryAx do
      throwError "Expected diagnostic reference admission {reference}"
    logInfo m!"EXACT_FROZEN_TYPE {actual}: {a.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.RA20." ||
    n.toString.startsWith "_private.NLA.RA20."
  let globals := env.constants.toList.filter (fun (n, _) => isProject n &&
    !(n.toString.startsWith "NLA.RA20.Referee1Reference."))
  for (n, ci) in globals do
    if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial project global {n}"
    for ax in (← liftCoreM <| collectAxioms n) do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Forbidden project-global axiom {n}: {ax}"
  logInfo m!"ALL_PROJECT_DECLARATIONS {globals.length}"
  let mut pending := pairs.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.RA20.Referee1Reference." then
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
  let required := [``NLA.RA20.hollow_variety_semantics_proved,
    ``NLA.RA20.reduced_coordinate_ring_proved,
    ``NLA.RA20.algebraic_smooth_locus_proved,
    ``NLA.RA20.algebraic_tangent_space_proved,
    ``NLA.RA20.full_frobenius_differential_proved,
    ``NLA.RA20.hollow_distance_semantics_proved,
    ``NLA.RA20.generic_critical_locus_proved,
    ``NLA.RA20.component_hessians_proved,
    ``NLA.RA20.generic_data_intersection_proved,
    ``NLA.RA20.generic_count_three_proved,
    ``NLA.RA20.generic_count_not_four_proved,
    ``NLA.RA20.not_criticalCountConjecture_proved,
    ``NLA.RA20.variety,
    ``NLA.RA20.definingIdeal,
    ``NLA.RA20.SmoothPoint,
    ``NLA.RA20.TangentVector,
    ``NLA.RA20.fullFrobeniusDistance,
    ``NLA.RA20.criticalSet,
    ``NLA.RA20.SmoothCriticalPoint,
    ``NLA.RA20.HasCriticalCount,
    ``NLA.RA20.HasGenericCriticalCount,
    ``NLA.RA20.predictedCount,
    ``NLA.RA20.criticalCountConjecture,
    ``NLA.RA20.genericPolynomial,
    ``NLA.RA20.candidate,
    ``NLA.RA20.GenericData,
    ``NLA.RA20.critical_count_three,
    ``NLA.RA20.polyDirectional_hollowPullback,
    ``NLA.RA20.abc_smooth_locus_iff,
    ``NLA.RA20.generic_critical_exhaustion,
    ``NLA.RA20.generic_candidate_injective,
    ``NLA.RA20.symmetricParameter_reconstruct,
    ``MvPolynomial.vanishingIdeal_zeroLocus_eq_radical,
    ``MvPolynomial.funext,
    ``Algebra.smoothLocus,
    ``MvPolynomial.pderiv,
    ``fderiv,
    ``Cardinal.mk,
    ``Cardinal.mk_range_eq]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.RA20.hollow_variety_semantics
#print axioms NLA.RA20.hollow_variety_semantics
#assert_trust kernel NLA.RA20.reduced_coordinate_ring
#print axioms NLA.RA20.reduced_coordinate_ring
#assert_trust kernel NLA.RA20.algebraic_smooth_locus
#print axioms NLA.RA20.algebraic_smooth_locus
#assert_trust kernel NLA.RA20.algebraic_tangent_space
#print axioms NLA.RA20.algebraic_tangent_space
#assert_trust kernel NLA.RA20.full_frobenius_differential
#print axioms NLA.RA20.full_frobenius_differential
#assert_trust kernel NLA.RA20.hollow_distance_semantics
#print axioms NLA.RA20.hollow_distance_semantics
#assert_trust kernel NLA.RA20.generic_critical_locus
#print axioms NLA.RA20.generic_critical_locus
#assert_trust kernel NLA.RA20.component_hessians
#print axioms NLA.RA20.component_hessians
#assert_trust kernel NLA.RA20.generic_data_intersection
#print axioms NLA.RA20.generic_data_intersection
#assert_trust kernel NLA.RA20.generic_count_three
#print axioms NLA.RA20.generic_count_three
#assert_trust kernel NLA.RA20.generic_count_not_four
#print axioms NLA.RA20.generic_count_not_four
#assert_trust kernel NLA.RA20.not_criticalCountConjecture
#print axioms NLA.RA20.not_criticalCountConjecture
set_option pp.all true in
#print NLA.RA20.SmoothPoint
set_option pp.all true in
#print NLA.RA20.TangentVector
set_option pp.all true in
#print NLA.RA20.HasGenericCriticalCount
set_option pp.all true in
#print NLA.RA20.criticalCountConjecture
set_option pp.all true in
#print NLA.RA20.predictedCount
set_option pp.proofs true in
#print NLA.RA20.critical_count_three
set_option pp.proofs true in
#print NLA.RA20.generic_count_three_proved
set_option pp.proofs true in
#print NLA.RA20.generic_count_not_four_proved
set_option pp.proofs true in
#print NLA.RA20.not_criticalCountConjecture_proved

set_option pp.all true in
#print NLA.RA20.HasCriticalCount
set_option pp.all true in
#print NLA.RA20.SmoothCriticalPoint
