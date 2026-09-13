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

end NLA.IE05._proved
