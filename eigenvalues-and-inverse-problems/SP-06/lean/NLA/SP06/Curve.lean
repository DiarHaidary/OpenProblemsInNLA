/-
Copyright (c) 2026 George Stepaniants. Released under Apache 2.0.
Formalization: Department of Computing and Mathematical Sciences,
California Institute of Technology. AI-assisted.

The radius is selected from the unique roots on one fixed interval. A
uniform Lipschitz estimate proves continuity on the entire actual circle.
-/
import NLA.SP06.Numeric
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Tactic.FunProp

set_option autoImplicit false
set_option leancert.trust "kernel"
set_option maxHeartbeats 600000
noncomputable section

namespace NLA.SP06

theorem radial_root_exists_unique (c : ℝ) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    ∃! r : ℝ, r ∈ Set.Ioo (1 / 2 : ℝ) 2 ∧ radialEquation r c = 0 := by
  have hl := (radial_lower_endpoint c hc).2
  have hu := radial_upper_endpoint c hc
  have hf : Continuous (fun r : ℝ => radialEquation r c) := by
    unfold radialEquation
    fun_prop
  have hz : (0 : ℝ) ∈ Set.Icc (radialEquation (1 / 2) c) (radialEquation 2 c) :=
    ⟨hl.le, by linarith⟩
  obtain ⟨r, hr, hrc⟩ := intermediate_value_Icc (by norm_num : (1 / 2 : ℝ) ≤ 2)
    hf.continuousOn hz
  change radialEquation r c = 0 at hrc
  have hrl : (1 / 2 : ℝ) < r := by
    apply lt_of_le_of_ne hr.1
    intro heq
    rw [← heq] at hrc
    linarith
  have hru : r < 2 := by
    apply lt_of_le_of_ne hr.2
    intro heq
    rw [heq] at hrc
    linarith
  refine ⟨r, ⟨⟨hrl, hru⟩, hrc⟩, ?_⟩
  intro s hs
  rcases le_total r s with hrs | hsr
  · have h := radial_uniform_slope c r s hc hr.1 hrs hs.1.2.le
    rw [hrc, hs.2] at h
    linarith
  · have h := radial_uniform_slope c s r hc hs.1.1.le hsr hr.2
    rw [hrc, hs.2] at h
    linarith

private theorem circle_re_bounds (u : Circle) : (u : ℂ).re ∈ Set.Icc (-1 : ℝ) 1 := by
  have h := Complex.abs_re_le_norm (u : ℂ)
  rw [Circle.norm_coe] at h
  exact abs_le.mp h

theorem continuous_radius_exists : ∃ ρ : Circle → ℝ, radiusProfile ρ := by
  classical
  have hroot (u : Circle) := (radial_root_exists_unique (u : ℂ).re (circle_re_bounds u)).exists
  choose ρ hρ using hroot
  refine ⟨ρ, ?_, hρ⟩
  have hLip : LipschitzWith 8 ρ := by
    apply LipschitzWith.of_dist_le_mul
    intro u v
    have h := radial_roots_lipschitz (u : ℂ).re (v : ℂ).re (ρ u) (ρ v)
      (circle_re_bounds u) (circle_re_bounds v) (hρ u).1 (hρ v).1
      (hρ u).2 (hρ v).2
    have hre : |(u : ℂ).re - (v : ℂ).re| ≤ dist u v := by
      change |(u : ℂ).re - (v : ℂ).re| ≤ dist (u : ℂ) (v : ℂ)
      simpa only [Complex.sub_re, dist_eq_norm] using
        Complex.abs_re_le_norm ((u : ℂ) - (v : ℂ))
    have hmul := mul_le_mul_of_nonneg_left hre (by norm_num : (0 : ℝ) ≤ 8)
    simpa only [Real.dist_eq, NNReal.coe_ofNat] using h.trans hmul
  exact hLip.continuous

theorem radial_curve_continuous (ρ : Circle → ℝ) (hρ : Continuous ρ) :
    Continuous (radialCurve ρ) := by
  unfold radialCurve
  exact (Complex.continuous_ofReal.comp hρ).mul continuous_subtype_val

theorem radial_curve_injective (ρ : Circle → ℝ) (hρ : ∀ u, 0 < ρ u) :
    Function.Injective (radialCurve ρ) := by
  intro u v huv
  have hn := congrArg norm huv
  simp only [radialCurve, norm_mul, Complex.norm_real, Circle.norm_coe, mul_one,
    Real.norm_eq_abs, abs_of_pos (hρ u), abs_of_pos (hρ v)] at hn
  apply Circle.coe_injective
  apply mul_left_cancel₀ (show (ρ u : ℂ) ≠ 0 by exact_mod_cast (hρ u).ne')
  simpa only [radialCurve, hn] using huv

theorem radial_curve_nonzero (ρ : Circle → ℝ) (hρ : ∀ u, 0 < ρ u) :
    ∀ u, radialCurve ρ u ≠ 0 := by
  intro u
  exact mul_ne_zero (by exact_mod_cast (hρ u).ne') (Circle.coe_ne_zero u)

theorem auxiliary_radial_im (r : ℝ) (hr : 0 < r) (u : Circle) :
    (auxiliary ((r : ℂ) * (u : ℂ))).im =
      (8 * (u : ℂ).im / r) * radialEquation r (u : ℂ).re := by
  have hu : (u : ℂ)⁻¹ = (starRingEnd ℂ) (u : ℂ) := by
    simpa only [Circle.coe_inv] using Circle.coe_inv_eq_conj u
  simp only [auxiliary, div_eq_mul_inv, mul_inv_rev, hu, ← Complex.ofReal_inv,
    Complex.add_im, Complex.mul_im, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, Complex.conj_re, Complex.conj_im, pow_two,
    zero_mul, mul_zero, add_zero, zero_add]
  norm_num [radialEquation]
  field_simp [hr.ne']
  ring

theorem radial_curve_symbol_real (ρ : Circle → ℝ) (hρ : radiusProfile ρ) :
    ∀ u, (laurentEval witness (radialCurve ρ u)).im = 0 := by
  have hp (u : Circle) : 0 < ρ u := by linarith [(hρ.2 u).1.1]
  intro u
  rw [witness_composition _ (radial_curve_nonzero ρ hp u)]
  have hi := auxiliary_radial_im (ρ u) (hp u) u
  rw [(hρ.2 u).2, mul_zero] at hi
  change (auxiliary (radialCurve ρ u)).im = 0 at hi
  simp [Complex.sub_im, pow_two, Complex.mul_im, hi]

theorem witness_real_jordan_curve : hasRealJordanCurve witness := by
  obtain ⟨ρ, hρ⟩ := continuous_radius_exists
  have hp (u : Circle) : 0 < ρ u := by linarith [(hρ.2 u).1.1]
  exact ⟨radialCurve ρ, radial_curve_continuous ρ hρ.1,
    radial_curve_injective ρ hp, radial_curve_nonzero ρ hp,
    radial_curve_symbol_real ρ hρ⟩

#assert_trust kernel radial_root_exists_unique
#assert_trust kernel continuous_radius_exists
#assert_trust kernel radial_curve_continuous
#assert_trust kernel radial_curve_injective
#assert_trust kernel radial_curve_nonzero
#assert_trust kernel auxiliary_radial_im
#assert_trust kernel radial_curve_symbol_real
#assert_trust kernel witness_real_jordan_curve

end NLA.SP06
