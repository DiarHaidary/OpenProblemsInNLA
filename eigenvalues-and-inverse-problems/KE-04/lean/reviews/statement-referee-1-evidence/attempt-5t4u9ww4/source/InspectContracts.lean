/- Intentional Challenge admissions are checked as admissions, never proofs. -/
import Challenge
import Lean.Util.FoldConsts
set_option maxHeartbeats 2000000
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let targets : List Name := [``NLA.KE04.real_matrix_semantics,
    ``NLA.KE04.krylov_range_semantics,
    ``NLA.KE04.krylov_nesting_and_shift,
    ``NLA.KE04.fullBlockDimension_iff_independent,
    ``NLA.KE04.fullBlockDimension_prefix,
    ``NLA.KE04.lastFullBlockIteration_exists,
    ``NLA.KE04.krylovBasis_exists,
    ``NLA.KE04.frameProjection_semantics,
    ``NLA.KE04.compression_semantics,
    ``NLA.KE04.orderedSpectrum_semantics,
    ``NLA.KE04.compression_basis_independent,
    ``NLA.KE04.interval_index_validity,
    ``NLA.KE04.quadratic_semantics,
    ``NLA.KE04.spectral_gap_quadratic_psd,
    ``NLA.KE04.spectral_window_subspace,
    ``NLA.KE04.krylov_intersection_nonzero,
    ``NLA.KE04.psd_zero_form_iff_kernel,
    ``NLA.KE04.compressedQuadratic_semantics,
    ``NLA.KE04.quadratic_forms_agree,
    ``NLA.KE04.later_quadratic_identity,
    ``NLA.KE04.fullRank_quadratic_nonannihilation,
    ``NLA.KE04.strictIntervalOccupancy,
    ``NLA.KE04.fullPrefix_implies_canonical,
    ``NLA.KE04.blockLanczosConjecture]
  let expectedDefs : List Name := [``NLA.KE04.Vec,
    ``NLA.KE04.Rect,
    ``NLA.KE04.Mat,
    ``NLA.KE04.column,
    ``NLA.KE04.act,
    ``NLA.KE04.columnSpace,
    ``NLA.KE04.FullColumnRank,
    ``NLA.KE04.krylovColumns,
    ``NLA.KE04.krylov,
    ``NLA.KE04.krylovCombination,
    ``NLA.KE04.FullBlockDimension,
    ``NLA.KE04.LastFullBlockIteration,
    ``NLA.KE04.IsKrylovBasis,
    ``NLA.KE04.frameProjection,
    ``NLA.KE04.compression,
    ``NLA.KE04.orderedEigenvalues,
    ``NLA.KE04.orderedEigenbasis,
    ``NLA.KE04.eigenvalueAt,
    ``NLA.KE04.ritzValues,
    ``NLA.KE04.ritzValueAt,
    ``NLA.KE04.monicQuadratic,
    ``NLA.KE04.quadraticMatrix,
    ``NLA.KE04.compressedQuadratic,
    ``NLA.KE04.form,
    ``NLA.KE04.IterationOccupancy,
    ``NLA.KE04.FullPrefixBlockLanczosClaim,
    ``NLA.KE04.BlockLanczosConjecture]
  for name in targets do
    let some ci := env.find? name | throwError "Missing contract {name}"
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Contract is not a theorem declaration {name}"
    let axs ← liftCoreM <| collectAxioms name
    unless axs.contains ``sorryAx do throwError "Expected deliberate admission missing {name}"
    for dep in ci.type.getUsedConstants do
      if dep.toString.startsWith "NLA.KE04." then
        unless expectedDefs.contains dep do throwError "Contract type uses another admitted contract {name}: {dep}"
    logInfo m!"CONTRACT_TYPE_DIRECT {name}: {ci.type.getUsedConstants.toList}"
    logInfo m!"CONTRACT_ADMITTED {name}: {axs.toList}"
  logInfo m!"CONTRACT_INSPECTION_COMPLETE {targets.length}"

set_option pp.all true in
#print NLA.KE04.real_matrix_semantics

set_option pp.all true in
#print NLA.KE04.krylov_range_semantics

set_option pp.all true in
#print NLA.KE04.krylov_nesting_and_shift

set_option pp.all true in
#print NLA.KE04.fullBlockDimension_iff_independent

set_option pp.all true in
#print NLA.KE04.fullBlockDimension_prefix

set_option pp.all true in
#print NLA.KE04.lastFullBlockIteration_exists

set_option pp.all true in
#print NLA.KE04.krylovBasis_exists

set_option pp.all true in
#print NLA.KE04.frameProjection_semantics

set_option pp.all true in
#print NLA.KE04.compression_semantics

set_option pp.all true in
#print NLA.KE04.orderedSpectrum_semantics

set_option pp.all true in
#print NLA.KE04.compression_basis_independent

set_option pp.all true in
#print NLA.KE04.interval_index_validity

set_option pp.all true in
#print NLA.KE04.quadratic_semantics

set_option pp.all true in
#print NLA.KE04.spectral_gap_quadratic_psd

set_option pp.all true in
#print NLA.KE04.spectral_window_subspace

set_option pp.all true in
#print NLA.KE04.krylov_intersection_nonzero

set_option pp.all true in
#print NLA.KE04.psd_zero_form_iff_kernel

set_option pp.all true in
#print NLA.KE04.compressedQuadratic_semantics

set_option pp.all true in
#print NLA.KE04.quadratic_forms_agree

set_option pp.all true in
#print NLA.KE04.later_quadratic_identity

set_option pp.all true in
#print NLA.KE04.fullRank_quadratic_nonannihilation

set_option pp.all true in
#print NLA.KE04.strictIntervalOccupancy

set_option pp.all true in
#print NLA.KE04.fullPrefix_implies_canonical

set_option pp.all true in
#print NLA.KE04.blockLanczosConjecture
