/- Generic finite-node minimax lemma for IE-16.

  The statement is independent of the particular nine-point coordinates.  It
  packages the exact complex Lagrange interpolation argument needed both for
  the full witness and for every five-point subset.

  This file is a source-only draft made while the local compiler is paused;
  it is not Lean proof evidence until a pinned direct typecheck succeeds. -/
import NLA.IE16.Definitions
import Mathlib.Tactic
import LeanCert.Tactic.Verification
import Mathlib.Algebra.Polynomial.Eval.Coeff
import Mathlib.Algebra.Polynomial.Degree.Defs
import Mathlib.LinearAlgebra.Lagrange

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical
noncomputable section

namespace NLA.IE16

def lagrangeBasisAtZero (S : Finset ℂ) (z : ℂ) : ℂ :=
  (Lagrange.basis S id z).eval 0

def lagrangeSum (S : Finset ℂ) : ℝ :=
  ∑ z ∈ S, ‖lagrangeBasisAtZero S z‖

lemma lagrangeBasisAtZero_ne_zero {S : Finset ℂ} {z : ℂ}
    (hz : z ∈ S) (hnz : ∀ w ∈ S, w ≠ 0) :
    lagrangeBasisAtZero S z ≠ 0 := by
  unfold lagrangeBasisAtZero
  rw [Lagrange.basis, Polynomial.eval_prod]
  apply Finset.prod_ne_zero_iff.mpr
  intro w hw
  rcases Finset.mem_erase.mp hw with ⟨hzw, hwS⟩
  simp only [Lagrange.basisDivisor, Polynomial.eval_mul,
    Polynomial.eval_C, Polynomial.eval_sub, Polynomial.eval_X, id_eq, zero_sub]
  apply mul_ne_zero
  · exact inv_ne_zero (sub_ne_zero.mpr hzw.symm)
  · exact neg_ne_zero.mpr (hnz w hwS)

lemma lagrangeSum_pos {S : Finset ℂ} (hS : S.Nonempty)
    (hnz : ∀ z ∈ S, z ≠ 0) : 0 < lagrangeSum S := by
  unfold lagrangeSum
  apply Finset.sum_pos'
  · intro z hz
    exact norm_nonneg _
  · rcases hS with ⟨z, hz⟩
    exact ⟨z, hz, norm_pos_iff.mpr (lagrangeBasisAtZero_ne_zero hz hnz)⟩

def lagrangeValue (S : Finset ℂ) (z : ℂ) : ℂ :=
  ((‖lagrangeBasisAtZero S z‖ / lagrangeSum S : ℝ) : ℂ) *
    (lagrangeBasisAtZero S z)⁻¹

def lagrangeAttainer (S : Finset ℂ) : Poly :=
  Lagrange.interpolate S id (lagrangeValue S)

lemma lagrangeValue_mul_basis {S : Finset ℂ} {z : ℂ}
    (hz : z ∈ S) (hnz : ∀ w ∈ S, w ≠ 0) :
    lagrangeBasisAtZero S z * lagrangeValue S z =
      ((‖lagrangeBasisAtZero S z‖ / lagrangeSum S : ℝ) : ℂ) := by
  unfold lagrangeValue
  rw [mul_left_comm, mul_inv_cancel₀ (lagrangeBasisAtZero_ne_zero hz hnz), mul_one]

lemma lagrangeValue_norm {S : Finset ℂ} {z : ℂ}
    (hz : z ∈ S) (hnz : ∀ w ∈ S, w ≠ 0) :
    ‖lagrangeValue S z‖ = (lagrangeSum S)⁻¹ := by
  have hA : 0 < lagrangeSum S := lagrangeSum_pos ⟨z, hz⟩ hnz
  have hB : 0 < ‖lagrangeBasisAtZero S z‖ :=
    norm_pos_iff.mpr (lagrangeBasisAtZero_ne_zero hz hnz)
  unfold lagrangeValue
  rw [norm_mul, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (div_pos hB hA), norm_inv]
  field_simp [ne_of_gt hA, ne_of_gt hB]

lemma lagrangeAttainer_eval_node {S : Finset ℂ} {z : ℂ}
    (hz : z ∈ S) :
    (lagrangeAttainer S).eval z = lagrangeValue S z := by
  unfold lagrangeAttainer
  simpa only [id_eq] using
    (Lagrange.eval_interpolate_at_node (r := lagrangeValue S)
      (v := id) (s := S) Function.injective_id.injOn hz)

lemma lagrangeAttainer_eval_zero {S : Finset ℂ} (hS : S.Nonempty)
    (hnz : ∀ z ∈ S, z ≠ 0) :
    (lagrangeAttainer S).eval 0 = 1 := by
  have hA : 0 < lagrangeSum S := lagrangeSum_pos hS hnz
  have hterm : ∀ z ∈ S,
      lagrangeValue S z * lagrangeBasisAtZero S z =
        ((‖lagrangeBasisAtZero S z‖ / lagrangeSum S : ℝ) : ℂ) := by
    intro z hz
    rw [mul_comm, lagrangeValue_mul_basis hz hnz]
  unfold lagrangeAttainer
  simp only [Lagrange.interpolate_apply, Polynomial.eval_finsetSum,
    Polynomial.eval_mul, Polynomial.eval_C]
  change (∑ z ∈ S, lagrangeValue S z * lagrangeBasisAtZero S z) = 1
  rw [Finset.sum_congr rfl hterm]
  have hreal : (∑ z ∈ S, ‖lagrangeBasisAtZero S z‖ /
      lagrangeSum S) = 1 := by
    rw [← Finset.sum_div]
    change lagrangeSum S / lagrangeSum S = 1
    exact div_self (ne_of_gt hA)
  exact_mod_cast hreal

lemma lagrangeAttainer_feasible {S : Finset ℂ} (hcard : S.card = 5)
    (hS : S.Nonempty) (hnz : ∀ z ∈ S, z ≠ 0) :
    feasible S 4 (lagrangeAttainer S) := by
  have hzero := lagrangeAttainer_eval_zero hS hnz
  have hdeg : (lagrangeAttainer S).degree < (S.card : WithBot ℕ) := by
    exact Lagrange.degree_interpolate_lt (lagrangeValue S) Function.injective_id.injOn
  have hne : lagrangeAttainer S ≠ 0 := by
    intro h
    rw [h, Polynomial.eval_zero] at hzero
    norm_num at hzero
  have hnat : (lagrangeAttainer S).natDegree < S.card :=
    (Polynomial.natDegree_lt_iff_degree_lt hne).mpr hdeg
  constructor
  · rw [hcard] at hnat
    omega
  · exact hzero

lemma maxModulus_nonempty_eq_sup {S : Finset ℂ} (hS : S.Nonempty) (p : Poly) :
    maxModulus S p = S.sup' hS (fun z => ‖p.eval z‖) := by
  simp [maxModulus, hS]

lemma lagrangeAttainer_objective {S : Finset ℂ} (hS : S.Nonempty)
    (hnz : ∀ z ∈ S, z ≠ 0) :
    maxModulus S (lagrangeAttainer S) = (lagrangeSum S)⁻¹ := by
  rw [maxModulus_nonempty_eq_sup hS]
  apply Finset.sup'_eq_of_forall
  intro z hz
  rw [lagrangeAttainer_eval_node hz, lagrangeValue_norm hz hnz]

lemma lagrange_lower_bound {S : Finset ℂ} (hcard : S.card = 5)
    (hS : S.Nonempty) (hnz : ∀ z ∈ S, z ≠ 0) {p : Poly}
    (hp : feasible S 4 p) :
    (lagrangeSum S)⁻¹ ≤ maxModulus S p := by
  have hA : 0 < lagrangeSum S := lagrangeSum_pos hS hnz
  have hdeg_le : p.degree ≤ (4 : WithBot ℕ) :=
    (Polynomial.natDegree_le_iff_degree_le).mp hp.1
  have hdeg : p.degree < (S.card : WithBot ℕ) := by
    rw [hcard]
    exact lt_of_le_of_lt hdeg_le (by norm_num)
  have heq := Lagrange.eq_interpolate (s := S) (v := id)
    (f := p) Function.injective_id.injOn hdeg
  have heq0 := congrArg (fun q : Poly => q.eval 0) heq
  have hsum : p.eval 0 =
      ∑ z ∈ S, p.eval z * lagrangeBasisAtZero S z := by
    simpa [lagrangeBasisAtZero, Lagrange.interpolate_apply,
      Polynomial.eval_finsetSum, Polynomial.eval_mul, Polynomial.eval_C] using heq0
  have hmax : ∀ z ∈ S, ‖p.eval z‖ ≤ maxModulus S p := by
    intro z hz
    rw [maxModulus_nonempty_eq_sup hS]
    exact Finset.le_sup' (fun w : ℂ => ‖p.eval w‖) hz
  have hprod : (1 : ℝ) ≤ maxModulus S p * lagrangeSum S := by
    calc
      1 = ‖p.eval 0‖ := by rw [hp.2]; norm_num
      _ = ‖∑ z ∈ S, p.eval z * lagrangeBasisAtZero S z‖ := by rw [hsum]
      _ ≤ ∑ z ∈ S, ‖p.eval z * lagrangeBasisAtZero S z‖ :=
        norm_sum_le _ _
      _ = ∑ z ∈ S, ‖p.eval z‖ * ‖lagrangeBasisAtZero S z‖ := by
        simp_rw [norm_mul]
      _ ≤ ∑ z ∈ S, maxModulus S p * ‖lagrangeBasisAtZero S z‖ := by
        exact Finset.sum_le_sum fun z hz =>
          mul_le_mul_of_nonneg_right (hmax z hz) (norm_nonneg _)
      _ = maxModulus S p * lagrangeSum S := by
        simp only [lagrangeSum, Finset.mul_sum]
  apply (mul_le_mul_iff_left₀ hA).mp
  calc
    (lagrangeSum S)⁻¹ * lagrangeSum S = 1 :=
      inv_mul_cancel₀ (ne_of_gt hA)
    _ ≤ maxModulus S p * lagrangeSum S := hprod

theorem lagrange_isLeast {S : Finset ℂ} (hcard : S.card = 5)
    (hS : S.Nonempty) (hnz : ∀ z ∈ S, z ≠ 0) :
    IsLeast (feasibleValues S 4) (lagrangeSum S)⁻¹ := by
  refine ⟨?_, ?_⟩
  · refine ⟨lagrangeAttainer S, lagrangeAttainer_feasible hcard hS hnz,
      lagrangeAttainer_objective hS hnz⟩
  · rintro r ⟨p, hp, rfl⟩
    exact lagrange_lower_bound hcard hS hnz hp

end NLA.IE16
