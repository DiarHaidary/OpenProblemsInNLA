import NLA.KE04.Spectral
import Lean.Util.FoldConsts

/- The expected propositions below are literal frozen contract signatures.
No admitted Challenge declarations are imported by this inspector. -/
set_option maxHeartbeats 2000000
set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators

namespace NLA.KE04.SpectralExpected

def orderedSpectrum_semantics : Prop :=
  ∀ {m : ℕ} (M : Mat m) (hM : M.IsHermitian),
    Monotone (orderedEigenvalues M hM) ∧
      (∀ r, act M (orderedEigenbasis M hM r) =
        orderedEigenvalues M hM r • orderedEigenbasis M hM r) ∧
      M.charpoly.roots = Finset.univ.val.map (orderedEigenvalues M hM) ∧
      ∀ i (hi : i < m), eigenvalueAt M hM i = orderedEigenvalues M hM ⟨i, hi⟩

def quadratic_semantics : Prop :=
  ∀ {m : ℕ} (M : Mat m) (a b : ℝ),
    (monicQuadratic a b).Monic ∧ (monicQuadratic a b).natDegree = 2 ∧
      quadraticMatrix M a b = Polynomial.aeval M (monicQuadratic a b) ∧
      quadraticMatrix M a b = M ^ 2 - (a + b) • M + (a * b) • (1 : Mat m)

def spectral_gap_quadratic_psd : Prop :=
  ∀ {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ), a ≤ b →
    (∀ r, ¬ (a < orderedEigenvalues M hM r ∧ orderedEigenvalues M hM r < b)) →
    (quadraticMatrix M a b).PosSemidef

def psd_zero_form_iff_kernel : Prop :=
  ∀ {m : ℕ} (M : Mat m), M.PosSemidef → ∀ (x : Vec m),
    form M x = 0 ↔ act M x = 0

end NLA.KE04.SpectralExpected

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let pairs := [
    (``NLA.KE04._proved.orderedSpectrum_semantics, ``NLA.KE04.SpectralExpected.orderedSpectrum_semantics),
    (``NLA.KE04._proved.quadratic_semantics, ``NLA.KE04.SpectralExpected.quadratic_semantics),
    (``NLA.KE04._proved.spectral_gap_quadratic_psd, ``NLA.KE04.SpectralExpected.spectral_gap_quadratic_psd),
    (``NLA.KE04._proved.psd_zero_form_iff_kernel, ``NLA.KE04.SpectralExpected.psd_zero_form_iff_kernel)]
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
  let mut pending := pairs.map Prod.fst ++ [``NLA.KE04._proved.quadratic_apply_eigenvector]
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:8000] do
    match pending with
    | [] => pure ()
    | name :: rest =>
      pending := rest
      unless seen.contains name do
        if name.toString.startsWith "NLA.KE04.SpectralExpected." then
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
  let required := [``NLA.KE04.act, ``NLA.KE04.orderedEigenvalues,
    ``NLA.KE04.orderedEigenbasis, ``NLA.KE04.eigenvalueAt, ``NLA.KE04.monicQuadratic,
    ``NLA.KE04.quadraticMatrix, ``NLA.KE04.form,
    ``NLA.KE04._proved.orderedSpectrum_semantics,
    ``NLA.KE04._proved.quadratic_apply_eigenvector,
    ``LinearMap.IsSymmetric.eigenvalues, ``LinearMap.IsSymmetric.eigenvectorBasis,
    ``LinearMap.IsSymmetric.eigenvalues_antitone,
    ``LinearMap.IsSymmetric.apply_eigenvectorBasis,
    ``LinearMap.IsSymmetric.roots_charpoly_eq_eigenvalues,
    ``Matrix.charpoly_toLin, ``Multiset.map_univ_val_equiv,
    ``Polynomial.monic_X_sub_C, ``Polynomial.natDegree_mul,
    ``Polynomial.aeval_X, ``Polynomial.aeval_C,
    ``Matrix.toLpLin_mul_same, ``Matrix.PosSemidef.diagonal,
    ``LinearMap.posSemidef_toMatrix_iff, ``Matrix.isPositive_toEuclideanLin_iff,
    ``Matrix.PosSemidef.dotProduct_mulVec_zero_iff]
  for need in required do
    unless used.contains need do throwError "Missing material dependency {need}"
    logInfo m!"RETAINED_DEPENDENCY {need}"
  for forbidden in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains forbidden then throwError "Forbidden direct dependency {forbidden}"
  logInfo m!"PROJECT_COUNTS declarations={seen.length}, required={required.length}"

#assert_trust kernel NLA.KE04._proved.orderedSpectrum_semantics
#assert_trust kernel NLA.KE04._proved.quadratic_semantics
#assert_trust kernel NLA.KE04._proved.quadratic_apply_eigenvector
#assert_trust kernel NLA.KE04._proved.spectral_gap_quadratic_psd
#assert_trust kernel NLA.KE04._proved.psd_zero_form_iff_kernel
#print axioms NLA.KE04._proved.orderedSpectrum_semantics
#print axioms NLA.KE04._proved.quadratic_semantics
#print axioms NLA.KE04._proved.quadratic_apply_eigenvector
#print axioms NLA.KE04._proved.spectral_gap_quadratic_psd
#print axioms NLA.KE04._proved.psd_zero_form_iff_kernel

set_option pp.all true in
#print NLA.KE04.orderedEigenvalues
set_option pp.all true in
#print NLA.KE04.orderedEigenbasis
set_option pp.all true in
#print NLA.KE04.eigenvalueAt
set_option pp.all true in
#print NLA.KE04.monicQuadratic
set_option pp.all true in
#print NLA.KE04.quadraticMatrix
set_option pp.all true in
#print NLA.KE04.form
set_option pp.proofs true in
#print NLA.KE04._proved.orderedSpectrum_semantics
set_option pp.proofs true in
#print NLA.KE04._proved.quadratic_semantics
set_option pp.proofs true in
#print NLA.KE04._proved.quadratic_apply_eigenvector
set_option pp.proofs true in
#print NLA.KE04._proved.spectral_gap_quadratic_psd
set_option pp.proofs true in
#print NLA.KE04._proved.psd_zero_form_iff_kernel
