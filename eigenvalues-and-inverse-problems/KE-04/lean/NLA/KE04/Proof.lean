import NLA.KE04.Completion

/-!
# KE-04: the complete approved theorem boundary

Every signature is copied from the independently approved original Challenge.
The implementation imports only completed proofs, never the reference Challenge.
Original mathematical proof: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA,
with substantial AI assistance. Final independent review remains a separate gate.
-/

noncomputable section
open scoped BigOperators
set_option leancert.trust "kernel"
namespace NLA.KE04

theorem real_matrix_semantics {n m : ℕ} (A : Mat n) (M : Rect n m) :
    (A.IsHermitian ↔ A.transpose = A) ∧
      (∀ (x : Vec m) i, act M x i = ∑ j, M i j * x j) ∧
      (M.transpose * M = 1 ↔ Orthonormal ℝ (column M)) := by
  exact @_proved.real_matrix_semantics n m A M

theorem krylov_range_semantics {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    krylov A V ell = LinearMap.range (krylovCombination A V ell) ∧
      (∀ x, x ∈ krylov A V ell ↔ ∃ c : Fin ell × Fin p → ℝ,
        x = ∑ rc, c rc • column (A ^ rc.1.val * V) rc.2) ∧
      Module.finrank ℝ (krylov A V ell) ≤ ell * p := by
  exact @_proved.krylov_range_semantics n p A V ell

theorem krylov_nesting_and_shift {n p : ℕ} (A : Mat n) (V : Rect n p) :
    krylov A V 0 = ⊥ ∧ Monotone (krylov A V) ∧
      ∀ ell x, x ∈ krylov A V ell → act A x ∈ krylov A V (ell + 1) := by
  exact @_proved.krylov_nesting_and_shift n p A V

theorem fullBlockDimension_iff_independent {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) :
    (FullBlockDimension A V ell ↔ LinearIndependent ℝ (krylovColumns A V ell)) ∧
      (FullColumnRank V ↔ FullBlockDimension A V 1) := by
  exact @_proved.fullBlockDimension_iff_independent n p A V ell

theorem fullBlockDimension_prefix {n p : ℕ} (A : Mat n) (V : Rect n p)
    (s : ℕ) (hs : FullBlockDimension A V s) :
    ∀ ell, ell ≤ s → FullBlockDimension A V ell ∧
      Function.Injective (krylovCombination A V ell) := by
  exact @_proved.fullBlockDimension_prefix n p A V s hs

theorem lastFullBlockIteration_exists {n p : ℕ} (hp : 0 < p)
    (A : Mat n) (V : Rect n p) (hV : FullColumnRank V) :
    ∃ s, 1 ≤ s ∧ LastFullBlockIteration A V s := by
  exact @_proved.lastFullBlockIteration_exists n p hp A V hV

theorem krylovBasis_exists {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (hfull : FullBlockDimension A V ell) :
    ∃ Q : Rect n (ell * p), IsKrylovBasis A V ell Q := by
  exact @_proved.krylovBasis_exists n p A V ell hfull

theorem frameProjection_semantics {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) :
    (frameProjection Q).IsHermitian ∧
      frameProjection Q * frameProjection Q = frameProjection Q ∧
      (∀ x, x ∈ columnSpace Q ↔ act (frameProjection Q) x = x) ∧
      ∀ x y, y ∈ columnSpace Q →
        inner ℝ y (x - act (frameProjection Q) x) = 0 := by
  exact @_proved.frameProjection_semantics n m Q hQ

theorem compression_semantics {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) :
    compression A Q = Q.transpose * A * Q ∧ (compression A Q).IsHermitian ∧
      ∀ x, x ∈ columnSpace Q →
        act Q (act (compression A Q) (act Q.transpose x)) =
          act (frameProjection Q) (act A x) := by
  exact @_proved.compression_semantics n m A hA Q hQ

theorem orderedSpectrum_semantics {m : ℕ} (M : Mat m) (hM : M.IsHermitian) :
    Monotone (orderedEigenvalues M hM) ∧
      (∀ r, act M (orderedEigenbasis M hM r) =
        orderedEigenvalues M hM r • orderedEigenbasis M hM r) ∧
      M.charpoly.roots = Finset.univ.val.map (orderedEigenvalues M hM) ∧
      ∀ i (hi : i < m), eigenvalueAt M hM i = orderedEigenvalues M hM ⟨i, hi⟩ := by
  exact @_proved.orderedSpectrum_semantics m M hM

theorem compression_basis_independent {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q R : Rect n m) (hQ : Q.transpose * Q = 1) (hR : R.transpose * R = 1)
    (hspan : columnSpace Q = columnSpace R) :
    (∃ O : Mat m, O.transpose * O = 1 ∧ R = Q * O ∧
      compression A R = O.transpose * compression A Q * O) ∧
      (compression A Q).charpoly = (compression A R).charpoly ∧
      ritzValues A hA Q = ritzValues A hA R := by
  exact @_proved.compression_basis_independent n m A hA Q R hQ hR hspan

theorem interval_index_validity (k p i : ℕ) (hk : 1 ≤ k)
    (hi : 1 ≤ i) (hu : i ≤ (k - 1) * p) :
    2 ≤ k ∧ 0 < p ∧ i - 1 < k * p ∧ i + p - 1 < k * p := by
  exact @_proved.interval_index_validity k p i hk hi hu

theorem quadratic_semantics {m : ℕ} (M : Mat m) (a b : ℝ) :
    (monicQuadratic a b).Monic ∧ (monicQuadratic a b).natDegree = 2 ∧
      quadraticMatrix M a b = Polynomial.aeval M (monicQuadratic a b) ∧
      quadraticMatrix M a b = M ^ 2 - (a + b) • M + (a * b) • (1 : Mat m) := by
  exact @_proved.quadratic_semantics m M a b

theorem spectral_gap_quadratic_psd {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ) (hab : a ≤ b)
    (hgap : ∀ r, ¬ (a < orderedEigenvalues M hM r ∧ orderedEigenvalues M hM r < b)) :
    (quadraticMatrix M a b).PosSemidef := by
  exact @_proved.spectral_gap_quadratic_psd m M hM a b hab hgap

theorem spectral_window_subspace {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) (i p : ℕ) (hi : i + p < m) :
    ∃ E : Submodule ℝ (Vec n), E ≤ columnSpace Q ∧ Module.finrank ℝ E = p + 1 ∧
      ∀ x, x ∈ E →
        form (compressedQuadratic A Q (ritzValueAt A hA Q i)
          (ritzValueAt A hA Q (i + p))) x ≤ 0 := by
  exact @_proved.spectral_window_subspace n m A hA Q hQ i p hi

theorem krylov_intersection_nonzero {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 1 ≤ k) (hfull : FullBlockDimension A V k)
    (hprev : FullBlockDimension A V (k - 1)) (E : Submodule ℝ (Vec n))
    (hE : E ≤ krylov A V k) (hdim : Module.finrank ℝ E = p + 1) :
    ∃ x : Vec n, x ≠ 0 ∧ x ∈ E ∧ x ∈ krylov A V (k - 1) := by
  exact @_proved.krylov_intersection_nonzero n p A V k hk hfull hprev E hE hdim

theorem psd_zero_form_iff_kernel {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m) :
    form M x = 0 ↔ act M x = 0 := by
  exact @_proved.psd_zero_form_iff_kernel m M hM x

theorem compressedQuadratic_semantics {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (a b : ℝ) :
    (∀ x, form (compressedQuadratic A Q a b) x =
      form (quadraticMatrix (compression A Q) a b) (act Q.transpose x)) ∧
      ((quadraticMatrix (compression A Q) a b).PosSemidef →
        (compressedQuadratic A Q a b).PosSemidef) := by
  exact @_proved.compressedQuadratic_semantics n m A Q a b

theorem quadratic_forms_agree {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j)
    (Qk : Rect n (k * p)) (Qj : Rect n (j * p))
    (hQk : IsKrylovBasis A V k Qk) (hQj : IsKrylovBasis A V j Qj)
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (a b : ℝ) :
    form (compressedQuadratic A Qk a b) x =
      form (compressedQuadratic A Qj a b) x := by
  exact @_proved.quadratic_forms_agree n p A hA V k j hk hkj Qk Qj hQk hQj x hx a b

theorem later_quadratic_identity {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k j : ℕ) (hk : 1 ≤ k) (hkj : k < j) (Qj : Rect n (j * p))
    (hQj : IsKrylovBasis A V j Qj) (x : Vec n)
    (hx : x ∈ krylov A V (k - 1)) (a b : ℝ) :
    act (compressedQuadratic A Qj a b) x = act (quadraticMatrix A a b) x := by
  exact @_proved.later_quadratic_identity n p A V k j hk hkj Qj hQj x hx a b

theorem fullRank_quadratic_nonannihilation {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 2 ≤ k) (hfull : FullBlockDimension A V (k + 1))
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (hne : x ≠ 0) (a b : ℝ) :
    act (quadraticMatrix A a b) x ≠ 0 := by
  exact @_proved.fullRank_quadratic_nonannihilation n p A V k hk hfull x hx hne a b

theorem strictIntervalOccupancy : FullPrefixBlockLanczosClaim := by
  exact @_proved.strictIntervalOccupancy

theorem fullPrefix_implies_canonical : FullPrefixBlockLanczosClaim → BlockLanczosConjecture := by
  exact @_proved.fullPrefix_implies_canonical

theorem blockLanczosConjecture : BlockLanczosConjecture := by
  exact @_proved.blockLanczosConjecture

#assert_trust kernel real_matrix_semantics
#print axioms real_matrix_semantics
#assert_trust kernel krylov_range_semantics
#print axioms krylov_range_semantics
#assert_trust kernel krylov_nesting_and_shift
#print axioms krylov_nesting_and_shift
#assert_trust kernel fullBlockDimension_iff_independent
#print axioms fullBlockDimension_iff_independent
#assert_trust kernel fullBlockDimension_prefix
#print axioms fullBlockDimension_prefix
#assert_trust kernel lastFullBlockIteration_exists
#print axioms lastFullBlockIteration_exists
#assert_trust kernel krylovBasis_exists
#print axioms krylovBasis_exists
#assert_trust kernel frameProjection_semantics
#print axioms frameProjection_semantics
#assert_trust kernel compression_semantics
#print axioms compression_semantics
#assert_trust kernel orderedSpectrum_semantics
#print axioms orderedSpectrum_semantics
#assert_trust kernel compression_basis_independent
#print axioms compression_basis_independent
#assert_trust kernel interval_index_validity
#print axioms interval_index_validity
#assert_trust kernel quadratic_semantics
#print axioms quadratic_semantics
#assert_trust kernel spectral_gap_quadratic_psd
#print axioms spectral_gap_quadratic_psd
#assert_trust kernel spectral_window_subspace
#print axioms spectral_window_subspace
#assert_trust kernel krylov_intersection_nonzero
#print axioms krylov_intersection_nonzero
#assert_trust kernel psd_zero_form_iff_kernel
#print axioms psd_zero_form_iff_kernel
#assert_trust kernel compressedQuadratic_semantics
#print axioms compressedQuadratic_semantics
#assert_trust kernel quadratic_forms_agree
#print axioms quadratic_forms_agree
#assert_trust kernel later_quadratic_identity
#print axioms later_quadratic_identity
#assert_trust kernel fullRank_quadratic_nonannihilation
#print axioms fullRank_quadratic_nonannihilation
#assert_trust kernel strictIntervalOccupancy
#print axioms strictIntervalOccupancy
#assert_trust kernel fullPrefix_implies_canonical
#print axioms fullPrefix_implies_canonical
#assert_trust kernel blockLanczosConjecture
#print axioms blockLanczosConjecture

end NLA.KE04
