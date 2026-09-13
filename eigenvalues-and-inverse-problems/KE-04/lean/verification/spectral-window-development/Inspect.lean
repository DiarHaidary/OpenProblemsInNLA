import NLA.KE04.SpectralWindow
import Lean.Util.FoldConsts

/- The expected propositions below are literal frozen contract signatures.
No admitted Challenge declarations are imported by this inspector. -/
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators

namespace NLA.KE04.SpectralWindowExpected

def compression_basis_independent : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian) (Q R : Rect n m),
    Q.transpose * Q = 1 → R.transpose * R = 1 → columnSpace Q = columnSpace R →
    (∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R

def spectral_window_subspace : Prop :=
  ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian) (Q : Rect n m),
    Q.transpose * Q = 1 → ∀ (i p : ℕ), i + p < m →
    ∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0

end NLA.KE04.SpectralWindowExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [
    (``NLA.KE04._proved.compression_basis_independent, ``NLA.KE04.SpectralWindowExpected.compression_basis_independent),
    (``NLA.KE04._proved.spectral_window_subspace, ``NLA.KE04.SpectralWindowExpected.spectral_window_subspace)]
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
  let mut pending := pairs.map Prod.fst ++ [``NLA.KE04._proved.orthonormal_span_form_nonpos]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.KE04.SpectralWindowExpected." then
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
  let required := [``NLA.KE04._proved.act_mul,
    ``NLA.KE04._proved.act_transpose_act,
    ``NLA.KE04._proved.inner_act_left,
    ``NLA.KE04._proved.columnSpace_eq_range_act,
    ``NLA.KE04._proved.frameProjection_fixed_iff,
    ``NLA.KE04._proved.frameProjection_act,
    ``NLA.KE04._proved.orderedSpectrum_semantics,
    ``NLA.KE04._proved.quadratic_apply_eigenvector,
    ``NLA.KE04._proved.orthonormal_span_form_nonpos,
    ``NLA.KE04.compression,
    ``NLA.KE04.compressedQuadratic,
    ``NLA.KE04.ritzValues,
    ``NLA.KE04.ritzValueAt,
    ``NLA.KE04.orderedEigenvalues,
    ``NLA.KE04.orderedEigenbasis,
    ``NLA.KE04.columnSpace,
    ``Matrix.charpoly_mul_comm,
    ``Matrix.charpoly_toLin,
    ``mul_eq_one_comm,
    ``LinearMap.IsSymmetric.eigenvalues_eq_eigenvalues_iff,
    ``Orthonormal.comp,
    ``Orthonormal.linearIndependent,
    ``Orthonormal.inner_sum,
    ``finrank_span_eq_card,
    ``Submodule.mem_span_range_iff_exists_fun]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.KE04._proved.compression_basis_independent
#print axioms NLA.KE04._proved.compression_basis_independent
#assert_trust kernel NLA.KE04._proved.orthonormal_span_form_nonpos
#print axioms NLA.KE04._proved.orthonormal_span_form_nonpos
#assert_trust kernel NLA.KE04._proved.spectral_window_subspace
#print axioms NLA.KE04._proved.spectral_window_subspace
set_option pp.all true in
#print NLA.KE04.orderedEigenvalues
set_option pp.all true in
#print NLA.KE04.orderedEigenbasis
set_option pp.all true in
#print NLA.KE04.ritzValues
set_option pp.all true in
#print NLA.KE04.ritzValueAt
set_option pp.all true in
#print NLA.KE04.compression
set_option pp.all true in
#print NLA.KE04.compressedQuadratic
set_option pp.proofs true in
#print NLA.KE04._proved.compression_basis_independent
set_option pp.proofs true in
#print NLA.KE04._proved.orthonormal_span_form_nonpos
set_option pp.proofs true in
#print NLA.KE04._proved.spectral_window_subspace
