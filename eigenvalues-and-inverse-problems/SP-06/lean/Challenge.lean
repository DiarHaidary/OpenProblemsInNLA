import NLA.SP06.Definitions

set_option autoImplicit false

/-!
Statement boundary only. Deliberate placeholders are not proofs and will
never be imported by Solution. The statements must receive two independent
reviews before implementation. In particular, the existence and regularity
of the entire real Jordan curve are proof obligations, not assumptions in
the final negative resolution.
-/
namespace NLA.SP06

theorem witness_admissible : hasAdmissibleBand witness := by
  sorry

theorem witness_composition (z : ℂ) (hz : z ≠ 0) :
    laurentEval witness z = auxiliary z - (auxiliary z) ^ 2 := by
  sorry

theorem radial_lower_endpoint (c : ℝ) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    radialEquation (1 / 2) c ≤ -(23 / 32 : ℝ) ∧
      radialEquation (1 / 2) c < 0 := by
  sorry

theorem radial_upper_endpoint (c : ℝ) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    1 ≤ radialEquation 2 c := by
  sorry

theorem radial_uniform_slope (c s r : ℝ)
    (hc : c ∈ Set.Icc (-1 : ℝ) 1)
    (hs : (1 / 2 : ℝ) ≤ s) (hsr : s ≤ r) (hr : r ≤ 2) :
    (r - s) / 4 ≤ radialEquation r c - radialEquation s c := by
  sorry

theorem radial_root_exists_unique (c : ℝ) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    ∃! r : ℝ, r ∈ Set.Ioo (1 / 2 : ℝ) 2 ∧ radialEquation r c = 0 := by
  sorry

theorem radial_roots_lipschitz (c d r s : ℝ)
    (hc : c ∈ Set.Icc (-1 : ℝ) 1) (hd : d ∈ Set.Icc (-1 : ℝ) 1)
    (hr : r ∈ Set.Ioo (1 / 2 : ℝ) 2) (hs : s ∈ Set.Ioo (1 / 2 : ℝ) 2)
    (hcr : radialEquation r c = 0) (hds : radialEquation s d = 0) :
    |r - s| ≤ 8 * |c - d| := by
  sorry

theorem continuous_radius_exists : ∃ ρ : Circle → ℝ, radiusProfile ρ := by
  sorry

theorem radial_curve_continuous (ρ : Circle → ℝ) (hρ : Continuous ρ) :
    Continuous (radialCurve ρ) := by
  sorry

theorem radial_curve_injective (ρ : Circle → ℝ) (hρ : ∀ u, 0 < ρ u) :
    Function.Injective (radialCurve ρ) := by
  sorry

theorem radial_curve_nonzero (ρ : Circle → ℝ) (hρ : ∀ u, 0 < ρ u) :
    ∀ u, radialCurve ρ u ≠ 0 := by
  sorry

theorem auxiliary_radial_im (r : ℝ) (hr : 0 < r) (u : Circle) :
    (auxiliary ((r : ℂ) * (u : ℂ))).im =
      (8 * (u : ℂ).im / r) * radialEquation r (u : ℂ).re := by
  sorry

theorem radial_curve_symbol_real (ρ : Circle → ℝ) (hρ : radiusProfile ρ) :
    ∀ u, (laurentEval witness (radialCurve ρ u)).im = 0 := by
  sorry

theorem witness_real_jordan_curve : hasRealJordanCurve witness := by
  sorry

theorem witness_toeplitz_two :
    toeplitz witness 2 = !![(-128 : ℂ), 8; -8, -128] := by
  sorry

theorem witness_eigenvalue_mem :
    nonrealEigenvalue ∈ spectrum ℂ (toeplitz witness 2) := by
  sorry

theorem witness_eigenvalue_im : nonrealEigenvalue.im = 8 := by
  sorry

theorem witness_nonreal_finite_spectrum : ¬ allFiniteSpectraReal witness := by
  sorry

theorem witness_counterexample : counterexampleClaim := by
  sorry

theorem not_targetImplication : ¬ targetImplication := by
  sorry

end NLA.SP06
