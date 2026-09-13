import NLA.KE04.Definitions
import LeanCert.Tactic.Verification
import Mathlib.Tactic.Ring

/-!
# KE-04: genuine Euclidean frames, projections and compressions

Original mathematical proof: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
The formal_review_standards AI agent implemented this helper after the accepted
statement gate. It uses Mathlib's actual subspace orthonormal bases and matrix
action. No compatibility between different Krylov bases is imposed.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.KE04._proved

theorem act_apply {n m : ℕ} (M : Rect n m) (x : Vec m) (i : Fin n) :
    act M x i = ∑ j, M i j * x j := rfl

theorem act_mul {n m r : ℕ} (M : Rect n m) (N : Rect m r) (x : Vec r) :
    act (M * N) x = act M (act N x) := by
  simp only [act, Matrix.toEuclideanLin, Matrix.toLpLin_mul_same, LinearMap.comp_apply]

theorem act_one {n : ℕ} (x : Vec n) : act (1 : Mat n) x = x := by
  simp only [act, Matrix.toEuclideanLin, Matrix.toLpLin_one, LinearMap.id_apply]

theorem inner_eq_sum {n : ℕ} (x y : Vec n) :
    inner ℝ x y = ∑ i, x i * y i := by
  simp [PiLp.inner_apply, mul_comm]

theorem inner_act_transpose {n m : ℕ} (M : Rect n m) (x : Vec n) (y : Vec m) :
    inner ℝ x (act M y) = inner ℝ (act M.transpose x) y := by
  simp_rw [inner_eq_sum, act_apply, Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro i _
  simp only [Matrix.transpose_apply]
  ring

theorem inner_act_left {n m : ℕ} (M : Rect n m) (x : Vec m) (y : Vec n) :
    inner ℝ (act M x) y = inner ℝ x (act M.transpose y) := by
  rw [real_inner_comm, inner_act_transpose, real_inner_comm]

theorem inner_columns {n m r : ℕ} (M : Rect n m) (N : Rect n r)
    (i : Fin m) (j : Fin r) :
    inner ℝ (column M i) (column N j) = (M.transpose * N) i j := by
  simp [column, PiLp.inner_apply, Matrix.mul_apply, Matrix.transpose_apply, mul_comm]

theorem frame_iff_orthonormal {n m : ℕ} (Q : Rect n m) :
    Q.transpose * Q = 1 ↔ Orthonormal ℝ (column Q) := by
  rw [orthonormal_iff_ite]
  simp only [inner_columns]
  constructor
  · intro h i j
    simpa [Matrix.one_apply] using congrArg (fun M : Mat m => M i j) h
  · intro h
    ext i j
    exact h i j

theorem real_matrix_semantics {n m : ℕ} (A : Mat n) (M : Rect n m) :
    (A.IsHermitian ↔ A.transpose = A) ∧
      (∀ (x : Vec m) i, act M x i = ∑ j, M i j * x j) ∧
      (M.transpose * M = 1 ↔ Orthonormal ℝ (column M)) := by
  refine ⟨?_, act_apply M, frame_iff_orthonormal M⟩
  simp only [Matrix.IsHermitian, Matrix.conjTranspose_eq_transpose_of_trivial]

theorem act_eq_column_sum {n m : ℕ} (Q : Rect n m) (x : Vec m) :
    act Q x = ∑ j, x j • column Q j := by
  ext i
  simp [act_apply, column, Finset.sum_apply, mul_comm]

theorem columnSpace_eq_range_act {n m : ℕ} (Q : Rect n m) :
    columnSpace Q = LinearMap.range (act Q) := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro _ ⟨j, rfl⟩
    refine ⟨EuclideanSpace.single j 1, ?_⟩
    ext i
    simp [act_apply, column, EuclideanSpace.single_apply]
  · rintro _ ⟨x, rfl⟩
    rw [act_eq_column_sum]
    exact Submodule.sum_mem _ fun j _ =>
      Submodule.smul_mem _ _ (Submodule.subset_span ⟨j, rfl⟩)

theorem act_transpose_act {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) (x : Vec m) :
    act Q.transpose (act Q x) = x := by
  rw [← act_mul, hQ, act_one]

theorem frameProjection_act {n m : ℕ} (Q : Rect n m) (x : Vec n) :
    act (frameProjection Q) x = act Q (act Q.transpose x) := by
  simp only [frameProjection, Matrix.conjTranspose_eq_transpose_of_trivial, act_mul]

theorem frameProjection_fixed_iff {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) (x : Vec n) :
    x ∈ columnSpace Q ↔ act (frameProjection Q) x = x := by
  rw [columnSpace_eq_range_act]
  constructor
  · rintro ⟨z, rfl⟩
    rw [frameProjection_act, act_transpose_act Q hQ]
  · intro hx
    exact ⟨act Q.transpose x, (frameProjection_act Q x).symm.trans hx⟩

theorem frameProjection_semantics {n m : ℕ} (Q : Rect n m)
    (hQ : Q.transpose * Q = 1) :
    (frameProjection Q).IsHermitian ∧
      frameProjection Q * frameProjection Q = frameProjection Q ∧
      (∀ x, x ∈ columnSpace Q ↔ act (frameProjection Q) x = x) ∧
      ∀ x y, y ∈ columnSpace Q →
        inner ℝ y (x - act (frameProjection Q) x) = 0 := by
  refine ⟨?_, ?_, frameProjection_fixed_iff Q hQ, ?_⟩
  · simp [frameProjection, Matrix.IsHermitian]
  · simp only [frameProjection, Matrix.conjTranspose_eq_transpose_of_trivial]
    calc
      Q * Q.transpose * (Q * Q.transpose) = Q * (Q.transpose * Q) * Q.transpose := by
        simp only [Matrix.mul_assoc]
      _ = Q * Q.transpose := by rw [hQ, Matrix.mul_one]
  · intro x y hy
    rw [columnSpace_eq_range_act] at hy
    obtain ⟨z, rfl⟩ := hy
    rw [inner_act_left, map_sub, frameProjection_act, act_transpose_act Q hQ,
      sub_self, inner_zero_right]

theorem submodule_frame_exists {n m : ℕ} (S : Submodule ℝ (Vec n))
    (hS : Module.finrank ℝ S = m) :
    ∃ Q : Rect n m, Q.transpose * Q = 1 ∧ columnSpace Q = S := by
  let b : OrthonormalBasis (Fin m) ℝ S :=
    (stdOrthonormalBasis ℝ S).reindex (finCongr hS)
  let Q : Rect n m := fun i j => (b j : Vec n) i
  have hc : column Q = fun j => (b j : Vec n) := by
    funext j
    ext i
    rfl
  refine ⟨Q, (frame_iff_orthonormal Q).mpr ?_, ?_⟩
  · rw [hc]
    exact b.orthonormal.comp_linearIsometry S.subtypeₗᵢ
  · change Submodule.span ℝ (Set.range (column Q)) = S
    rw [hc]
    have hmap := congrArg (Submodule.map S.subtype) b.toBasis.span_eq
    simpa only [Submodule.map_span, Set.image_range, Submodule.map_subtype_top,
      OrthonormalBasis.coe_toBasis, Function.comp_def, Submodule.subtype_apply] using hmap

theorem krylovBasis_exists {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (hfull : FullBlockDimension A V ell) :
    ∃ Q : Rect n (ell * p), IsKrylovBasis A V ell Q := by
  exact submodule_frame_exists (krylov A V ell) hfull

theorem compression_semantics {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (hQ : Q.transpose * Q = 1) :
    compression A Q = Q.transpose * A * Q ∧ (compression A Q).IsHermitian ∧
      ∀ x, x ∈ columnSpace Q →
        act Q (act (compression A Q) (act Q.transpose x)) =
          act (frameProjection Q) (act A x) := by
  refine ⟨?_, Matrix.isHermitian_conjTranspose_mul_mul Q hA, ?_⟩
  · simp only [compression, Matrix.conjTranspose_eq_transpose_of_trivial]
  · intro x hx
    have hrep : act Q (act Q.transpose x) = x :=
      (frameProjection_act Q x).symm.trans ((frameProjection_fixed_iff Q hQ x).mp hx)
    simp only [compression, Matrix.conjTranspose_eq_transpose_of_trivial, act_mul,
      frameProjection_act, hrep]

theorem compressedQuadratic_semantics {n m : ℕ} (A : Mat n) (Q : Rect n m)
    (a b : ℝ) :
    (∀ x, form (compressedQuadratic A Q a b) x =
      form (quadraticMatrix (compression A Q) a b) (act Q.transpose x)) ∧
      ((quadraticMatrix (compression A Q) a b).PosSemidef →
        (compressedQuadratic A Q a b).PosSemidef) := by
  constructor
  · intro x
    simp only [form, compressedQuadratic, act_mul,
      Matrix.conjTranspose_eq_transpose_of_trivial, inner_act_transpose]
  · intro h
    exact h.mul_mul_conjTranspose_same Q

#assert_trust kernel real_matrix_semantics
#print axioms real_matrix_semantics
#assert_trust kernel columnSpace_eq_range_act
#print axioms columnSpace_eq_range_act
#assert_trust kernel inner_act_transpose
#print axioms inner_act_transpose
#assert_trust kernel frameProjection_semantics
#print axioms frameProjection_semantics
#assert_trust kernel submodule_frame_exists
#print axioms submodule_frame_exists
#assert_trust kernel krylovBasis_exists
#print axioms krylovBasis_exists
#assert_trust kernel compression_semantics
#print axioms compression_semantics
#assert_trust kernel compressedQuadratic_semantics
#print axioms compressedQuadratic_semantics

end NLA.KE04._proved
