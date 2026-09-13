import NLA.KE04.Definitions

/-!
# KE-04: statement-only reference contracts

Every `sorry` is an intentional Challenge placeholder. A future proof module
must never import Challenge. No proof implementation or statement freeze has
been authorized; two independent approvals and coordinator acceptance are required.
-/

noncomputable section
open scoped BigOperators

namespace NLA.KE04.FinalReferee1Reference

/-- Real Hermitian symmetry and the L2 matrix action have their source meanings. -/
theorem real_matrix_semantics {n m : ℕ} (A : Mat n) (M : Rect n m) :
    (A.IsHermitian ↔ A.transpose = A) ∧
      (∀ (x : Vec m) i, act M x i = ∑ j, M i j * x j) ∧
      (M.transpose * M = 1 ↔ Orthonormal ℝ (column M)) := by sorry

/-- Actual range and coefficient description of the block Krylov matrix. -/
theorem krylov_range_semantics {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    krylov A V ell = LinearMap.range (krylovCombination A V ell) ∧
      (∀ x, x ∈ krylov A V ell ↔ ∃ c : Fin ell × Fin p → ℝ,
        x = ∑ rc, c rc • column (A ^ rc.1.val * V) rc.2) ∧
      Module.finrank ℝ (krylov A V ell) ≤ ell * p := by sorry

/-- Nesting and one-power propagation are derived from the actual columns. -/
theorem krylov_nesting_and_shift {n p : ℕ} (A : Mat n) (V : Rect n p) :
    krylov A V 0 = ⊥ ∧ Monotone (krylov A V) ∧
      ∀ ell x, x ∈ krylov A V ell → act A x ∈ krylov A V (ell + 1) := by sorry

/-- Full dimension is exactly independence of every actual block-power column. -/
theorem fullBlockDimension_iff_independent {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) :
    (FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell)) ∧
      (FullColumnRank V ↔ FullBlockDimension A V 1) := by sorry

/-- Full dimension at s supplies every preceding dimension and coefficient uniqueness. -/
theorem fullBlockDimension_prefix {n p : ℕ} (A : Mat n) (V : Rect n p)
    (s : ℕ) (hs : FullBlockDimension A V s) :
    ∀ ell, ell ≤ s → FullBlockDimension A V ell ∧
      Function.Injective (krylovCombination A V ell) := by sorry

/-- Positive block width is essential for existence of a largest index. -/
theorem lastFullBlockIteration_exists {n p : ℕ} (hp : 0 < p)
    (A : Mat n) (V : Rect n p) (hV : FullColumnRank V) :
    ∃ s, 1 ≤ s ∧ LastFullBlockIteration A V s := by sorry

/-- Orthonormal bases of the exact required size exist, rather than being a vacuous premise. -/
theorem krylovBasis_exists {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (hfull : FullBlockDimension A V ell) :
    ∃ Q : Rect n (ell * p), IsKrylovBasis A V ell Q := by sorry

/-- The frame matrix is the actual orthogonal projector onto its column space. -/
theorem frameProjection_semantics {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) :
    (frameProjection Q).IsHermitian ∧
      frameProjection Q * frameProjection Q = frameProjection Q ∧
      (∀ x, x ∈ columnSpace Q ↔ act (frameProjection Q) x = x) ∧
      ∀ x y, y ∈ columnSpace Q →
        inner ℝ y (x - act (frameProjection Q) x) = 0 := by sorry

/-- Genuine symmetric compression and exact representation of P A on its subspace. -/
theorem compression_semantics {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) :
    compression A Q = Q.transpose * A * Q ∧ (compression A Q).IsHermitian ∧
      ∀ x, x ∈ columnSpace Q →
        act Q (act (compression A Q) (act Q.transpose x)) =
          act (frameProjection Q) (act A x) := by sorry

/-- Increasing genuine eigenvalues, corresponding eigenvectors, and algebraic multiplicities. -/
theorem orderedSpectrum_semantics {m : ℕ} (M : Mat m) (hM : M.IsHermitian) :
    Monotone (orderedEigenvalues M hM) ∧
      (∀ r, act M (orderedEigenbasis M hM r) =
        orderedEigenvalues M hM r • orderedEigenbasis M hM r) ∧
      M.charpoly.roots = Finset.univ.val.map (orderedEigenvalues M hM) ∧
      ∀ i (hi : i < m), eigenvalueAt M hM i = orderedEigenvalues M hM ⟨i, hi⟩ := by sorry

/-- Independent orthonormal basis choices yield orthogonally similar compressions
and exactly the same ordered eigenvalue function, with repetitions retained. -/
theorem compression_basis_independent {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q R : Rect n m) (hQ : Q.transpose * Q = 1) (hR : R.transpose * R = 1)
    (hspan : columnSpace Q = columnSpace R) :
    (∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R := by sorry

/-- Every source interval endpoint lies in the genuine spectrum's index range.
The p=0 and k=1 source index ranges are empty; no endpoint separation is assumed. -/
theorem interval_index_validity (k p i : ℕ) (hk : 1 ≤ k)
    (hi : 1 ≤ i) (hu : i ≤ (k - 1) * p) :
    2 ≤ k ∧ 0 < p ∧ i - 1 < k * p ∧ i + p - 1 < k * p := by sorry

/-- The exact monic quadratic and its matrix evaluation; there is no interval computation. -/
theorem quadratic_semantics {m : ℕ} (M : Mat m) (a b : ℝ) :
    (monicQuadratic a b).Monic ∧ (monicQuadratic a b).natDegree = 2 ∧
      quadraticMatrix M a b = Polynomial.aeval M (monicQuadratic a b) ∧
      quadraticMatrix M a b = M ^ 2 - (a + b) • M + (a * b) • (1 : Mat m) := by sorry

/-- Absence from the strict open interval makes the actual later quadratic PSD.
The case a=b remains included. -/
theorem spectral_gap_quadratic_psd {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ) (hab : a ≤ b)
    (hgap : ∀ r, ¬ (a < orderedEigenvalues M hM r ∧ orderedEigenvalues M hM r < b)) :
    (quadraticMatrix M a b).PosSemidef := by sorry

/-- p+1 consecutive indexed eigenvectors supply the required subspace even when
their eigenvalues repeat. Its dimension and quadratic sign are conclusions. -/
theorem spectral_window_subspace {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) (i p : ℕ) (hi : i + p < m) :
    ∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0 := by sorry

/-- Dimension p+1 cannot avoid the previous Krylov space of codimension p. -/
theorem krylov_intersection_nonzero {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 1 ≤ k) (hfull : FullBlockDimension A V k)
    (hprev : FullBlockDimension A V (k - 1)) (E : Submodule ℝ (Vec n))
    (hE : E ≤ krylov A V k) (hdim : Module.finrank ℝ E = p + 1) :
    ∃ x : Vec n, x ≠ 0 ∧ x ∈ E ∧ x ∈ krylov A V (k - 1) := by sorry

/-- Genuine PSD, including singular PSD, has zero quadratic form exactly on its kernel. -/
theorem psd_zero_form_iff_kernel {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m) :
    form M x = 0 ↔ act M x = 0 := by sorry

/-- Lifting a compressed quadratic preserves its PSD property and its quadratic form. -/
theorem compressedQuadratic_semantics {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (a b : ℝ) :
    (∀ x, form (compressedQuadratic A Q a b) x =
      form (quadraticMatrix (compression A Q) a b) (act Q.transpose x)) ∧
      ((quadraticMatrix (compression A Q) a b).PosSemidef →
        (compressedQuadratic A Q a b).PosSemidef) := by sorry

/-- On K_(k-1), the earlier and later quadratic forms agree. This does not
assert equality of the earlier squared compression with A^2. -/
theorem quadratic_forms_agree {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j)
    (Qk : Rect n (k * p)) (Qj : Rect n (j * p))
    (hQk : IsKrylovBasis A V k Qk) (hQj : IsKrylovBasis A V j Qj)
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (a b : ℝ) :
    form (compressedQuadratic A Qk a b) x =
      form (compressedQuadratic A Qj a b) x := by sorry

/-- The later compression contains x, Ax, A^2x and therefore acts as q(A) on x. -/
theorem later_quadratic_identity {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j) (Qj : Rect n (j * p))
    (hQj : IsKrylovBasis A V j Qj) (x : Vec n)
    (hx : x ∈ krylov A V (k - 1)) (a b : ℝ) :
    act (compressedQuadratic A Qj a b) x = act (quadraticMatrix A a b) x := by sorry

/-- Full block rank, not an assumed annihilation exclusion, supplies the contradiction. -/
theorem fullRank_quadratic_nonannihilation {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 2 ≤ k) (hfull : FullBlockDimension A V (k + 1))
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (hne : x ≠ 0) (a b : ℝ) :
    act (quadraticMatrix A a b) x ≠ 0 := by sorry

/-- Complete strict occupancy under the stronger arbitrary-full-prefix hypothesis. -/
theorem strictIntervalOccupancy : FullPrefixBlockLanczosClaim := by sorry

/-- Full-prefix occupancy implies exactly the source's maximal-s formulation. -/
theorem fullPrefix_implies_canonical : FullPrefixBlockLanczosClaim → BlockLanczosConjecture := by sorry

/-- The complete original all-dimensional, all-index, arbitrary-basis KE-04 claim. -/
theorem blockLanczosConjecture : BlockLanczosConjecture := by sorry

end NLA.KE04.FinalReferee1Reference
