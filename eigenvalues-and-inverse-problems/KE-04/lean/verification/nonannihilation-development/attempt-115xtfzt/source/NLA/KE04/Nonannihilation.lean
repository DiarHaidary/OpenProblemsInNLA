import NLA.KE04.Krylov
import NLA.KE04.Frames
import Mathlib.Algebra.BigOperators.Fin

/-!
# KE-04: full Krylov rank excludes quadratic annihilation

Appending a zero block and shifting the coefficient blocks describe the same
Krylov vector and its image under A. Independence forces these coefficient
representations to agree only trivially when A x = a x: backward induction
starts from the appended zero block. Applying that fact to the two affine
factors proves the monic quadratic assertion, even at coincident endpoints.

Original mathematical argument: Matthew J. Colbrook, University of Cambridge.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA,
with AI assistance by the mf16_final_referee agent.
-/

set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.KE04._proved

/-- Append the zero coefficient at the new greatest degree. -/
def blockExtend {ell p : ℕ} (c : Fin ell × Fin p → ℝ) :
    Fin (ell + 1) × Fin p → ℝ :=
  fun rc => Fin.lastCases 0 (fun r => c (r, rc.2)) rc.1

/-- Multiplication by the formal degree variable shifts every coefficient up. -/
def blockShift {ell p : ℕ} (c : Fin ell × Fin p → ℝ) :
    Fin (ell + 1) × Fin p → ℝ :=
  fun rc => Fin.cases 0 (fun r => c (r, rc.2)) rc.1

/-- Zero extension leaves the actual finite Krylov combination unchanged. -/
theorem krylovCombination_extend {n p ell : ℕ} (A : Mat n) (V : Rect n p)
    (c : Fin ell × Fin p → ℝ) :
    krylovCombination A V (ell + 1) (blockExtend c) = krylovCombination A V ell c := by
  simp only [krylovCombination, Fintype.linearCombination_apply, Fintype.sum_prod_type]
  rw [Fin.sum_univ_castSucc]
  simp [blockExtend, krylovColumns]

/-- The shifted coefficients represent multiplication by the actual matrix A. -/
theorem krylovCombination_shift {n p ell : ℕ} (A : Mat n) (V : Rect n p)
    (c : Fin ell × Fin p → ℝ) :
    krylovCombination A V (ell + 1) (blockShift c) = act A (krylovCombination A V ell c) := by
  simp only [krylovCombination, Fintype.linearCombination_apply, Fintype.sum_prod_type]
  rw [Fin.sum_univ_succ]
  simp [blockShift, krylovColumns, map_sum, map_smul, act_column_mul,
    pow_succ', Matrix.mul_assoc]

/-- A shift cannot equal a scalar times zero extension unless every block is zero. -/
theorem blockShift_eq_smul_extend {ell p : ℕ} (c : Fin ell × Fin p → ℝ) (a : ℝ)
    (h : blockShift c = a • blockExtend c) : c = 0 := by
  cases ell with
  | zero =>
      funext rc
      exact rc.1.elim0
  | succ ell =>
      funext rc
      obtain ⟨r, j⟩ := rc
      induction r using Fin.reverseInduction with
      | last =>
          have ht := congrFun h ((Fin.last ell).succ, j)
          simp only [blockShift, Fin.cases_succ, Pi.smul_apply, smul_eq_mul] at ht
          have he : (Fin.last ell).succ = Fin.last (ell + 1) := rfl
          rw [he] at ht
          simpa [blockExtend] using ht
      | cast r ih =>
          have ht := congrFun h (r.castSucc.succ, j)
          simp only [blockShift, Fin.cases_succ, Pi.smul_apply, smul_eq_mul] at ht
          have he : r.castSucc.succ = r.succ.castSucc := rfl
          rw [he] at ht
          -- Keep the cast outside the successor so lastCases reduces at its
          -- explicit castSucc constructor; unrestricted simp reverses that form.
          simpa only [blockExtend, Fin.lastCases_castSucc, ih, mul_zero] using ht

/-- Full rank one degree further excludes any eigenvector in the earlier Krylov space. -/
theorem fullRank_krylov_eigenvector_zero {n p : ℕ} (A : Mat n) (V : Rect n p)
    (ell : ℕ) (hfull : FullBlockDimension A V (ell + 1))
    (x : Vec n) (hx : x ∈ krylov A V ell) (a : ℝ) (hAx : act A x = a • x) :
    x = 0 := by
  rw [krylov_eq_range] at hx
  obtain ⟨c, hc⟩ := hx
  have hi := (fullBlockDimension_prefix A V (ell + 1) hfull (ell + 1) le_rfl).2
  have he : blockShift c = a • blockExtend c := by
    apply hi
    rw [krylovCombination_shift, map_smul, krylovCombination_extend, hc, hAx]
  have hz := blockShift_eq_smul_extend c a he
  rw [hz, map_zero] at hc
  exact hc.symm

/-- The affine matrix factor has its ordinary Euclidean action. -/
theorem act_sub_smul_one {n : ℕ} (A : Mat n) (a : ℝ) (x : Vec n) :
    act (A - a • (1 : Mat n)) x = act A x - a • x := by
  ext i
  simp [act_apply, Matrix.sub_apply, Matrix.one_apply, sub_mul,
    Finset.sum_sub_distrib]

/-- The exact approved monic quadratic nonannihilation contract. -/
theorem fullRank_quadratic_nonannihilation {n p : ℕ} (A : Mat n) (V : Rect n p)
    (k : ℕ) (hk : 2 ≤ k) (hfull : FullBlockDimension A V (k + 1))
    (x : Vec n) (hx : x ∈ krylov A V (k - 1)) (hne : x ≠ 0) (a b : ℝ) :
    act (quadraticMatrix A a b) x ≠ 0 := by
  have hk1 : k - 1 + 1 = k := by omega
  have hfullk := (fullBlockDimension_prefix A V (k + 1) hfull k (by omega)).1
  let y := act A x - b • x
  have hy : y ∈ krylov A V k := by
    apply (krylov A V k).sub_mem
    · simpa only [hk1] using act_mem_krylov_succ A V (k - 1) x hx
    · exact (krylov A V k).smul_mem b (krylov_mono A V (by omega) hx)
  intro hq
  have hay : act A y = a • y := by
    apply sub_eq_zero.mp
    simpa only [quadraticMatrix, act_mul, act_sub_smul_one, y] using hq
  have hy0 := fullRank_krylov_eigenvector_zero A V k hfull y hy a hay
  have hb : act A x = b • x := sub_eq_zero.mp hy0
  have hx0 := fullRank_krylov_eigenvector_zero A V (k - 1)
    (by simpa only [hk1] using hfullk) x hx b hb
  exact hne hx0

#assert_trust kernel blockExtend
#print axioms blockExtend
#assert_trust kernel blockShift
#print axioms blockShift
#assert_trust kernel krylovCombination_extend
#print axioms krylovCombination_extend
#assert_trust kernel krylovCombination_shift
#print axioms krylovCombination_shift
#assert_trust kernel blockShift_eq_smul_extend
#print axioms blockShift_eq_smul_extend
#assert_trust kernel fullRank_krylov_eigenvector_zero
#print axioms fullRank_krylov_eigenvector_zero
#assert_trust kernel act_sub_smul_one
#print axioms act_sub_smul_one
#assert_trust kernel fullRank_quadratic_nonannihilation
#print axioms fullRank_quadratic_nonannihilation

end NLA.KE04._proved
