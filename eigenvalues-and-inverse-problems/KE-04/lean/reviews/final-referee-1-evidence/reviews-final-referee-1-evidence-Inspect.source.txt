/- Independent KE-04 final mathematical referee 1 diagnostic.
The reference retains the exact frozen signatures and 24 deliberate admitted
bodies, changed only into a new namespace. It is never imported by Solution.
All real type/body closures must reject that namespace and every axiom outside
the standard three. This local check is not the authoritative Linux Comparator.
-/
import Solution
import reviews.«final-referee-1-evidence».Reference
import Lean.Util.FoldConsts

set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs : List (Name × Name) := [
    (``NLA.KE04.real_matrix_semantics, ``NLA.KE04.FinalReferee1Reference.real_matrix_semantics),
    (``NLA.KE04.krylov_range_semantics, ``NLA.KE04.FinalReferee1Reference.krylov_range_semantics),
    (``NLA.KE04.krylov_nesting_and_shift, ``NLA.KE04.FinalReferee1Reference.krylov_nesting_and_shift),
    (``NLA.KE04.fullBlockDimension_iff_independent, ``NLA.KE04.FinalReferee1Reference.fullBlockDimension_iff_independent),
    (``NLA.KE04.fullBlockDimension_prefix, ``NLA.KE04.FinalReferee1Reference.fullBlockDimension_prefix),
    (``NLA.KE04.lastFullBlockIteration_exists, ``NLA.KE04.FinalReferee1Reference.lastFullBlockIteration_exists),
    (``NLA.KE04.krylovBasis_exists, ``NLA.KE04.FinalReferee1Reference.krylovBasis_exists),
    (``NLA.KE04.frameProjection_semantics, ``NLA.KE04.FinalReferee1Reference.frameProjection_semantics),
    (``NLA.KE04.compression_semantics, ``NLA.KE04.FinalReferee1Reference.compression_semantics),
    (``NLA.KE04.orderedSpectrum_semantics, ``NLA.KE04.FinalReferee1Reference.orderedSpectrum_semantics),
    (``NLA.KE04.compression_basis_independent, ``NLA.KE04.FinalReferee1Reference.compression_basis_independent),
    (``NLA.KE04.interval_index_validity, ``NLA.KE04.FinalReferee1Reference.interval_index_validity),
    (``NLA.KE04.quadratic_semantics, ``NLA.KE04.FinalReferee1Reference.quadratic_semantics),
    (``NLA.KE04.spectral_gap_quadratic_psd, ``NLA.KE04.FinalReferee1Reference.spectral_gap_quadratic_psd),
    (``NLA.KE04.spectral_window_subspace, ``NLA.KE04.FinalReferee1Reference.spectral_window_subspace),
    (``NLA.KE04.krylov_intersection_nonzero, ``NLA.KE04.FinalReferee1Reference.krylov_intersection_nonzero),
    (``NLA.KE04.psd_zero_form_iff_kernel, ``NLA.KE04.FinalReferee1Reference.psd_zero_form_iff_kernel),
    (``NLA.KE04.compressedQuadratic_semantics, ``NLA.KE04.FinalReferee1Reference.compressedQuadratic_semantics),
    (``NLA.KE04.quadratic_forms_agree, ``NLA.KE04.FinalReferee1Reference.quadratic_forms_agree),
    (``NLA.KE04.later_quadratic_identity, ``NLA.KE04.FinalReferee1Reference.later_quadratic_identity),
    (``NLA.KE04.fullRank_quadratic_nonannihilation, ``NLA.KE04.FinalReferee1Reference.fullRank_quadratic_nonannihilation),
    (``NLA.KE04.strictIntervalOccupancy, ``NLA.KE04.FinalReferee1Reference.strictIntervalOccupancy),
    (``NLA.KE04.fullPrefix_implies_canonical, ``NLA.KE04.FinalReferee1Reference.fullPrefix_implies_canonical),
    (``NLA.KE04.blockLanczosConjecture, ``NLA.KE04.FinalReferee1Reference.blockLanczosConjecture)]
  for (realName, refName) in pairs do
    let some realInfo := env.find? realName | throwError "Missing implementation {realName}"
    let some refInfo := env.find? refName | throwError "Missing reference {refName}"
    match realInfo with
    | .thmInfo _ => pure ()
    | _ => throwError "Expected actual theorem {realName}"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq realInfo.type refInfo.type do
        throwError "Actual signature differs from frozen contract: {realName}"
    let refAxioms ← liftCoreM <| collectAxioms refName
    unless refAxioms.contains ``sorryAx do
      throwError "Reference no longer contains its declared admission: {refName}"
    logInfo m!"EXACT_ELABORATED_SIGNATURE {realName} = {refName}"
    logInfo m!"EXPORTED_TYPE {realName}: {realInfo.type}"
  let exports := [``NLA.KE04.real_matrix_semantics,
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
  let sources := [``NLA.KE04.real_matrix_semantics,
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
    ``NLA.KE04.blockLanczosConjecture,
    ``NLA.KE04.Vec,
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
    ``NLA.KE04.BlockLanczosConjecture,
    ``NLA.KE04._proved.psd_form_nonneg,
    ``NLA.KE04._proved.strictIntervalOccupancy,
    ``NLA.KE04._proved.blockLanczosConjecture,
    ``NLA.KE04._proved.act_apply,
    ``NLA.KE04._proved.act_mul,
    ``NLA.KE04._proved.act_one,
    ``NLA.KE04._proved.inner_eq_sum,
    ``NLA.KE04._proved.inner_act_transpose,
    ``NLA.KE04._proved.inner_act_left,
    ``NLA.KE04._proved.inner_columns,
    ``NLA.KE04._proved.frame_iff_orthonormal,
    ``NLA.KE04._proved.real_matrix_semantics,
    ``NLA.KE04._proved.act_eq_column_sum,
    ``NLA.KE04._proved.columnSpace_eq_range_act,
    ``NLA.KE04._proved.act_transpose_act,
    ``NLA.KE04._proved.frameProjection_act,
    ``NLA.KE04._proved.frameProjection_fixed_iff,
    ``NLA.KE04._proved.frameProjection_semantics,
    ``NLA.KE04._proved.submodule_frame_exists,
    ``NLA.KE04._proved.krylovBasis_exists,
    ``NLA.KE04._proved.compression_semantics,
    ``NLA.KE04._proved.compressedQuadratic_semantics,
    ``NLA.KE04._proved.krylov_intersection_nonzero,
    ``NLA.KE04._proved.act_column_mul,
    ``NLA.KE04._proved.krylov_eq_range,
    ``NLA.KE04._proved.krylov_finrank_le,
    ``NLA.KE04._proved.krylov_range_semantics,
    ``NLA.KE04._proved.krylov_mono,
    ``NLA.KE04._proved.act_mem_krylov_succ,
    ``NLA.KE04._proved.krylov_nesting_and_shift,
    ``NLA.KE04._proved.fullBlockDimension_iff_columns,
    ``NLA.KE04._proved.fullColumnRank_iff_first,
    ``NLA.KE04._proved.fullBlockDimension_iff_independent,
    ``NLA.KE04._proved.fullBlockDimension_prefix,
    ``NLA.KE04._proved.fullBlockDimension_mul_le,
    ``NLA.KE04._proved.fullBlockDimension_index_le,
    ``NLA.KE04._proved.lastFullBlockIteration_exists,
    ``NLA.KE04._proved.blockExtend,
    ``NLA.KE04._proved.blockShift,
    ``NLA.KE04._proved.krylovCombination_extend,
    ``NLA.KE04._proved.krylovCombination_shift,
    ``NLA.KE04._proved.blockShift_eq_smul_extend,
    ``NLA.KE04._proved.fullRank_krylov_eigenvector_zero,
    ``NLA.KE04._proved.act_sub_smul_one,
    ``NLA.KE04._proved.fullRank_quadratic_nonannihilation,
    ``NLA.KE04._proved.orderedSpectrum_semantics,
    ``NLA.KE04._proved.quadratic_semantics,
    ``NLA.KE04._proved.quadratic_apply_eigenvector,
    ``NLA.KE04._proved.spectral_gap_quadratic_psd,
    ``NLA.KE04._proved.psd_zero_form_iff_kernel,
    ``NLA.KE04._proved.compression_basis_independent,
    ``NLA.KE04._proved.orthonormal_span_form_nonpos,
    ``NLA.KE04._proved.spectral_window_subspace,
    ``NLA.KE04._proved.frame_coordinates,
    ``NLA.KE04._proved.frame_inner,
    ``NLA.KE04._proved.compression_action_coordinates,
    ``NLA.KE04._proved.quadratic_action_expansion,
    ``NLA.KE04._proved.quadratic_form_expansion,
    ``NLA.KE04._proved.compressed_form_expansion,
    ``NLA.KE04._proved.compressed_action_identity,
    ``NLA.KE04._proved.quadratic_forms_agree,
    ``NLA.KE04._proved.later_quadratic_identity,
    ``NLA.KE04._proved.interval_index_validity,
    ``NLA.KE04._proved.fullPrefix_implies_canonical]
  let common := [``NLA.KE04._proved.blockLanczosConjecture,
    ``NLA.KE04._proved.strictIntervalOccupancy,
    ``NLA.KE04._proved.fullPrefix_implies_canonical,
    ``NLA.KE04._proved.interval_index_validity,
    ``NLA.KE04._proved.orderedSpectrum_semantics,
    ``NLA.KE04._proved.spectral_gap_quadratic_psd,
    ``NLA.KE04._proved.spectral_window_subspace,
    ``NLA.KE04._proved.orthonormal_span_form_nonpos,
    ``NLA.KE04._proved.quadratic_apply_eigenvector,
    ``NLA.KE04._proved.compressedQuadratic_semantics,
    ``NLA.KE04._proved.fullBlockDimension_prefix,
    ``NLA.KE04._proved.krylov_intersection_nonzero,
    ``NLA.KE04._proved.psd_zero_form_iff_kernel,
    ``NLA.KE04._proved.quadratic_forms_agree,
    ``NLA.KE04._proved.later_quadratic_identity,
    ``NLA.KE04._proved.fullRank_quadratic_nonannihilation,
    ``NLA.KE04._proved.fullRank_krylov_eigenvector_zero,
    ``NLA.KE04._proved.blockShift_eq_smul_extend,
    ``NLA.KE04._proved.krylovCombination_extend,
    ``NLA.KE04._proved.krylovCombination_shift,
    ``NLA.KE04._proved.compressed_form_expansion,
    ``NLA.KE04._proved.compressed_action_identity,
    ``NLA.KE04._proved.quadratic_form_expansion,
    ``NLA.KE04._proved.quadratic_action_expansion,
    ``NLA.KE04._proved.compression_action_coordinates,
    ``NLA.KE04._proved.frame_coordinates,
    ``NLA.KE04._proved.frame_inner,
    ``NLA.KE04._proved.frameProjection_fixed_iff,
    ``NLA.KE04._proved.columnSpace_eq_range_act,
    ``NLA.KE04._proved.act_mem_krylov_succ,
    ``NLA.KE04._proved.krylov_mono,
    ``NLA.KE04._proved.fullBlockDimension_iff_columns,
    ``NLA.KE04._proved.quadratic_semantics,
    ``LinearMap.IsSymmetric.eigenvalues_antitone,
    ``LinearMap.IsSymmetric.apply_eigenvectorBasis,
    ``LinearMap.IsSymmetric.roots_charpoly_eq_eigenvalues,
    ``Matrix.PosSemidef.dotProduct_mulVec_zero_iff,
    ``Matrix.isPositive_toEuclideanLin_iff,
    ``LinearMap.posSemidef_toMatrix_iff,
    ``Submodule.finrank_sup_add_finrank_inf_eq,
    ``linearIndependent_iff_injective_fintypeLinearCombination,
    ``finrank_span_eq_card]
  let extra := [``NLA.KE04._proved.lastFullBlockIteration_exists,
    ``NLA.KE04._proved.fullBlockDimension_index_le,
    ``NLA.KE04._proved.fullBlockDimension_mul_le,
    ``NLA.KE04._proved.fullColumnRank_iff_first,
    ``NLA.KE04._proved.krylovBasis_exists,
    ``NLA.KE04._proved.submodule_frame_exists,
    ``NLA.KE04._proved.compression_basis_independent,
    ``NLA.KE04._proved.frameProjection_semantics,
    ``NLA.KE04._proved.compression_semantics,
    ``NLA.KE04._proved.real_matrix_semantics,
    ``NLA.KE04._proved.krylov_range_semantics,
    ``NLA.KE04._proved.fullBlockDimension_iff_independent,
    ``NLA.KE04._proved.krylov_nesting_and_shift,
    ``stdOrthonormalBasis,
    ``LinearMap.IsSymmetric.eigenvalues_eq_eigenvalues_iff]
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." ||
    n.toString.startsWith "_private.NLA.KE04."
  for (label, starts) in [("FINAL", [``NLA.KE04.blockLanczosConjecture]),
      ("ALL", exports), ("SOURCE", sources)] do
    let mut todo := starts
    let mut seen : List Name := []
    let mut allDeps : List Name := []
    for _ in [:10000] do
      match todo with
      | [] => pure ()
      | name :: rest =>
        todo := rest
        unless seen.contains name do
          if name.toString.startsWith "NLA.KE04.FinalReferee1Reference." then
            throwError "Real proof reached admitted reference {name}"
          seen := name :: seen
          let some ci := env.find? name | throwError "Missing actual dependency {name}"
          if ci.isUnsafe || ci.isPartial then
            throwError "Unsafe/partial actual project dependency {name}"
          let axs ← liftCoreM <| collectAxioms name
          for ax in axs do
            unless [``propext, ``Quot.sound, ``Classical.choice].contains ax do
              throwError "Forbidden actual transitive axiom {name}: {ax}"
          let valueDeps ← match ci.value? (allowOpaque := true) with
            | some body => pure body.getUsedConstants.toList
            | none => match ci with
              | .inductInfo _ | .ctorInfo _ | .recInfo _ => pure []
              | _ => throwError "Unexplained bodyless declaration {name}"
          let ds := ci.type.getUsedConstants.toList ++ valueDeps
          allDeps := ds ++ allDeps
          let following := ds.filter isProject
          todo := following ++ todo
          logInfo m!"ACTUAL_EDGE {label} {name}: {following}"
          logInfo m!"ACTUAL_AXIOMS {label} {name}: {axs.toList}"
    unless todo.isEmpty do throwError "Incomplete traversal {label}"
    let must := common ++ if label == "FINAL" then [] else extra
    for need in must do
      unless allDeps.contains need do
        throwError "Required material bridge absent in {label}: {need}"
      logInfo m!"MATERIAL_BRIDGE {label}: {need}"
    logInfo m!"INDEPENDENT_COUNTS {label}: project={seen.length}, material={must.length}"

#assert_trust kernel NLA.KE04.real_matrix_semantics
#print axioms NLA.KE04.real_matrix_semantics

#assert_trust kernel NLA.KE04.krylov_range_semantics
#print axioms NLA.KE04.krylov_range_semantics

#assert_trust kernel NLA.KE04.krylov_nesting_and_shift
#print axioms NLA.KE04.krylov_nesting_and_shift

#assert_trust kernel NLA.KE04.fullBlockDimension_iff_independent
#print axioms NLA.KE04.fullBlockDimension_iff_independent

#assert_trust kernel NLA.KE04.fullBlockDimension_prefix
#print axioms NLA.KE04.fullBlockDimension_prefix

#assert_trust kernel NLA.KE04.lastFullBlockIteration_exists
#print axioms NLA.KE04.lastFullBlockIteration_exists

#assert_trust kernel NLA.KE04.krylovBasis_exists
#print axioms NLA.KE04.krylovBasis_exists

#assert_trust kernel NLA.KE04.frameProjection_semantics
#print axioms NLA.KE04.frameProjection_semantics

#assert_trust kernel NLA.KE04.compression_semantics
#print axioms NLA.KE04.compression_semantics

#assert_trust kernel NLA.KE04.orderedSpectrum_semantics
#print axioms NLA.KE04.orderedSpectrum_semantics

#assert_trust kernel NLA.KE04.compression_basis_independent
#print axioms NLA.KE04.compression_basis_independent

#assert_trust kernel NLA.KE04.interval_index_validity
#print axioms NLA.KE04.interval_index_validity

#assert_trust kernel NLA.KE04.quadratic_semantics
#print axioms NLA.KE04.quadratic_semantics

#assert_trust kernel NLA.KE04.spectral_gap_quadratic_psd
#print axioms NLA.KE04.spectral_gap_quadratic_psd

#assert_trust kernel NLA.KE04.spectral_window_subspace
#print axioms NLA.KE04.spectral_window_subspace

#assert_trust kernel NLA.KE04.krylov_intersection_nonzero
#print axioms NLA.KE04.krylov_intersection_nonzero

#assert_trust kernel NLA.KE04.psd_zero_form_iff_kernel
#print axioms NLA.KE04.psd_zero_form_iff_kernel

#assert_trust kernel NLA.KE04.compressedQuadratic_semantics
#print axioms NLA.KE04.compressedQuadratic_semantics

#assert_trust kernel NLA.KE04.quadratic_forms_agree
#print axioms NLA.KE04.quadratic_forms_agree

#assert_trust kernel NLA.KE04.later_quadratic_identity
#print axioms NLA.KE04.later_quadratic_identity

#assert_trust kernel NLA.KE04.fullRank_quadratic_nonannihilation
#print axioms NLA.KE04.fullRank_quadratic_nonannihilation

#assert_trust kernel NLA.KE04.strictIntervalOccupancy
#print axioms NLA.KE04.strictIntervalOccupancy

#assert_trust kernel NLA.KE04.fullPrefix_implies_canonical
#print axioms NLA.KE04.fullPrefix_implies_canonical

#assert_trust kernel NLA.KE04.blockLanczosConjecture
#print axioms NLA.KE04.blockLanczosConjecture

#assert_trust kernel NLA.KE04.Vec
#print axioms NLA.KE04.Vec

#assert_trust kernel NLA.KE04.Rect
#print axioms NLA.KE04.Rect

#assert_trust kernel NLA.KE04.Mat
#print axioms NLA.KE04.Mat

#assert_trust kernel NLA.KE04.column
#print axioms NLA.KE04.column

#assert_trust kernel NLA.KE04.act
#print axioms NLA.KE04.act

#assert_trust kernel NLA.KE04.columnSpace
#print axioms NLA.KE04.columnSpace

#assert_trust kernel NLA.KE04.FullColumnRank
#print axioms NLA.KE04.FullColumnRank

#assert_trust kernel NLA.KE04.krylovColumns
#print axioms NLA.KE04.krylovColumns

#assert_trust kernel NLA.KE04.krylov
#print axioms NLA.KE04.krylov

#assert_trust kernel NLA.KE04.krylovCombination
#print axioms NLA.KE04.krylovCombination

#assert_trust kernel NLA.KE04.FullBlockDimension
#print axioms NLA.KE04.FullBlockDimension

#assert_trust kernel NLA.KE04.LastFullBlockIteration
#print axioms NLA.KE04.LastFullBlockIteration

#assert_trust kernel NLA.KE04.IsKrylovBasis
#print axioms NLA.KE04.IsKrylovBasis

#assert_trust kernel NLA.KE04.frameProjection
#print axioms NLA.KE04.frameProjection

#assert_trust kernel NLA.KE04.compression
#print axioms NLA.KE04.compression

#assert_trust kernel NLA.KE04.orderedEigenvalues
#print axioms NLA.KE04.orderedEigenvalues

#assert_trust kernel NLA.KE04.orderedEigenbasis
#print axioms NLA.KE04.orderedEigenbasis

#assert_trust kernel NLA.KE04.eigenvalueAt
#print axioms NLA.KE04.eigenvalueAt

#assert_trust kernel NLA.KE04.ritzValues
#print axioms NLA.KE04.ritzValues

#assert_trust kernel NLA.KE04.ritzValueAt
#print axioms NLA.KE04.ritzValueAt

#assert_trust kernel NLA.KE04.monicQuadratic
#print axioms NLA.KE04.monicQuadratic

#assert_trust kernel NLA.KE04.quadraticMatrix
#print axioms NLA.KE04.quadraticMatrix

#assert_trust kernel NLA.KE04.compressedQuadratic
#print axioms NLA.KE04.compressedQuadratic

#assert_trust kernel NLA.KE04.form
#print axioms NLA.KE04.form

#assert_trust kernel NLA.KE04.IterationOccupancy
#print axioms NLA.KE04.IterationOccupancy

#assert_trust kernel NLA.KE04.FullPrefixBlockLanczosClaim
#print axioms NLA.KE04.FullPrefixBlockLanczosClaim

#assert_trust kernel NLA.KE04.BlockLanczosConjecture
#print axioms NLA.KE04.BlockLanczosConjecture

set_option pp.all true in
#check NLA.KE04.real_matrix_semantics

set_option pp.all true in
#check NLA.KE04.krylov_range_semantics

set_option pp.all true in
#check NLA.KE04.krylov_nesting_and_shift

set_option pp.all true in
#check NLA.KE04.fullBlockDimension_iff_independent

set_option pp.all true in
#check NLA.KE04.fullBlockDimension_prefix

set_option pp.all true in
#check NLA.KE04.lastFullBlockIteration_exists

set_option pp.all true in
#check NLA.KE04.krylovBasis_exists

set_option pp.all true in
#check NLA.KE04.frameProjection_semantics

set_option pp.all true in
#check NLA.KE04.compression_semantics

set_option pp.all true in
#check NLA.KE04.orderedSpectrum_semantics

set_option pp.all true in
#check NLA.KE04.compression_basis_independent

set_option pp.all true in
#check NLA.KE04.interval_index_validity

set_option pp.all true in
#check NLA.KE04.quadratic_semantics

set_option pp.all true in
#check NLA.KE04.spectral_gap_quadratic_psd

set_option pp.all true in
#check NLA.KE04.spectral_window_subspace

set_option pp.all true in
#check NLA.KE04.krylov_intersection_nonzero

set_option pp.all true in
#check NLA.KE04.psd_zero_form_iff_kernel

set_option pp.all true in
#check NLA.KE04.compressedQuadratic_semantics

set_option pp.all true in
#check NLA.KE04.quadratic_forms_agree

set_option pp.all true in
#check NLA.KE04.later_quadratic_identity

set_option pp.all true in
#check NLA.KE04.fullRank_quadratic_nonannihilation

set_option pp.all true in
#check NLA.KE04.strictIntervalOccupancy

set_option pp.all true in
#check NLA.KE04.fullPrefix_implies_canonical

set_option pp.all true in
#check NLA.KE04.blockLanczosConjecture

set_option pp.all true in
#print NLA.KE04.IterationOccupancy

set_option pp.all true in
#print NLA.KE04.FullPrefixBlockLanczosClaim

set_option pp.all true in
#print NLA.KE04.BlockLanczosConjecture

set_option pp.all true in
#print NLA.KE04.krylovColumns

set_option pp.all true in
#print NLA.KE04.krylov

set_option pp.all true in
#print NLA.KE04.krylovCombination

set_option pp.all true in
#print NLA.KE04.FullColumnRank

set_option pp.all true in
#print NLA.KE04.FullBlockDimension

set_option pp.all true in
#print NLA.KE04.LastFullBlockIteration

set_option pp.all true in
#print NLA.KE04.IsKrylovBasis

set_option pp.all true in
#print NLA.KE04.orderedEigenvalues

set_option pp.all true in
#print NLA.KE04.orderedEigenbasis

set_option pp.all true in
#print NLA.KE04.eigenvalueAt

set_option pp.all true in
#print NLA.KE04.frameProjection

set_option pp.all true in
#print NLA.KE04.compression

set_option pp.all true in
#print NLA.KE04.compressedQuadratic

set_option pp.all true in
#print NLA.KE04.form
