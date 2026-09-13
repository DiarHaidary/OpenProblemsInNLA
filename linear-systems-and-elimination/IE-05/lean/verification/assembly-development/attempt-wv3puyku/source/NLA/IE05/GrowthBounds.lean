import NLA.IE05.GEPP

/-!
# IE-05: generic bounds for positively scaled entries and actual growth

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.
AI-assisted formalization after the accepted statement gate.

The approved integer inequalities imply these real bounds symbolically.
No numerical square-root enclosure or subdivision is needed.
-/

set_option leancert.trust "kernel"
noncomputable section

namespace NLA.IE05._proved

theorem abs_div_sqrt_le {x d c a : ℝ} (hd : 0 < d) (hc : 0 < c)
    (ha : 0 ≤ a) (h : c * x ^ 2 ≤ a ^ 2 * d) :
    |x / Real.sqrt d| ≤ a / Real.sqrt c := by
  apply (sq_le_sq₀ (abs_nonneg _) (div_nonneg ha (Real.sqrt_nonneg c))).mp
  rw [sq_abs, div_pow, div_pow, Real.sq_sqrt hd.le, Real.sq_sqrt hc.le]
  exact (div_le_div_iff₀ hd hc).mpr (by nlinarith only [h])

theorem abs_div_sqrt_le_sqrt {x d C : ℝ} (hd : 0 < d) (hC : 0 ≤ C)
    (h : x ^ 2 ≤ C * d) : |x / Real.sqrt d| ≤ Real.sqrt C := by
  apply (sq_le_sq₀ (abs_nonneg _) (Real.sqrt_nonneg C)).mp
  rw [sq_abs, div_pow, Real.sq_sqrt hd.le, Real.sq_sqrt hC]
  exact (div_le_iff₀ hd).mpr h

theorem entryMax_le_from_entries {n : ℕ} (A : Mat n) (C : ℝ) (hC : 0 ≤ C)
    (h : ∀ i j, |A i j| ≤ C) : entryMax A ≤ C := by
  rw [← activeMax_zero_proved A]
  exact activeMax_le_proved A 0 C hC (fun i j _ _ => h i j)

theorem growth_nonneg {n : ℕ} (A : Mat n) (path : PivotPath n) :
    0 ≤ growth A path := by
  exact div_nonneg (NNReal.coe_nonneg _) (entryMax_nonneg_proved A)

#print axioms abs_div_sqrt_le
#assert_trust kernel abs_div_sqrt_le
#print axioms abs_div_sqrt_le_sqrt
#assert_trust kernel abs_div_sqrt_le_sqrt
#print axioms entryMax_le_from_entries
#assert_trust kernel entryMax_le_from_entries
#print axioms growth_nonneg
#assert_trust kernel growth_nonneg

end NLA.IE05._proved
