import NLA.KE04.Completion
import Lean.Util.FoldConsts

/- The expected propositions below are literal frozen contract signatures.
No admitted Challenge declarations are imported by this inspector. -/
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators

namespace NLA.KE04.CompletionExpected
def strictIntervalOccupancy : Prop := FullPrefixBlockLanczosClaim
def blockLanczosConjecture : Prop := BlockLanczosConjecture
end NLA.KE04.CompletionExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [
    (``NLA.KE04._proved.strictIntervalOccupancy, ``NLA.KE04.CompletionExpected.strictIntervalOccupancy),
    (``NLA.KE04._proved.blockLanczosConjecture, ``NLA.KE04.CompletionExpected.blockLanczosConjecture)]
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
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  let mut pending := pairs.map Prod.fst ++ [``NLA.KE04._proved.psd_form_nonneg]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.KE04.CompletionExpected." then
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
        logInfo m!"ALL_DIRECT_DEPENDENCIES {name}: {deps}"
        pending := follow ++ pending
  unless pending.isEmpty do throwError "Incomplete traversal"
  let required := [``NLA.KE04.IterationOccupancy,
    ``NLA.KE04.FullPrefixBlockLanczosClaim,
    ``NLA.KE04.BlockLanczosConjecture,
    ``NLA.KE04.FullColumnRank,
    ``NLA.KE04.FullBlockDimension,
    ``NLA.KE04.LastFullBlockIteration,
    ``NLA.KE04._proved.interval_index_validity,
    ``NLA.KE04._proved.orderedSpectrum_semantics,
    ``NLA.KE04._proved.spectral_gap_quadratic_psd,
    ``NLA.KE04._proved.compressedQuadratic_semantics,
    ``NLA.KE04._proved.spectral_window_subspace,
    ``NLA.KE04._proved.fullBlockDimension_prefix,
    ``NLA.KE04._proved.krylov_intersection_nonzero,
    ``NLA.KE04._proved.quadratic_forms_agree,
    ``NLA.KE04._proved.psd_form_nonneg,
    ``NLA.KE04._proved.psd_zero_form_iff_kernel,
    ``NLA.KE04._proved.later_quadratic_identity,
    ``NLA.KE04._proved.fullRank_quadratic_nonannihilation,
    ``NLA.KE04._proved.fullPrefix_implies_canonical,
    ``NLA.KE04._proved.strictIntervalOccupancy,
    ``Matrix.isPositive_toEuclideanLin_iff,
    ``LinearMap.IsPositive.inner_nonneg_right]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.KE04._proved.strictIntervalOccupancy
#print axioms NLA.KE04._proved.strictIntervalOccupancy
#assert_trust kernel NLA.KE04._proved.blockLanczosConjecture
#print axioms NLA.KE04._proved.blockLanczosConjecture
#assert_trust kernel NLA.KE04._proved.psd_form_nonneg
#print axioms NLA.KE04._proved.psd_form_nonneg
set_option pp.all true in
#print NLA.KE04.IterationOccupancy
set_option pp.all true in
#print NLA.KE04.FullPrefixBlockLanczosClaim
set_option pp.all true in
#print NLA.KE04.BlockLanczosConjecture
set_option pp.all true in
#print NLA.KE04.FullBlockDimension
set_option pp.all true in
#print NLA.KE04.FullColumnRank
set_option pp.all true in
#print NLA.KE04.LastFullBlockIteration
set_option pp.all true in
#print NLA.KE04.IsKrylovBasis
set_option pp.proofs true in
#print NLA.KE04._proved.strictIntervalOccupancy
set_option pp.proofs true in
#print NLA.KE04._proved.blockLanczosConjecture
set_option pp.proofs true in
#print NLA.KE04._proved.psd_form_nonneg
