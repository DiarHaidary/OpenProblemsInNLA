/-
Copyright (c) 2026 George Stepaniants. Released under Apache 2.0.
Formalization: Department of Computing and Mathematical Sciences,
California Institute of Technology. AI-assisted; source attribution is in SOURCE_MAP.md.

Exact algebra and one uniform inequality replace numerical subdivision.
The complete statement boundary was approved before this file was written.
-/
import NLA.SP06.Definitions
import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import LeanCert.Tactic.Verification

set_option autoImplicit false
set_option leancert.trust "kernel"
set_option maxHeartbeats 600000
noncomputable section

namespace NLA.SP06

theorem witness_admissible : hasAdmissibleBand witness := by
  refine ⟨2, 4, by norm_num, by norm_num, ?_, ?_⟩
  · intro k hk
    have h0 : k ≠ 0 := by omega
    have hm1 : k ≠ -1 := by omega
    have hm2 : k ≠ -2 := by omega
    have h1 : k ≠ 1 := by omega
    have h2 : k ≠ 2 := by omega
    have h3 : k ≠ 3 := by omega
    have h4 : k ≠ 4 := by omega
    simp [witness, h0, hm1, hm2, h1, h2, h3, h4]
  · norm_num [witness, Finsupp.single_apply]

theorem witness_composition (z : ℂ) (hz : z ≠ 0) :
    laurentEval witness z = auxiliary z - (auxiliary z) ^ 2 := by
  simp only [laurentEval, witness,
    Finsupp.sum_add_index' (h := fun (k : ℤ) (a : ℂ) => a * z ^ k)
      (fun _ => zero_mul _) (fun _ _ _ => add_mul _ _ _),
    Finsupp.sum_single_index (h := fun (k : ℤ) (a : ℂ) => a * z ^ k) (zero_mul _)]
  norm_num [auxiliary, zpow_neg, zpow_natCast]
  field_simp [hz]
  ring

theorem radial_lower_endpoint (c : ℝ) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    radialEquation (1 / 2) c ≤ -(23 / 32 : ℝ) ∧
      radialEquation (1 / 2) c < 0 := by
  dsimp [radialEquation]
  constructor <;> nlinarith [hc.2]

theorem radial_upper_endpoint (c : ℝ) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    1 ≤ radialEquation 2 c := by
  dsimp [radialEquation]
  nlinarith [hc.1]

theorem radial_uniform_slope (c s r : ℝ)
    (hc : c ∈ Set.Icc (-1 : ℝ) 1)
    (hs : (1 / 2 : ℝ) ≤ s) (hsr : s ≤ r) (hr : r ≤ 2) :
    (r - s) / 4 ≤ radialEquation r c - radialEquation s c := by
  have hs0 : 0 ≤ s := by linarith
  have hr0 : 0 ≤ r := by linarith
  have hs2 : s ≤ 2 := hsr.trans hr
  have hrr : r ^ 2 ≤ 2 * r := by nlinarith
  have hss : s ^ 2 ≤ 2 * s := by nlinarith
  have hrs : r * s ≤ r + s := by nlinarith [sq_nonneg (r - s)]
  have hk : 0 ≤ r ^ 2 + r * s + s ^ 2 :=
    add_nonneg (add_nonneg (sq_nonneg r) (mul_nonneg hr0 hs0)) (sq_nonneg s)
  have hck := mul_nonneg (show 0 ≤ c + 1 by linarith [hc.1]) hk
  have hb : (1 / 4 : ℝ) ≤ r + s + c * (r ^ 2 + r * s + s ^ 2) / 4 := by
    nlinarith
  have hm := mul_nonneg (sub_nonneg.mpr hsr) (sub_nonneg.mpr hb)
  have hid : radialEquation r c - radialEquation s c =
      (r - s) * (r + s + c * (r ^ 2 + r * s + s ^ 2) / 4) := by
    dsimp [radialEquation]
    ring
  rw [hid]
  nlinarith

private theorem roots_ordered_bound (c d r s : ℝ)
    (hc : c ∈ Set.Icc (-1 : ℝ) 1)
    (hr : r ∈ Set.Ioo (1 / 2 : ℝ) 2) (hs : s ∈ Set.Ioo (1 / 2 : ℝ) 2)
    (hcr : radialEquation r c = 0) (hds : radialEquation s d = 0)
    (hrs : r ≤ s) : s - r ≤ 8 * |c - d| := by
  have hsep := radial_uniform_slope c r s hc hr.1.le hrs hs.2.le
  rw [hcr, sub_zero] at hsep
  have hs0 : 0 ≤ s := by linarith [hs.1]
  have hcoef0 : 0 ≤ s ^ 3 / 4 := by positivity
  have hcoef2 : s ^ 3 / 4 ≤ 2 := by
    have hs2 : s ^ 2 ≤ 4 := by nlinarith [hs.2]
    have hmul := mul_le_mul_of_nonneg_left hs2 hs0
    nlinarith [hs.2]
  have hid : radialEquation s c = (s ^ 3 / 4) * (c - d) := by
    dsimp [radialEquation] at hds ⊢
    nlinarith
  have hab : |radialEquation s c| ≤ 2 * |c - d| := by
    rw [hid, abs_mul, abs_of_nonneg hcoef0]
    exact mul_le_mul_of_nonneg_right hcoef2 (abs_nonneg _)
  have hle := le_abs_self (radialEquation s c)
  linarith

theorem radial_roots_lipschitz (c d r s : ℝ)
    (hc : c ∈ Set.Icc (-1 : ℝ) 1) (hd : d ∈ Set.Icc (-1 : ℝ) 1)
    (hr : r ∈ Set.Ioo (1 / 2 : ℝ) 2) (hs : s ∈ Set.Ioo (1 / 2 : ℝ) 2)
    (hcr : radialEquation r c = 0) (hds : radialEquation s d = 0) :
    |r - s| ≤ 8 * |c - d| := by
  rcases le_total r s with hrs | hsr
  · rw [abs_of_nonpos (sub_nonpos.mpr hrs)]
    have h := roots_ordered_bound c d r s hc hr hs hcr hds hrs
    linarith
  · rw [abs_of_nonneg (sub_nonneg.mpr hsr)]
    simpa only [abs_sub_comm d c] using
      roots_ordered_bound d c s r hd hs hr hds hcr hsr

theorem witness_toeplitz_two :
    toeplitz witness 2 = !![(-128 : ℂ), 8; -8, -128] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [toeplitz, witness, Finsupp.single_apply]

theorem witness_eigenvalue_mem :
    nonrealEigenvalue ∈ spectrum ℂ (toeplitz witness 2) := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly, Polynomial.IsRoot,
    Matrix.eval_charpoly, witness_toeplitz_two, Matrix.det_fin_two]
  norm_num [nonrealEigenvalue, Matrix.scalar, Matrix.diagonal_apply]
  ring_nf
  simp

theorem witness_eigenvalue_im : nonrealEigenvalue.im = 8 := by
  norm_num [nonrealEigenvalue]

#assert_trust kernel witness_admissible
#assert_trust kernel witness_composition
#assert_trust kernel radial_lower_endpoint
#assert_trust kernel radial_upper_endpoint
#assert_trust kernel radial_uniform_slope
#assert_trust kernel radial_roots_lipschitz
#assert_trust kernel witness_toeplitz_two
#assert_trust kernel witness_eigenvalue_mem
#assert_trust kernel witness_eigenvalue_im

end NLA.SP06
