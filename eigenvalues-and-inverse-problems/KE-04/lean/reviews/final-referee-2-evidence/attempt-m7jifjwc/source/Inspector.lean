import Solution
import Reference
import Lean.Util.FoldConsts
set_option leancert.trust "kernel"
set_option maxHeartbeats 4000000
set_option pp.universes true
set_option pp.proofs false
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

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  logInfo m!"LOCAL_ELABORATION_TRUST_LEVEL {env.header.trustLevel}"
  for n in env.header.moduleNames do logInfo m!"IMPORTED_MODULE {n}"
  let targets : List Name := [``NLA.KE04.real_matrix_semantics, ``NLA.KE04.krylov_range_semantics, ``NLA.KE04.krylov_nesting_and_shift, ``NLA.KE04.fullBlockDimension_iff_independent, ``NLA.KE04.fullBlockDimension_prefix, ``NLA.KE04.lastFullBlockIteration_exists, ``NLA.KE04.krylovBasis_exists, ``NLA.KE04.frameProjection_semantics, ``NLA.KE04.compression_semantics, ``NLA.KE04.orderedSpectrum_semantics, ``NLA.KE04.compression_basis_independent, ``NLA.KE04.interval_index_validity, ``NLA.KE04.quadratic_semantics, ``NLA.KE04.spectral_gap_quadratic_psd, ``NLA.KE04.spectral_window_subspace, ``NLA.KE04.krylov_intersection_nonzero, ``NLA.KE04.psd_zero_form_iff_kernel, ``NLA.KE04.compressedQuadratic_semantics, ``NLA.KE04.quadratic_forms_agree, ``NLA.KE04.later_quadratic_identity, ``NLA.KE04.fullRank_quadratic_nonannihilation, ``NLA.KE04.strictIntervalOccupancy, ``NLA.KE04.fullPrefix_implies_canonical, ``NLA.KE04.blockLanczosConjecture]
  for n in targets do
    let expected := ("NLA.KE04.Reference." ++ (n.toString.splitOn ".").getLast!).toName
    let some actualCI := env.find? n | throwError "No actual theorem {n}"
    let some refCI := env.find? expected | throwError "No reference theorem {expected}"
    unless actualCI.isTheorem do throwError "Not a theorem: {n}"
    liftTermElabM do
      unless ← Meta.isDefEq actualCI.type refCI.type do throwError "Type differs: {n}"
    let axs ← liftCoreM <| collectAxioms n
    for ax in axs do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unallowed axiom at actual target {n}: {ax}"
    let referenceAxioms ← liftCoreM <| collectAxioms expected
    unless referenceAxioms.contains ``sorryAx do throwError "Reference did not retain deliberate hole {expected}"
    logInfo m!"EXACT_FROZEN_TYPE {n}: {actualCI.type}"
    logInfo m!"REFERENCE_ONLY_PLACEHOLDER {expected}"
  let isProject := fun n : Name =>
    (n.toString.startsWith "NLA.KE04." && !n.toString.startsWith "NLA.KE04.Reference.") ||
    n.toString.startsWith "_private.NLA.KE04."
  let groups : List (String × List Name) :=
    [("FINAL_TARGET", [``NLA.KE04.blockLanczosConjecture]), ("ALL_EXPORTS", targets)]
  for (label, roots) in groups do
    let mut pending := roots
    let mut seen : List Name := []
    let mut used : List Name := []
    for _ in [:20000] do
      match pending with
      | [] => pure ()
      | n :: tail =>
        pending := tail
        unless seen.contains n do
          seen := n :: seen
          let some ci := env.find? n | throwError "Unknown reached declaration {n}"
          if ci.isUnsafe || ci.isPartial then throwError "Unsafe or partial {n}"
          let some body := ci.value? (allowOpaque := true) | throwError "Missing body {n}"
          let axs ← liftCoreM <| collectAxioms n
          for ax in axs do
            unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
              throwError "Nonstandard reached axiom {n}: {ax}"
          let ds := ci.type.getUsedConstants.toList ++ body.getUsedConstants.toList
          for dep in ds do
            if dep.toString.startsWith "NLA.KE04.Reference." || dep == ``sorryAx ||
                dep == ``Lean.ofReduceBool || dep == ``Lean.ofReduceNat || dep == ``Lean.trustCompiler then
              throwError "Forbidden reached dependency {dep} in {n}"
          used := ds ++ used
          pending := ds.filter isProject ++ pending
          logInfo m!"REACHED {label} {n}; AXIOMS {axs.toList}; DIRECT {ds}"
    unless pending.isEmpty do throwError "Traversal incomplete {label}"
    let requiredFinal : List Name := [
      ``NLA.KE04._proved.strictIntervalOccupancy,
      ``NLA.KE04._proved.interval_index_validity,
      ``NLA.KE04._proved.spectral_window_subspace,
      ``NLA.KE04._proved.spectral_gap_quadratic_psd,
      ``NLA.KE04._proved.krylov_intersection_nonzero,
      ``NLA.KE04._proved.quadratic_forms_agree,
      ``NLA.KE04._proved.later_quadratic_identity,
      ``NLA.KE04._proved.psd_zero_form_iff_kernel,
      ``NLA.KE04._proved.fullRank_quadratic_nonannihilation,
      ``NLA.KE04._proved.fullRank_krylov_eigenvector_zero,
      ``NLA.KE04._proved.blockShift_eq_smul_extend,
      ``NLA.KE04._proved.fullBlockDimension_prefix,
      ``NLA.KE04._proved.act_mem_krylov_succ,
      ``NLA.KE04._proved.krylov_mono,
      ``NLA.KE04._proved.orderedSpectrum_semantics,
      ``NLA.KE04._proved.compressedQuadratic_semantics,
      ``NLA.KE04.act, ``NLA.KE04.krylov, ``NLA.KE04.krylovCombination,
      ``NLA.KE04.FullBlockDimension, ``NLA.KE04.IsKrylovBasis,
      ``NLA.KE04.orderedEigenvalues, ``NLA.KE04.orderedEigenbasis,
      ``NLA.KE04.ritzValueAt, ``NLA.KE04.ritzValues,
      ``NLA.KE04.compression, ``NLA.KE04.quadraticMatrix,
      ``NLA.KE04.compressedQuadratic, ``NLA.KE04.IterationOccupancy,
      ``NLA.KE04.BlockLanczosConjecture, ``NLA.KE04.FullPrefixBlockLanczosClaim]
    let requiredAll : List Name := [
      ``NLA.KE04._proved.lastFullBlockIteration_exists,
      ``NLA.KE04._proved.submodule_frame_exists,
      ``NLA.KE04._proved.compression_basis_independent,
      ``Matrix.toEuclideanLin,
      ``Fintype.linearCombination,
      ``Submodule.finrank_sup_add_finrank_inf_eq,
      ``LinearMap.IsSymmetric.eigenvalues_antitone,
      ``LinearMap.IsSymmetric.roots_charpoly_eq_eigenvalues,
      ``Matrix.PosSemidef.dotProduct_mulVec_zero_iff]
    let required := requiredFinal ++ (if label == "ALL_EXPORTS" then requiredAll else [])
    for dep in required do
      unless used.contains dep || seen.contains dep do throwError "Unreached material dependency {label}: {dep}"
      logInfo m!"REQUIRED_DEPENDENCY {label} {dep}"
    logInfo m!"CLOSURE_TOTAL {label} reached={seen.length} required={required.length}"
