import NLA.KE04.Proof
import Lean.Util.FoldConsts
noncomputable section
open scoped BigOperators
open NLA.KE04
namespace KE04ProofExpected
def real_matrix_semantics : Prop := ∀ {n m : ℕ} (A : Mat n) (M : Rect n m),
(A.IsHermitian ↔ A.transpose = A) ∧
      (∀ (x : Vec m) i, act M x i = ∑ j, M i j * x j) ∧
      (M.transpose * M = 1 ↔ Orthonormal ℝ (column M))

def krylov_range_semantics : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ),
krylov A V ell = LinearMap.range (krylovCombination A V ell) ∧
      (∀ x, x ∈ krylov A V ell ↔ ∃ c : Fin ell × Fin p → ℝ,
        x = ∑ rc, c rc • column (A ^ rc.1.val * V) rc.2) ∧
      Module.finrank ℝ (krylov A V ell) ≤ ell * p

def krylov_nesting_and_shift : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p),
krylov A V 0 = ⊥ ∧ Monotone (krylov A V) ∧
      ∀ ell x, x ∈ krylov A V ell → act A x ∈ krylov A V (ell + 1)

def fullBlockDimension_iff_independent : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ),
(FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell)) ∧
      (FullColumnRank V ↔ FullBlockDimension A V 1)

def fullBlockDimension_prefix : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (s : ℕ) (hs : FullBlockDimension A V s),
∀ ell, ell ≤ s → FullBlockDimension A V ell ∧
      Function.Injective (krylovCombination A V ell)

def lastFullBlockIteration_exists : Prop := ∀ {n p : ℕ} (hp : 0 < p)
    (A : Mat n) (V : Rect n p) (hV : FullColumnRank V),
∃ s, 1 ≤ s ∧ LastFullBlockIteration A V s

def krylovBasis_exists : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (hfull : FullBlockDimension A V ell),
∃ Q : Rect n (ell * p), IsKrylovBasis A V ell Q

def frameProjection_semantics : Prop := ∀ {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1),
(frameProjection Q).IsHermitian ∧
      frameProjection Q * frameProjection Q = frameProjection Q ∧
      (∀ x, x ∈ columnSpace Q ↔ act (frameProjection Q) x = x) ∧
      ∀ x y, y ∈ columnSpace Q →
        inner ℝ y (x - act (frameProjection Q) x) = 0

def compression_semantics : Prop := ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1),
compression A Q = Q.transpose * A * Q ∧ (compression A Q).IsHermitian ∧
      ∀ x, x ∈ columnSpace Q →
        act Q (act (compression A Q) (act Q.transpose x)) =
          act (frameProjection Q) (act A x)

def orderedSpectrum_semantics : Prop := ∀ {m : ℕ} (M : Mat m) (hM : M.IsHermitian),
Monotone (orderedEigenvalues M hM) ∧
      (∀ r, act M (orderedEigenbasis M hM r) =
        orderedEigenvalues M hM r • orderedEigenbasis M hM r) ∧
      M.charpoly.roots = Finset.univ.val.map (orderedEigenvalues M hM) ∧
      ∀ i (hi : i < m), eigenvalueAt M hM i = orderedEigenvalues M hM ⟨i, hi⟩

def compression_basis_independent : Prop := ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q R : Rect n m) (hQ : Q.transpose * Q = 1) (hR : R.transpose * R = 1)
    (hspan : columnSpace Q = columnSpace R),
(∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R

def interval_index_validity : Prop := ∀ (k p i : ℕ) (hk : 1 ≤ k)
    (hi : 1 ≤ i) (hu : i ≤ (k - 1) * p),
2 ≤ k ∧ 0 < p ∧ i - 1 < k * p ∧ i + p - 1 < k * p

def quadratic_semantics : Prop := ∀ {m : ℕ} (M : Mat m) (a b : ℝ),
(monicQuadratic a b).Monic ∧ (monicQuadratic a b).natDegree = 2 ∧
      quadraticMatrix M a b = Polynomial.aeval M (monicQuadratic a b) ∧
      quadraticMatrix M a b = M ^ 2 - (a + b) • M + (a * b) • (1 : Mat m)

def spectral_gap_quadratic_psd : Prop := ∀ {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ) (hab : a ≤ b)
    (hgap : ∀ r, ¬ (a < orderedEigenvalues M hM r ∧ orderedEigenvalues M hM r < b)),
(quadraticMatrix M a b).PosSemidef

def spectral_window_subspace : Prop := ∀ {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) (i p : ℕ) (hi : i + p < m),
∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0

def krylov_intersection_nonzero : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 1 ≤ k) (hfull : FullBlockDimension A V k)
    (hprev : FullBlockDimension A V (k - 1)) (E : Submodule ℝ (Vec n))
    (hE : E ≤ krylov A V k) (hdim : Module.finrank ℝ E = p + 1),
∃ x : Vec n, x ≠ 0 ∧ x ∈ E ∧ x ∈ krylov A V (k - 1)

def psd_zero_form_iff_kernel : Prop := ∀ {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m),
form M x = 0 ↔ act M x = 0

def compressedQuadratic_semantics : Prop := ∀ {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (a b : ℝ),
(∀ x, form (compressedQuadratic A Q a b) x =
      form (quadraticMatrix (compression A Q) a b) (act Q.transpose x)) ∧
      ((quadraticMatrix (compression A Q) a b).PosSemidef →
        (compressedQuadratic A Q a b).PosSemidef)

def quadratic_forms_agree : Prop := ∀ {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j)
    (Qk : Rect n (k * p)) (Qj : Rect n (j * p))
    (hQk : IsKrylovBasis A V k Qk) (hQj : IsKrylovBasis A V j Qj)
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (a b : ℝ),
form (compressedQuadratic A Qk a b) x =
      form (compressedQuadratic A Qj a b) x

def later_quadratic_identity : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j) (Qj : Rect n (j * p))
    (hQj : IsKrylovBasis A V j Qj) (x : Vec n)
    (hx : x ∈ krylov A V (k - 1)) (a b : ℝ),
act (compressedQuadratic A Qj a b) x = act (quadraticMatrix A a b) x

def fullRank_quadratic_nonannihilation : Prop := ∀ {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 2 ≤ k) (hfull : FullBlockDimension A V (k + 1))
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (hne : x ≠ 0) (a b : ℝ),
act (quadraticMatrix A a b) x ≠ 0

def strictIntervalOccupancy : Prop := FullPrefixBlockLanczosClaim

def fullPrefix_implies_canonical : Prop := FullPrefixBlockLanczosClaim → BlockLanczosConjecture

def blockLanczosConjecture : Prop := BlockLanczosConjecture

end KE04ProofExpected
set_option leancert.trust "kernel"
set_option maxHeartbeats 1600000
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
  let targets : List (Name × Name) := [(``NLA.KE04.real_matrix_semantics, ``KE04ProofExpected.real_matrix_semantics), (``NLA.KE04.krylov_range_semantics, ``KE04ProofExpected.krylov_range_semantics), (``NLA.KE04.krylov_nesting_and_shift, ``KE04ProofExpected.krylov_nesting_and_shift), (``NLA.KE04.fullBlockDimension_iff_independent, ``KE04ProofExpected.fullBlockDimension_iff_independent), (``NLA.KE04.fullBlockDimension_prefix, ``KE04ProofExpected.fullBlockDimension_prefix), (``NLA.KE04.lastFullBlockIteration_exists, ``KE04ProofExpected.lastFullBlockIteration_exists), (``NLA.KE04.krylovBasis_exists, ``KE04ProofExpected.krylovBasis_exists), (``NLA.KE04.frameProjection_semantics, ``KE04ProofExpected.frameProjection_semantics), (``NLA.KE04.compression_semantics, ``KE04ProofExpected.compression_semantics), (``NLA.KE04.orderedSpectrum_semantics, ``KE04ProofExpected.orderedSpectrum_semantics), (``NLA.KE04.compression_basis_independent, ``KE04ProofExpected.compression_basis_independent), (``NLA.KE04.interval_index_validity, ``KE04ProofExpected.interval_index_validity), (``NLA.KE04.quadratic_semantics, ``KE04ProofExpected.quadratic_semantics), (``NLA.KE04.spectral_gap_quadratic_psd, ``KE04ProofExpected.spectral_gap_quadratic_psd), (``NLA.KE04.spectral_window_subspace, ``KE04ProofExpected.spectral_window_subspace), (``NLA.KE04.krylov_intersection_nonzero, ``KE04ProofExpected.krylov_intersection_nonzero), (``NLA.KE04.psd_zero_form_iff_kernel, ``KE04ProofExpected.psd_zero_form_iff_kernel), (``NLA.KE04.compressedQuadratic_semantics, ``KE04ProofExpected.compressedQuadratic_semantics), (``NLA.KE04.quadratic_forms_agree, ``KE04ProofExpected.quadratic_forms_agree), (``NLA.KE04.later_quadratic_identity, ``KE04ProofExpected.later_quadratic_identity), (``NLA.KE04.fullRank_quadratic_nonannihilation, ``KE04ProofExpected.fullRank_quadratic_nonannihilation), (``NLA.KE04.strictIntervalOccupancy, ``KE04ProofExpected.strictIntervalOccupancy), (``NLA.KE04.fullPrefix_implies_canonical, ``KE04ProofExpected.fullPrefix_implies_canonical), (``NLA.KE04.blockLanczosConjecture, ``KE04ProofExpected.blockLanczosConjecture)]
  for (actual, expected) in targets do
    let some ci := env.find? actual | throwError "Missing actual proof {actual}"
    let some expectedCI := env.find? expected | throwError "Missing exact target"
    let some expectedType := expectedCI.value? (allowOpaque := true) | throwError "Missing expected type"
    liftTermElabM do
      unless ← Lean.Meta.isDefEq ci.type expectedType do throwError "Frozen type mismatch {actual}"
    logInfo m!"EXACT_CONTRACT {actual}: {ci.type}"
  let isProject := fun n : Name => n.toString.startsWith "NLA.KE04." || n.toString.startsWith "_private.NLA.KE04."
  let mut pending := targets.map Prod.fst
  let mut seen : List Name := []
  let mut used : List Name := []
  for _ in [:6000] do
    match pending with
    | [] => pure ()
    | n :: rest =>
      pending := rest
      unless seen.contains n do
        seen := n :: seen
        let some ci := env.find? n | throwError "Missing project declaration {n}"
        if ci.isUnsafe || ci.isPartial then throwError "Unsafe/partial declaration {n}"
        let axs ← liftCoreM <| collectAxioms n
        for ax in axs do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Nonstandard actual axiom {n}: {ax}"
        let some body := ci.value? (allowOpaque := true) | throwError "Bodyless declaration {n}"
        let ds := ci.type.getUsedConstants.toList ++ body.getUsedConstants.toList
        used := ds ++ used
        pending := ds.filter isProject ++ pending
        logInfo m!"ACTUAL_PROJECT {n}: axioms={axs.toList}; dependencies={ds}"
  unless pending.isEmpty do throwError "Incomplete actual traversal"
  for bad in [``sorryAx, `Lean.ofReduceBool, `Lean.trustCompiler] do
    if used.contains bad then throwError "Forbidden dependency {bad}"
  let required := [``NLA.KE04._proved.strictIntervalOccupancy,
    ``NLA.KE04._proved.fullPrefix_implies_canonical,
    ``NLA.KE04._proved.fullRank_quadratic_nonannihilation,
    ``NLA.KE04._proved.fullRank_krylov_eigenvector_zero,
    ``NLA.KE04._proved.blockShift_eq_smul_extend,
    ``NLA.KE04._proved.krylov_intersection_nonzero,
    ``NLA.KE04._proved.spectral_window_subspace,
    ``NLA.KE04._proved.spectral_gap_quadratic_psd,
    ``NLA.KE04._proved.quadratic_forms_agree,
    ``NLA.KE04._proved.later_quadratic_identity,
    ``NLA.KE04._proved.psd_zero_form_iff_kernel,
    ``NLA.KE04._proved.psd_form_nonneg,
    ``NLA.KE04._proved.interval_index_validity,
    ``NLA.KE04._proved.fullBlockDimension_prefix,
    ``NLA.KE04._proved.krylov_mono,
    ``NLA.KE04._proved.act_mem_krylov_succ,
    ``NLA.KE04._proved.compression_action_coordinates,
    ``NLA.KE04._proved.compression_basis_independent,
    ``NLA.KE04._proved.submodule_frame_exists,
    ``NLA.KE04._proved.orderedSpectrum_semantics,
    ``NLA.KE04.act,
    ``NLA.KE04.columnSpace,
    ``NLA.KE04.krylov,
    ``NLA.KE04.krylovCombination,
    ``NLA.KE04.FullBlockDimension,
    ``NLA.KE04.IsKrylovBasis,
    ``NLA.KE04.compression,
    ``NLA.KE04.compressedQuadratic,
    ``NLA.KE04.quadraticMatrix,
    ``NLA.KE04.form,
    ``NLA.KE04.orderedEigenvalues,
    ``NLA.KE04.orderedEigenbasis,
    ``NLA.KE04.ritzValues,
    ``NLA.KE04.ritzValueAt,
    ``NLA.KE04.IterationOccupancy,
    ``NLA.KE04.FullPrefixBlockLanczosClaim,
    ``NLA.KE04.BlockLanczosConjecture]
  for dep in required do
    unless used.contains dep do throwError "Missing material dependency {dep}"
    logInfo m!"MATERIAL_DEPENDENCY {dep}"
  logInfo m!"FINAL_COUNTS contracts={targets.length}, closure={seen.length}, material={required.length}"
