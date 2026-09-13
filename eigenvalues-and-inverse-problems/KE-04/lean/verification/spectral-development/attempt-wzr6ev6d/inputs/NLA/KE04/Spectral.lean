import NLA.KE04.Definitions
import LeanCert.Tactic.Verification
import Mathlib.Tactic

/-!
# KE-04: ordered spectral and quadratic semantics

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted formalization after the accepted statement gate.

The underlying mathematical argument is Matthew J. Colbrook's KE-04 proof.
These helpers use Mathlib's self-adjoint spectral theorem, retaining the full
root multiset and the matched orthonormal basis when reversing the order.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators

namespace NLA.KE04._proved

theorem orderedSpectrum_semantics {m : ℕ} (M : Mat m) (hM : M.IsHermitian) :
    Monotone (orderedEigenvalues M hM) ∧
      (∀ r, act M (orderedEigenbasis M hM r) =
        orderedEigenvalues M hM r • orderedEigenbasis M hM r) ∧
      M.charpoly.roots = Finset.univ.val.map (orderedEigenvalues M hM) ∧
      ∀ i (hi : i < m), eigenvalueAt M hM i = orderedEigenvalues M hM ⟨i, hi⟩ := by
  let hT := Matrix.isSymmetric_toEuclideanLin_iff.mpr hM
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i j hij
    exact hT.eigenvalues_antitone finrank_euclideanSpace_fin (Fin.rev_le_rev.mpr hij)
  · intro r
    simp [orderedEigenbasis, orderedEigenvalues, act]
  · have hr : M.charpoly.roots = Finset.univ.val.map
        (hT.eigenvalues finrank_euclideanSpace_fin) := by
      simpa only [Matrix.toEuclideanLin_eq_toLin_orthonormal, Matrix.charpoly_toLin,
        Function.comp_def, RCLike.ofReal_real_eq_id, id_eq] using
        hT.roots_charpoly_eq_eigenvalues finrank_euclideanSpace_fin
    rw [hr]
    change _ = Finset.univ.val.map
      ((hT.eigenvalues finrank_euclideanSpace_fin) ∘ (Fin.revPerm : Fin m ≃ Fin m))
    rw [← Multiset.map_map, Multiset.map_univ_val_equiv]
  · intro i hi
    simp [eigenvalueAt, hi]

theorem quadratic_semantics {m : ℕ} (M : Mat m) (a b : ℝ) :
    (monicQuadratic a b).Monic ∧ (monicQuadratic a b).natDegree = 2 ∧
      quadraticMatrix M a b = Polynomial.aeval M (monicQuadratic a b) ∧
      quadraticMatrix M a b = M ^ 2 - (a + b) • M + (a * b) • (1 : Mat m) := by
  refine ⟨(Polynomial.monic_X_sub_C a).mul (Polynomial.monic_X_sub_C b), ?_, ?_, ?_⟩
  · rw [monicQuadratic, Polynomial.natDegree_mul (Polynomial.X_sub_C_ne_zero a)
      (Polynomial.X_sub_C_ne_zero b), Polynomial.natDegree_X_sub_C,
      Polynomial.natDegree_X_sub_C]
  · simp [quadraticMatrix, monicQuadratic, Algebra.algebraMap_eq_smul_one]
  · simp only [quadraticMatrix, mul_sub, sub_mul, mul_smul_comm, smul_mul_assoc,
      mul_one, one_mul, smul_sub, smul_smul, add_smul, pow_two]
    module

/-- Applying the quadratic to any eigenvector uses its original eigenvalue. -/
theorem quadratic_apply_eigenvector {m : ℕ} (M : Mat m) (a b mu : ℝ) (v : Vec m)
    (hv : act M v = mu • v) :
    act (quadraticMatrix M a b) v = ((mu - a) * (mu - b)) • v := by
  change Matrix.toLpLin 2 2 M v = mu • v at hv
  simp only [act, quadraticMatrix, Matrix.toLpLin_mul_same, map_sub, map_smul,
    Matrix.toLpLin_one, LinearMap.comp_apply, LinearMap.sub_apply,
    LinearMap.smul_apply, LinearMap.id_apply]
  rw [hv, map_sub, map_smul, map_smul, hv]
  module

theorem spectral_gap_quadratic_psd {m : ℕ} (M : Mat m) (hM : M.IsHermitian)
    (a b : ℝ) (hab : a ≤ b)
    (hgap : ∀ r, ¬ (a < orderedEigenvalues M hM r ∧ orderedEigenvalues M hM r < b)) :
    (quadraticMatrix M a b).PosSemidef := by
  let B := orderedEigenbasis M hM
  let d := fun r => (orderedEigenvalues M hM r - a) * (orderedEigenvalues M hM r - b)
  have hd : ∀ r, 0 ≤ d r := by
    intro r
    by_cases h : orderedEigenvalues M hM r ≤ a
    · exact mul_nonneg_of_nonpos_of_nonpos (sub_nonpos.mpr h)
        (sub_nonpos.mpr (h.trans hab))
    · have hb : b ≤ orderedEigenvalues M hM r := by
        by_contra hn
        exact hgap r ⟨lt_of_not_ge h, lt_of_not_ge hn⟩
      exact mul_nonneg (sub_nonneg.mpr (hab.trans hb)) (sub_nonneg.mpr hb)
  have heig (r : Fin m) : act (quadraticMatrix M a b) (B r) = d r • B r :=
    quadratic_apply_eigenvector M a b _ _ ((orderedSpectrum_semantics M hM).2.1 r)
  have hdiag : LinearMap.toMatrix B.toBasis B.toBasis (act (quadraticMatrix M a b)) =
      Matrix.diagonal d := by
    ext i j
    simp [LinearMap.toMatrix_apply, heig, Matrix.diagonal_apply]
    split_ifs <;> simp_all
  apply Matrix.isPositive_toEuclideanLin_iff.mp
  apply (LinearMap.posSemidef_toMatrix_iff B).mp
  rw [show Matrix.toEuclideanLin (quadraticMatrix M a b) = act (quadraticMatrix M a b)
    from rfl, hdiag]
  exact Matrix.PosSemidef.diagonal hd

theorem psd_zero_form_iff_kernel {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m) :
    form M x = 0 ↔ act M x = 0 := by
  simpa [form, act, EuclideanSpace.inner_eq_star_dotProduct, Matrix.ofLp_toLpLin,
    Matrix.toLin'_apply, ← WithLp.ofLp_eq_zero, dotProduct_comm] using
      hM.dotProduct_mulVec_zero_iff (WithLp.ofLp x)

#assert_trust kernel orderedSpectrum_semantics
#assert_trust kernel quadratic_semantics
#assert_trust kernel quadratic_apply_eigenvector
#assert_trust kernel spectral_gap_quadratic_psd
#assert_trust kernel psd_zero_form_iff_kernel
#print axioms orderedSpectrum_semantics
#print axioms quadratic_semantics
#print axioms quadratic_apply_eigenvector
#print axioms spectral_gap_quadratic_psd
#print axioms psd_zero_form_iff_kernel

end NLA.KE04._proved
