/-
  Indexed bridge for the full nine-point lower bound.

  The indexed formulation avoids introducing an inverse weight function on
  the image explicitL: the nine nodes are indexed by Fin 3 × Fin 3, and
  explicitL is their injective image. The generic weighted identity is
  combined with the exact moments from Numeric.lean.
-/
import NLA.IE16.WeightedDraft
import NLA.IE16.Numeric
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Algebra.Polynomial.Eval.Degree
import Mathlib.Data.Complex.BigOperators
import Mathlib.Tactic

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Classical ComplexConjugate
noncomputable section

namespace NLA.IE16

lemma weighted_norm_sq_identity_indexed {ι : Type*} [Fintype ι]
    {f : ι → ℂ} {pstar p : Poly} {m : ℝ} {w : ι → ℝ}
    (hweights : ∀ i, 0 ≤ w i)
    (hsum : ∑ i, w i = 1)
    (hstar : ∀ i, ‖pstar.eval (f i)‖ = m)
    (horth : ∑ i,
        w i * (conj (pstar.eval (f i)) *
          (p.eval (f i) - pstar.eval (f i))).re = 0) :
    ∑ i, w i * ‖p.eval (f i)‖ ^ 2 =
      m ^ 2 + ∑ i, w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 := by
  classical
  have hterm : ∀ i,
      ‖p.eval (f i)‖ ^ 2 =
        ‖pstar.eval (f i)‖ ^ 2 +
          ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 +
          2 * (conj (pstar.eval (f i)) *
            (p.eval (f i) - pstar.eval (f i))).re := by
    intro i
    have he : p.eval (f i) = pstar.eval (f i) +
        (p.eval (f i) - pstar.eval (f i)) := by ring
    calc
      ‖p.eval (f i)‖ ^ 2 =
          ‖pstar.eval (f i) + (p.eval (f i) - pstar.eval (f i))‖ ^ 2 := by
            exact congrArg (fun z : ℂ => ‖z‖ ^ 2) he
      _ = ‖pstar.eval (f i)‖ ^ 2 +
          ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 +
          2 * (conj (pstar.eval (f i)) *
            (p.eval (f i) - pstar.eval (f i))).re := by
            exact complex_sq_norm_add _ _
  calc
    ∑ i, w i * ‖p.eval (f i)‖ ^ 2 =
        ∑ i, w i * (‖pstar.eval (f i)‖ ^ 2 +
          ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 +
          2 * (conj (pstar.eval (f i)) *
            (p.eval (f i) - pstar.eval (f i))).re) := by
      exact Finset.sum_congr rfl (fun i hi => congrArg (fun r : ℝ => w i * r)
        (hterm i))
    _ = (∑ i, w i * ‖pstar.eval (f i)‖ ^ 2) +
        (∑ i, w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2) +
        2 * (∑ i, w i * (conj (pstar.eval (f i)) *
          (p.eval (f i) - pstar.eval (f i))).re) := by
      calc
        (∑ i, w i *
            (‖pstar.eval (f i)‖ ^ 2 + ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 +
              2 * (conj (pstar.eval (f i)) *
                (p.eval (f i) - pstar.eval (f i))).re)) =
            ∑ i,
              (w i * ‖pstar.eval (f i)‖ ^ 2 +
                (w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 +
                  w i * (2 * (conj (pstar.eval (f i)) *
                    (p.eval (f i) - pstar.eval (f i))).re))) := by
          apply Finset.sum_congr rfl
          intro i hi
          ring
        _ = (∑ i, w i * ‖pstar.eval (f i)‖ ^ 2) +
              ((∑ i, w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2) +
                (∑ i, w i * (2 * (conj (pstar.eval (f i)) *
                  (p.eval (f i) - pstar.eval (f i))).re))) := by
          rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
        _ = (∑ i, w i * ‖pstar.eval (f i)‖ ^ 2) +
              (∑ i, w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2) +
              2 * (∑ i, w i * (conj (pstar.eval (f i)) *
                (p.eval (f i) - pstar.eval (f i))).re) := by
          have hcross :
              (∑ i, w i * (2 * (conj (pstar.eval (f i)) *
                (p.eval (f i) - pstar.eval (f i))).re)) =
                2 * (∑ i, w i * (conj (pstar.eval (f i)) *
                  (p.eval (f i) - pstar.eval (f i))).re) := by
            calc
              (∑ i, w i * (2 * (conj (pstar.eval (f i)) *
                  (p.eval (f i) - pstar.eval (f i))).re)) =
                  ∑ i, 2 * (w i * (conj (pstar.eval (f i)) *
                    (p.eval (f i) - pstar.eval (f i))).re) := by
                apply Finset.sum_congr rfl
                intro i hi
                ring
              _ = 2 * (∑ i, w i * (conj (pstar.eval (f i)) *
                    (p.eval (f i) - pstar.eval (f i))).re) := by
                rw [Finset.mul_sum]
          rw [hcross]
          ring
    _ = m ^ 2 + ∑ i, w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 := by
      rw [horth]
      have hsquare : ∑ i, w i * ‖pstar.eval (f i)‖ ^ 2 = m ^ 2 := by
        calc
          ∑ i, w i * ‖pstar.eval (f i)‖ ^ 2 =
              ∑ i, w i * m ^ 2 := by
            exact Finset.sum_congr rfl (fun i hi =>
              congrArg (fun r : ℝ => w i * r)
                (congrArg (fun r : ℝ => r ^ 2) (hstar i)))
          _ = (∑ i, w i) * m ^ 2 := by rw [Finset.sum_mul]
          _ = m ^ 2 := by rw [hsum, one_mul]
      rw [hsquare]
      ring

theorem weighted_minimum_lower_indexed {ι : Type*} [Fintype ι]
    {f : ι → ℂ} {pstar : Poly} {m : ℝ} {w : ι → ℝ}
    (hweights : ∀ i, 0 ≤ w i)
    (hsum : ∑ i, w i = 1)
    (hstar : ∀ i, ‖pstar.eval (f i)‖ = m)
    {p : Poly} (hp : feasible (Finset.univ.image f) 4 p)
    (horth : ∑ i,
        w i * (conj (pstar.eval (f i)) *
          (p.eval (f i) - pstar.eval (f i))).re = 0) :
    m ≤ maxModulus (Finset.univ.image f) p := by
  classical
  have hS : (Finset.univ.image f).Nonempty := by
    have hi : (Finset.univ : Finset ι).Nonempty := by
      by_contra hu
      have heu : (Finset.univ : Finset ι) = ∅ :=
        Finset.not_nonempty_iff_eq_empty.mp hu
      rw [heu] at hsum
      simp at hsum
    obtain ⟨i, hi⟩ := hi
    exact ⟨f i, Finset.mem_image.mpr ⟨i, hi, rfl⟩⟩
  have hm : 0 ≤ m := by
    obtain ⟨i, hi⟩ := hS
    rcases Finset.mem_image.mp hi with ⟨j, hj, rfl⟩
    rw [← hstar j]
    exact norm_nonneg _
  have hR : 0 ≤ maxModulus (Finset.univ.image f) p := by
    unfold maxModulus
    simp only [dif_pos hS]
    obtain ⟨z, hz⟩ := hS
    exact (norm_nonneg (p.eval z)).trans
      (Finset.le_sup' (fun w : ℂ => ‖p.eval w‖) hz)
  have hmax : ∀ i, ‖p.eval (f i)‖ ≤ maxModulus (Finset.univ.image f) p := by
    intro i
    unfold maxModulus
    simp only [dif_pos hS]
    exact Finset.le_sup' (fun z : ℂ => ‖p.eval z‖)
      (Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩)
  have henergy_nonneg : 0 ≤
      ∑ i, w i * ‖p.eval (f i) - pstar.eval (f i)‖ ^ 2 := by
    apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hweights i) (sq_nonneg _)
  have henergy_lower : m ^ 2 ≤ ∑ i, w i * ‖p.eval (f i)‖ ^ 2 := by
    rw [weighted_norm_sq_identity_indexed hweights hsum hstar horth]
    linarith
  have henergy_upper :
      ∑ i, w i * ‖p.eval (f i)‖ ^ 2 ≤
        (maxModulus (Finset.univ.image f) p) ^ 2 := by
    calc
      ∑ i, w i * ‖p.eval (f i)‖ ^ 2 ≤
          ∑ i, w i * (maxModulus (Finset.univ.image f) p) ^ 2 := by
        apply Finset.sum_le_sum
        intro i hi
        exact mul_le_mul_of_nonneg_left
          (by nlinarith [hmax i, norm_nonneg (p.eval (f i))])
          (hweights i)
      _ = (maxModulus (Finset.univ.image f) p) ^ 2 := by
        rw [← Finset.sum_mul, hsum, one_mul]
  nlinarith

def witnessKernel (a b : Fin 3) : ℂ :=
  (witnessWeight a b : ℂ) *
    conj (witnessPolynomial.eval (clusterPoint a b))

lemma witnessKernel_moment (ell : Fin 4) :
    ∑ a : Fin 3, ∑ b : Fin 3,
      witnessKernel a b * clusterPoint a b ^ (ell.val + 1) = 0 := by
  simpa [witnessKernel, mul_assoc] using weighted_moment ell

lemma weighted_cross_zero {q : Poly} (hdeg : q.natDegree ≤ 4)
    (hzero : q.eval 0 = 0) :
    ∑ a : Fin 3, ∑ b : Fin 3,
      witnessKernel a b * q.eval (clusterPoint a b) = 0 := by
  have hdeg_lt : q.natDegree < 5 := by omega
  have hc0 : q.coeff 0 = 0 := by
    rw [Polynomial.coeff_zero_eq_eval_zero]
    exact hzero
  have hq (z : ℂ) : q.eval z =
      q.coeff 1 * z + q.coeff 2 * z ^ 2 +
        q.coeff 3 * z ^ 3 + q.coeff 4 * z ^ 4 := by
    rw [Polynomial.eval_eq_sum_range' (p := q) hdeg_lt z]
    simp [Finset.sum_range_succ, hc0] <;> ring
  have hterm (j : Fin 4) :
      ∑ a : Fin 3, ∑ b : Fin 3,
        witnessKernel a b *
          (q.coeff (j.val + 1) * clusterPoint a b ^ (j.val + 1)) = 0 := by
    calc
      ∑ a : Fin 3, ∑ b : Fin 3,
          witnessKernel a b *
            (q.coeff (j.val + 1) * clusterPoint a b ^ (j.val + 1)) =
          ∑ a : Fin 3, ∑ b : Fin 3,
            q.coeff (j.val + 1) *
              (witnessKernel a b * clusterPoint a b ^ (j.val + 1)) := by
        apply Finset.sum_congr rfl
        intro a ha
        apply Finset.sum_congr rfl
        intro b hb
        ring
      _ = ∑ a : Fin 3, q.coeff (j.val + 1) *
          (∑ b : Fin 3,
            witnessKernel a b * clusterPoint a b ^ (j.val + 1)) := by
        apply Finset.sum_congr rfl
        intro a ha
        rw [← Finset.mul_sum]
      _ = q.coeff (j.val + 1) *
          (∑ a : Fin 3, ∑ b : Fin 3,
            witnessKernel a b * clusterPoint a b ^ (j.val + 1)) := by
        rw [← Finset.mul_sum]
      _ = 0 := by rw [witnessKernel_moment j, mul_zero]
  calc
    ∑ a : Fin 3, ∑ b : Fin 3,
        witnessKernel a b * q.eval (clusterPoint a b) =
        ∑ a : Fin 3, ∑ b : Fin 3,
          witnessKernel a b *
            (q.coeff 1 * clusterPoint a b +
              q.coeff 2 * clusterPoint a b ^ 2 +
              q.coeff 3 * clusterPoint a b ^ 3 +
              q.coeff 4 * clusterPoint a b ^ 4) := by
      apply Finset.sum_congr rfl
      intro a ha
      apply Finset.sum_congr rfl
      intro b hb
      rw [hq]
    _ = (∑ a : Fin 3, ∑ b : Fin 3,
          witnessKernel a b *
            (q.coeff 1 * clusterPoint a b)) +
        (∑ a : Fin 3, ∑ b : Fin 3,
          witnessKernel a b *
            (q.coeff 2 * clusterPoint a b ^ 2)) +
        (∑ a : Fin 3, ∑ b : Fin 3,
          witnessKernel a b *
            (q.coeff 3 * clusterPoint a b ^ 3)) +
        (∑ a : Fin 3, ∑ b : Fin 3,
          witnessKernel a b *
            (q.coeff 4 * clusterPoint a b ^ 4)) := by
      simp only [mul_add, Finset.sum_add_distrib]
    _ = 0 := by
      have h₁ := hterm (0 : Fin 4)
      have h₂ := hterm (1 : Fin 4)
      have h₃ := hterm (2 : Fin 4)
      have h₄ := hterm (3 : Fin 4)
      norm_num at h₁ h₂ h₃ h₄
      rw [h₁, h₂, h₃, h₄]
      ring

lemma witness_cross_real_zero {p : Poly} (hp : feasible explicitL 4 p) :
    ∑ a : Fin 3, ∑ b : Fin 3,
      witnessWeight a b *
        (conj (witnessPolynomial.eval (clusterPoint a b)) *
          (p.eval (clusterPoint a b) -
            witnessPolynomial.eval (clusterPoint a b))).re = 0 := by
  have hqdeg : (p - witnessPolynomial).natDegree ≤ 4 :=
    Polynomial.natDegree_sub_le_of_le hp.1 witness_feasible.1
  have hqzero : (p - witnessPolynomial).eval 0 = 0 := by
    rw [Polynomial.eval_sub, hp.2, witness_feasible.2]
    ring
  have hq := weighted_cross_zero hqdeg hqzero
  have hre := congrArg Complex.re hq
  simpa [witnessKernel, mul_assoc, Complex.re_sum,
    Complex.re_ofReal_mul] using hre

theorem witness_full_lower {p : Poly} (hp : feasible explicitL 4 p) :
    exactFullMinimum ≤ maxModulus explicitL p := by
  have hlower := weighted_minimum_lower_indexed
    (f := fun ab : Fin 3 × Fin 3 => clusterPoint ab.1 ab.2)
    (pstar := witnessPolynomial) (m := exactFullMinimum)
    (w := fun ab : Fin 3 × Fin 3 => witnessWeight ab.1 ab.2)
    (fun ab => le_of_lt (witnessWeight_pos ab.1 ab.2))
    (by
      simpa only [← Finset.sum_product', Finset.univ_product_univ] using
        witnessWeight_sum)
    (by
      intro ab
      exact witness_eval_norm ab.1 ab.2)
    (by simpa [explicitL] using hp)
    (by
      simpa only [← Finset.sum_product', Finset.univ_product_univ] using
        witness_cross_real_zero hp)
  simpa [explicitL] using hlower

lemma full_lower_bound_of_feasible {p : Poly} (hp : feasible explicitL 4 p) :
    fullLowerBound ≤ maxModulus explicitL p := by
  have hnum : fullLowerBound ≤ exactFullMinimum := by
    norm_num [fullLowerBound, exactFullMinimum]
  exact hnum.trans (witness_full_lower hp)

end NLA.IE16
