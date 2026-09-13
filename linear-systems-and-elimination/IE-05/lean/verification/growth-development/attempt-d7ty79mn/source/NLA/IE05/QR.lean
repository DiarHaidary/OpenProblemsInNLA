import NLA.IE05.Scaling
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

/-!
# IE-05: the actual normalized Gram--Schmidt QR factor

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted formalization of the approved statement boundary.
-/

set_option leancert.trust "kernel"

noncomputable section
open scoped BigOperators
open InnerProductSpace

namespace NLA.IE05._proved

theorem euclideanColumns_inner {n : ℕ} (A B : Mat n) (i j : Fin n) :
    inner ℝ (euclideanColumns A i) (euclideanColumns B j) =
      (A.transpose * B) i j := by
  simp [euclideanColumns, PiLp.inner_apply, Matrix.mul_apply,
    Matrix.transpose_apply, mul_comm]

theorem orthogonal_iff_orthonormal_columns {n : ℕ} (Q : Mat n) :
    Orthogonal Q ↔ Orthonormal ℝ (euclideanColumns Q) := by
  rw [orthonormal_iff_ite]
  simp only [euclideanColumns_inner]
  constructor
  · intro h i j
    simpa [Matrix.one_apply] using congrArg (fun M : Mat n => M i j) h
  · intro h
    ext i j
    exact h i j

theorem euclideanColumns_linearIndependent {n : ℕ} (A : Mat n) (hA : A.det ≠ 0) :
    LinearIndependent ℝ (euclideanColumns A) := by
  exact (Matrix.linearIndependent_cols_of_det_ne_zero hA).map'
    (WithLp.linearEquiv 2 ℝ (Fin n → ℝ)).symm.toLinearMap
    (LinearMap.ker_eq_bot.mpr (WithLp.linearEquiv 2 ℝ (Fin n → ℝ)).symm.injective)

theorem euclideanColumns_normalizedQRQ {n : ℕ} (A : Mat n) (j : Fin n) :
    euclideanColumns (normalizedQRQ A) j =
      gramSchmidtNormed ℝ (euclideanColumns A) j := by
  ext i
  rfl

theorem normalizedQRQ_orthogonal {n : ℕ} (A : Mat n) (hA : A.det ≠ 0) :
    Orthogonal (normalizedQRQ A) := by
  rw [orthogonal_iff_orthonormal_columns]
  have hfun : euclideanColumns (normalizedQRQ A) =
      gramSchmidtNormed ℝ (euclideanColumns A) :=
    funext (euclideanColumns_normalizedQRQ A)
  rw [hfun]
  exact gramSchmidtNormed_orthonormal (euclideanColumns_linearIndependent A hA)

theorem gramSchmidt_inner_original {n : ℕ}
    (f : Fin n → EuclideanSpace ℝ (Fin n)) (j : Fin n) :
    inner ℝ (gramSchmidt ℝ f j) (f j) = ‖gramSchmidt ℝ f j‖ ^ 2 := by
  rw [gramSchmidt_def'' ℝ f j, inner_add_right, inner_sum]
  simp only [RCLike.ofReal_real_eq_id, id_eq]
  have hz : (∑ i ∈ Finset.Iio j,
      inner ℝ (gramSchmidt ℝ f j)
        ((inner ℝ (gramSchmidt ℝ f i) (f j) / ‖gramSchmidt ℝ f i‖ ^ 2) •
          gramSchmidt ℝ f i)) = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    rw [inner_smul_right,
      gramSchmidt_orthogonal ℝ f (ne_of_gt (Finset.mem_Iio.mp hi)), mul_zero]
  rw [hz, add_zero, real_inner_self_eq_norm_sq]

theorem normalizedQRQ_upper {n : ℕ} (A : Mat n) :
    UpperTriangular ((normalizedQRQ A).transpose * A) := by
  intro i j hji
  rw [← euclideanColumns_inner, euclideanColumns_normalizedQRQ,
    gramSchmidtNormed, real_inner_smul_left,
    gramSchmidt_inv_triangular ℝ (euclideanColumns A) hji, mul_zero]

theorem normalizedQRQ_diagonal_pos {n : ℕ} (A : Mat n) (hA : A.det ≠ 0)
    (i : Fin n) : 0 < ((normalizedQRQ A).transpose * A) i i := by
  rw [← euclideanColumns_inner, euclideanColumns_normalizedQRQ,
    gramSchmidtNormed, real_inner_smul_left, gramSchmidt_inner_original]
  have hn : 0 < ‖gramSchmidt ℝ (euclideanColumns A) i‖ :=
    norm_pos_iff.mpr (gramSchmidt_ne_zero i (euclideanColumns_linearIndependent A hA))
  positivity

theorem normalizedQRQ_positiveQR {n : ℕ} (A : Mat n) (hA : A.det ≠ 0) :
    PositiveQR A (normalizedQRQ A) ((normalizedQRQ A).transpose * A) := by
  have hQ := normalizedQRQ_orthogonal A hA
  refine ⟨hQ, ?_, normalizedQRQ_upper A, normalizedQRQ_diagonal_pos A hA⟩
  have hQQ : normalizedQRQ A * (normalizedQRQ A).transpose = 1 :=
    mul_eq_one_comm.mp hQ
  rw [← Matrix.mul_assoc, hQQ, Matrix.one_mul]

theorem prescribedLower_det (n : ℕ) : (prescribedLower n).det = 1 := by
  have hL : (prescribedLower n).IsLowerTriangular := by
    intro i j hij
    change i < j at hij
    simp [prescribedLower, ne_of_lt hij, not_lt_of_ge hij.le]
  rw [Matrix.det_of_isLowerTriangular _ hL]
  simp [prescribedLower]

theorem positiveQR_inner {n : ℕ} {A Q R : Mat n} (hQR : PositiveQR A Q R)
    (i j : Fin n) : inner ℝ (euclideanColumns Q i) (euclideanColumns A j) = R i j := by
  rw [euclideanColumns_inner, hQR.2.1, ← Matrix.mul_assoc, hQR.1, Matrix.one_mul]

theorem positiveQR_column {n : ℕ} {A Q R : Mat n} (hQR : PositiveQR A Q R)
    (j : Fin n) : euclideanColumns A j =
      R j j • euclideanColumns Q j +
        ∑ i ∈ Finset.Iio j, R i j • euclideanColumns Q i := by
  have hsum : euclideanColumns A j =
      ∑ i : Fin n, R i j • euclideanColumns Q i := by
    apply (WithLp.linearEquiv 2 ℝ (Fin n → ℝ)).injective
    ext k
    simpa [euclideanColumns, map_sum, Matrix.mul_apply, mul_comm] using
      congrArg (fun M : Mat n => M k j) hQR.2.1
  rw [hsum]
  calc
    (∑ i : Fin n, R i j • euclideanColumns Q i) =
        ∑ i ∈ insert j (Finset.Iio j), R i j • euclideanColumns Q i := by
      symm
      apply Finset.sum_subset (Finset.subset_univ _)
      intro i _ hi
      have hji : j < i := by simpa using hi
      rw [hQR.2.2.1 i j hji, zero_smul]
    _ = _ := by rw [Finset.sum_insert (by simp)]

theorem gramSchmidt_eq_of_positiveQR {n : ℕ} {A Q R : Mat n}
    (hQR : PositiveQR A Q R) (j : Fin n) :
    gramSchmidt ℝ (euclideanColumns A) j = R j j • euclideanColumns Q j := by
  have hcols := (orthogonal_iff_orthonormal_columns Q).mp hQR.1
  refine (wellFounded_lt : WellFounded ((· < ·) : Fin n → Fin n → Prop)).induction
    (C := fun j : Fin n => gramSchmidt ℝ (euclideanColumns A) j =
      R j j • euclideanColumns Q j) j ?_
  intro j ih
  rw [gramSchmidt_def]
  have hprojections : (∑ i ∈ Finset.Iio j,
      (ℝ ∙ gramSchmidt ℝ (euclideanColumns A) i).starProjection
        (euclideanColumns A j)) =
      ∑ i ∈ Finset.Iio j, R i j • euclideanColumns Q i := by
    apply Finset.sum_congr rfl
    intro i hi
    rw [Submodule.starProjection_singleton, ih i (Finset.mem_Iio.mp hi)]
    simp only [real_inner_smul_left, positiveQR_inner hQR, norm_smul,
      Real.norm_eq_abs, abs_of_pos (hQR.2.2.2 i), hcols.norm_eq_one i, mul_one,
      smul_smul, RCLike.ofReal_real_eq_id, id_eq]
    congr 1
    field_simp [ne_of_gt (hQR.2.2.2 i)]
  rw [hprojections, positiveQR_column hQR j, add_sub_cancel_right]

theorem normalizedQRQ_eq_of_positiveQR {n : ℕ} {A Q R : Mat n}
    (hQR : PositiveQR A Q R) : normalizedQRQ A = Q := by
  have hcols := (orthogonal_iff_orthonormal_columns Q).mp hQR.1
  ext i j
  have hj : gramSchmidtNormed ℝ (euclideanColumns A) j = euclideanColumns Q j := by
    rw [gramSchmidtNormed, gramSchmidt_eq_of_positiveQR hQR j]
    simp [norm_smul, Real.norm_eq_abs, abs_of_pos (hQR.2.2.2 j), hcols.norm_eq_one j,
      smul_smul, ne_of_gt (hQR.2.2.2 j)]
  exact congrArg (fun v : EuclideanSpace ℝ (Fin n) => v i) hj

theorem candidate_positiveQR (n : ℕ) (_hn : 2 ≤ n) :
    PositiveQR (prescribedLower n) (candidateQ n) (candidateR n) ∧
      ∀ Q R, PositiveQR (prescribedLower n) Q R →
        Q = candidateQ n ∧ R = candidateR n := by
  have hdet : (prescribedLower n).det ≠ 0 := by rw [prescribedLower_det]; norm_num
  refine ⟨normalizedQRQ_positiveQR (prescribedLower n) hdet, ?_⟩
  intro Q R hQR
  have hQ : Q = candidateQ n := (normalizedQRQ_eq_of_positiveQR hQR).symm
  refine ⟨hQ, ?_⟩
  unfold candidateR
  rw [← hQ, hQR.2.1, ← Matrix.mul_assoc, hQR.1, Matrix.one_mul]

#print axioms euclideanColumns_inner
#assert_trust kernel euclideanColumns_inner
#print axioms orthogonal_iff_orthonormal_columns
#assert_trust kernel orthogonal_iff_orthonormal_columns
#print axioms euclideanColumns_linearIndependent
#assert_trust kernel euclideanColumns_linearIndependent
#print axioms euclideanColumns_normalizedQRQ
#assert_trust kernel euclideanColumns_normalizedQRQ
#print axioms normalizedQRQ_orthogonal
#assert_trust kernel normalizedQRQ_orthogonal
#print axioms gramSchmidt_inner_original
#assert_trust kernel gramSchmidt_inner_original
#print axioms normalizedQRQ_upper
#assert_trust kernel normalizedQRQ_upper
#print axioms normalizedQRQ_diagonal_pos
#assert_trust kernel normalizedQRQ_diagonal_pos
#print axioms normalizedQRQ_positiveQR
#assert_trust kernel normalizedQRQ_positiveQR
#print axioms prescribedLower_det
#assert_trust kernel prescribedLower_det
#print axioms positiveQR_inner
#assert_trust kernel positiveQR_inner
#print axioms positiveQR_column
#assert_trust kernel positiveQR_column
#print axioms gramSchmidt_eq_of_positiveQR
#assert_trust kernel gramSchmidt_eq_of_positiveQR
#print axioms normalizedQRQ_eq_of_positiveQR
#assert_trust kernel normalizedQRQ_eq_of_positiveQR
#print axioms candidate_positiveQR
#assert_trust kernel candidate_positiveQR

end NLA.IE05._proved
