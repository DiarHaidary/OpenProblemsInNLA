/- Source-only draft of the positive-weight full-set lower bound.

  `Numeric.lean` supplies the concrete nine-point moments.  This file keeps
  the analytic bridge separate while the remote compiler checks the frozen
  finite arithmetic drafts; it is not proof evidence until that check passes.
-/
import NLA.IE16.Minimax
import Mathlib.Analysis.Complex.Norm

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical
noncomputable section

namespace NLA.IE16

lemma complex_sq_norm_add (u v : ℂ) :
    ‖u + v‖ ^ 2 = ‖u‖ ^ 2 + ‖v‖ ^ 2 +
      2 * (conj u * v).re := by
  rw [Complex.sq_norm, Complex.sq_norm, Complex.sq_norm]
  simp only [Complex.normSq_apply, Complex.add_re, Complex.add_im,
    Complex.mul_re, Complex.conj_re, Complex.conj_im]
  ring

lemma weighted_norm_sq_identity {S : Finset ℂ} {pstar p : Poly}
    {m : ℝ} {w : ℂ → ℝ}
    (hS : S.Nonempty)
    (hweights : ∀ z ∈ S, 0 ≤ w z)
    (hsum : ∑ z in S, w z = 1)
    (hstar : ∀ z ∈ S, ‖pstar.eval z‖ = m)
    (horth : ∑ z in S,
        w z * (conj (pstar.eval z) * (p.eval z - pstar.eval z)).re = 0) :
    ∑ z in S, w z * ‖p.eval z‖ ^ 2 =
      m ^ 2 + ∑ z in S, w z * ‖p.eval z - pstar.eval z‖ ^ 2 := by
  have hterm : ∀ z ∈ S,
      ‖p.eval z‖ ^ 2 =
        ‖pstar.eval z‖ ^ 2 + ‖p.eval z - pstar.eval z‖ ^ 2 +
          2 * (conj (pstar.eval z) *
            (p.eval z - pstar.eval z)).re := by
    intro z hz
    have he : p.eval z = pstar.eval z + (p.eval z - pstar.eval z) := by ring
    rw [he, complex_sq_norm_add]
  calc
    ∑ z in S, w z * ‖p.eval z‖ ^ 2 =
        ∑ z in S, w z *
          (‖pstar.eval z‖ ^ 2 + ‖p.eval z - pstar.eval z‖ ^ 2 +
            2 * (conj (pstar.eval z) *
              (p.eval z - pstar.eval z)).re) := by
      exact Finset.sum_congr rfl (fun z hz => congrArg (fun r : ℝ => w z * r)
        (hterm z hz))
    _ = (∑ z in S, w z * ‖pstar.eval z‖ ^ 2) +
        (∑ z in S, w z * ‖p.eval z - pstar.eval z‖ ^ 2) +
        2 * (∑ z in S,
          w z * (conj (pstar.eval z) *
            (p.eval z - pstar.eval z)).re) := by
      simp_rw [mul_add]
      rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      rw [← Finset.sum_mul]
      ring
    _ = m ^ 2 + ∑ z in S, w z * ‖p.eval z - pstar.eval z‖ ^ 2 := by
      rw [horth]
      have hsquare : ∑ z in S, w z * ‖pstar.eval z‖ ^ 2 = m ^ 2 := by
        calc
          ∑ z in S, w z * ‖pstar.eval z‖ ^ 2 =
              ∑ z in S, w z * m ^ 2 := by
            exact Finset.sum_congr rfl (fun z hz =>
              congrArg (fun r : ℝ => w z * r)
                (congrArg (fun r : ℝ => r ^ 2) (hstar z hz)))
          _ = (∑ z in S, w z) * m ^ 2 := by rw [Finset.sum_mul]
          _ = m ^ 2 := by rw [hsum, one_mul]
      rw [hsquare]
      ring

theorem weighted_minimum_lower {S : Finset ℂ} {pstar : Poly} {m : ℝ}
    {w : ℂ → ℝ} (hS : S.Nonempty)
    (hweights : ∀ z ∈ S, 0 ≤ w z)
    (hsum : ∑ z in S, w z = 1)
    (hstar : ∀ z ∈ S, ‖pstar.eval z‖ = m)
    {p : Poly} (hp : feasible S 4 p)
    (horth : ∑ z in S,
        w z * (conj (pstar.eval z) * (p.eval z - pstar.eval z)).re = 0) :
    m ≤ maxModulus S p := by
  have hm : 0 ≤ m := by
    rcases hS with ⟨z, hz⟩
    rw [← hstar z hz]
    exact norm_nonneg _
  have hR : 0 ≤ maxModulus S p := by
    unfold maxModulus
    simp only [dif_pos hS]
    exact Finset.sup'_le hS (fun z hz => norm_nonneg _)
  have hmax : ∀ z ∈ S, ‖p.eval z‖ ≤ maxModulus S p := by
    intro z hz
    unfold maxModulus
    simp only [dif_pos hS]
    exact Finset.le_sup' _ hz
  have henergy_nonneg : 0 ≤
      ∑ z in S, w z * ‖p.eval z - pstar.eval z‖ ^ 2 := by
    apply Finset.sum_nonneg
    intro z hz
    exact mul_nonneg (hweights z hz) (sq_nonneg _)
  have henergy_lower : m ^ 2 ≤
      ∑ z in S, w z * ‖p.eval z‖ ^ 2 := by
    rw [weighted_norm_sq_identity hS hweights hsum hstar horth]
    linarith
  have henergy_upper :
      ∑ z in S, w z * ‖p.eval z‖ ^ 2 ≤ (maxModulus S p) ^ 2 := by
    calc
      ∑ z in S, w z * ‖p.eval z‖ ^ 2 ≤
          ∑ z in S, w z * (maxModulus S p) ^ 2 := by
        apply Finset.sum_le_sum
        intro z hz
        exact mul_le_mul_of_nonneg_left
          (by nlinarith [hmax z hz, norm_nonneg (p.eval z)])
          (hweights z hz)
      _ = (maxModulus S p) ^ 2 := by
        rw [← Finset.sum_mul, hsum, one_mul]
  nlinarith

end NLA.IE16
