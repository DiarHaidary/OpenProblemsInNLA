/- IE-16 subset-bound helpers.

The numerical statements were written first in SUBSET_BOUND_OPTIMIZATION.md.
These generic estimates avoid repeating irrational arithmetic for all 126
subsets and supply the complete five-point-subset bound.

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology. AI-assisted formalization.
-/
import NLA.IE16.Minimax
import Mathlib.Algebra.Order.BigOperators.GroupWithZero.Finset
import Mathlib.Data.Fintype.Powerset

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators
noncomputable section

namespace NLA.IE16.SubsetBounds

def pointLower : ℝ := 999 / 1000
def nearUpper : ℝ := 13 / 7500
def farUpper : ℝ := 2603 / 1500

lemma rational_pair_margin :
    109 * nearUpper * farUpper ^ 3 < pointLower ^ 4 := by
  norm_num [nearUpper, farUpper, pointLower]

lemma rational_triple_margin :
    146 * nearUpper ^ 2 * farUpper ^ 2 < pointLower ^ 4 := by
  norm_num [nearUpper, farUpper, pointLower]

lemma sqrt_three_upper : Real.sqrt 3 < (26 / 15 : ℝ) := by
  have hs := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)
  have hn := Real.sqrt_nonneg (3 : ℝ)
  nlinarith

lemma coefficient_norm_product (S : Finset ℂ) (z : ℂ) :
    ‖lagrangeBasisAtZero S z‖ =
      (∏ w ∈ S.erase z, ‖w‖) / (∏ w ∈ S.erase z, ‖z - w‖) := by
  classical
  simp only [lagrangeBasisAtZero, Lagrange.basis, Polynomial.eval_prod,
    Lagrange.basisDivisor, Polynomial.eval_mul, Polynomial.eval_C,
    Polynomial.eval_sub, Polynomial.eval_X, id_eq, zero_sub,
    norm_prod, norm_mul, norm_inv, norm_neg, Finset.prod_mul_distrib,
    Finset.prod_inv_distrib, div_eq_mul_inv]
  ring

lemma denominator_positive {S : Finset ℂ} {z : ℂ} :
    0 < ∏ w ∈ S.erase z, ‖z - w‖ := by
  classical
  apply Finset.prod_pos
  intro w hw
  exact norm_pos_iff.mpr (sub_ne_zero.mpr (Finset.mem_erase.mp hw).1.symm)

lemma numerator_lower {S : Finset ℂ} {z : ℂ}
    (hcard : S.card = 5) (hz : z ∈ S)
    (hpoint : ∀ w ∈ S, pointLower ≤ ‖w‖) :
    pointLower ^ 4 ≤ ∏ w ∈ S.erase z, ‖w‖ := by
  classical
  calc
    pointLower ^ 4 = ∏ _w ∈ S.erase z, pointLower := by
      simp [Finset.prod_const, Finset.card_erase_of_mem hz, hcard]
    _ ≤ ∏ w ∈ S.erase z, ‖w‖ := by
      apply Finset.prod_le_prod
      · intro w hw
        norm_num [pointLower]
      · intro w hw
        exact hpoint w (Finset.mem_of_mem_erase hw)

lemma denominator_upper {S H : Finset ℂ} {z : ℂ} {h : ℕ}
    (hcard : S.card = 5) (hz : z ∈ S)
    (hH : H ⊆ S.erase z) (hHcard : H.card = h)
    (hnear : ∀ w ∈ H, ‖z - w‖ ≤ nearUpper)
    (hfar : ∀ w ∈ S.erase z, ‖z - w‖ ≤ farUpper) :
    (∏ w ∈ S.erase z, ‖z - w‖) ≤
      nearUpper ^ h * farUpper ^ (4 - h) := by
  classical
  have hrestcard : ((S.erase z) \ H).card = 4 - h := by
    rw [Finset.card_sdiff_of_subset hH, Finset.card_erase_of_mem hz,
      hcard, hHcard]
  have hprodH : (∏ w ∈ H, ‖z - w‖) ≤ nearUpper ^ h := by
    calc
      (∏ w ∈ H, ‖z - w‖) ≤ ∏ _w ∈ H, nearUpper :=
        Finset.prod_le_prod (fun w _ => norm_nonneg _) hnear
      _ = nearUpper ^ h := by rw [Finset.prod_const, hHcard]
  have hprodRest : (∏ w ∈ (S.erase z) \ H, ‖z - w‖) ≤
      farUpper ^ (4 - h) := by
    calc
      (∏ w ∈ (S.erase z) \ H, ‖z - w‖) ≤
          ∏ _w ∈ (S.erase z) \ H, farUpper := by
        apply Finset.prod_le_prod (fun w _ => norm_nonneg _)
        intro w hw
        exact hfar w (Finset.mem_sdiff.mp hw).1
      _ = farUpper ^ (4 - h) := by rw [Finset.prod_const, hrestcard]
  rw [← Finset.prod_sdiff hH]
  calc
    (∏ w ∈ (S.erase z) \ H, ‖z - w‖) * (∏ w ∈ H, ‖z - w‖) ≤
        farUpper ^ (4 - h) * nearUpper ^ h :=
      mul_le_mul hprodRest hprodH
        (Finset.prod_nonneg (fun w _ => norm_nonneg _))
        (pow_nonneg (by norm_num [farUpper]) _)
    _ = nearUpper ^ h * farUpper ^ (4 - h) := mul_comm _ _

lemma coefficient_gt_of_close_subset {S H : Finset ℂ} {z : ℂ}
    {h : ℕ} {c : ℝ}
    (hcard : S.card = 5) (hz : z ∈ S)
    (hpoint : ∀ w ∈ S, pointLower ≤ ‖w‖)
    (hH : H ⊆ S.erase z) (hHcard : H.card = h)
    (hnear : ∀ w ∈ H, ‖z - w‖ ≤ nearUpper)
    (hfar : ∀ w ∈ S.erase z, ‖z - w‖ ≤ farUpper)
    (hc : 0 ≤ c)
    (hmargin : c * (nearUpper ^ h * farUpper ^ (4 - h)) < pointLower ^ 4) :
    c < ‖lagrangeBasisAtZero S z‖ := by
  classical
  rw [coefficient_norm_product]
  apply (lt_div_iff₀ denominator_positive).mpr
  calc
    c * (∏ w ∈ S.erase z, ‖z - w‖) ≤
        c * (nearUpper ^ h * farUpper ^ (4 - h)) :=
      mul_le_mul_of_nonneg_left
        (denominator_upper hcard hz hH hHcard hnear hfar) hc
    _ < pointLower ^ 4 := hmargin
    _ ≤ ∏ w ∈ S.erase z, ‖w‖ := numerator_lower hcard hz hpoint

lemma pair_coefficient_gt {S H : Finset ℂ} {z : ℂ}
    (hcard : S.card = 5) (hz : z ∈ S)
    (hpoint : ∀ w ∈ S, pointLower ≤ ‖w‖)
    (hH : H ⊆ S.erase z) (hHcard : H.card = 1)
    (hnear : ∀ w ∈ H, ‖z - w‖ ≤ nearUpper)
    (hfar : ∀ w ∈ S.erase z, ‖z - w‖ ≤ farUpper) :
    (109 : ℝ) < ‖lagrangeBasisAtZero S z‖ := by
  apply coefficient_gt_of_close_subset hcard hz hpoint hH hHcard hnear hfar
    (by norm_num)
  simpa only [pow_one, Nat.reduceSub, mul_assoc] using rational_pair_margin

lemma triple_coefficient_gt {S H : Finset ℂ} {z : ℂ}
    (hcard : S.card = 5) (hz : z ∈ S)
    (hpoint : ∀ w ∈ S, pointLower ≤ ‖w‖)
    (hH : H ⊆ S.erase z) (hHcard : H.card = 2)
    (hnear : ∀ w ∈ H, ‖z - w‖ ≤ nearUpper)
    (hfar : ∀ w ∈ S.erase z, ‖z - w‖ ≤ farUpper) :
    (146 : ℝ) < ‖lagrangeBasisAtZero S z‖ := by
  apply coefficient_gt_of_close_subset hcard hz hpoint hH hHcard hnear hfar
    (by norm_num)
  simpa only [Nat.reduceSub, mul_assoc] using rational_triple_margin

abbrev Grid := Fin 3 × Fin 3

def companionCount (S : Finset Grid) (z : Grid) : ℕ :=
  ((S.erase z).filter (fun w => w.1 = z.1)).card

/- This finite statement is pure nine-label combinatorics, with no complex
   arithmetic or interval evaluation. It includes every five-element subset.
   If it is expensive remotely, replace the finite proof by the 2,2,1 versus
   3,a,b occupancy argument; never remove any subset from the statement. -/
set_option maxRecDepth 10000 in
set_option maxHeartbeats 2000000 in
lemma occupancy_disjunction : ∀ S : Finset Grid, S.card = 5 →
    4 ≤ (S.filter (fun z => 1 ≤ companionCount S z)).card ∨
    3 ≤ (S.filter (fun z => 2 ≤ companionCount S z)).card := by
  decide

lemma sum_gt_from_many_terms {ι : Type*} [DecidableEq ι]
    {S T : Finset ι} {f : ι → ℝ} {n : ℕ} {c : ℝ}
    (hTS : T ⊆ S) (hn : 0 < n) (hcard : n ≤ T.card)
    (hc : 0 ≤ c) (hterm : ∀ z ∈ T, c < f z)
    (hnonneg : ∀ z ∈ S, 0 ≤ f z) :
    (n : ℝ) * c < ∑ z ∈ S, f z := by
  have hT : T.Nonempty := Finset.card_pos.mp (lt_of_lt_of_le hn hcard)
  have hcast : (n : ℝ) ≤ (T.card : ℝ) := by exact_mod_cast hcard
  calc
    (n : ℝ) * c ≤ (T.card : ℝ) * c := mul_le_mul_of_nonneg_right hcast hc
    _ = ∑ _z ∈ T, c := by simp
    _ < ∑ z ∈ T, f z := Finset.sum_lt_sum_of_nonempty hT hterm
    _ ≤ ∑ z ∈ S, f z :=
      Finset.sum_le_sum_of_subset_of_nonneg hTS (fun z hz _ => hnonneg z hz)

end NLA.IE16.SubsetBounds
