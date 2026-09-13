/-
RA-20: exhaustion of the actual smooth critical set on the full generic open set.
Formalization: George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA, with AI assistance.
Original resolution: Codex automated maintainer audit; conjecture of Kubjas,
Sodomaco and Tsigaridas. The actual smooth, tangent and differential helpers
retain their separately recorded implementation and Mathlib attribution.
-/
import NLA.RA20.Smooth
import NLA.RA20.Differential
import NLA.RA20.Tangent

set_option autoImplicit false
set_option leancert.trust "kernel"
noncomputable section
open scoped BigOperators
namespace NLA.RA20

theorem smoothPoint_hollow_iff (a b c : ℂ) :
    SmoothPoint 3 3 (hollow a b c) ↔ ExactlyOneZero a b c := by
  simpa [hollow] using algebraic_smooth_locus_proved (hollow a b c)

/-- The actual full-entry derivative on arbitrary hollow directions. -/
theorem hollow_frobenius_differential (U : Mat 3) (hU : U.IsSymm)
    (a b c u v w : ℂ) :
    fderiv ℂ (fullFrobeniusDistance U) (hollow a b c) (hollow u v w) =
      4 * ((a - U 0 1) * u + (b - U 0 2) * v + (c - U 1 2) * w) := by
  rw [full_frobenius_differential_proved]
  have h10 : U 1 0 = U 0 1 := hU.apply 0 1
  have h20 : U 2 0 = U 0 2 := hU.apply 0 2
  have h21 : U 2 1 = U 1 2 := hU.apply 1 2
  simp [hollow, Fin.sum_univ_succ, h10, h20, h21]
  ring

theorem generic_coordinates_ne_zero (U : Mat 3) (hU : GenericData U) :
    U 0 1 ≠ 0 ∧ U 0 2 ≠ 0 ∧ U 1 2 ≠ 0 := by
  have h := mul_ne_zero_iff.mp hU.2
  exact ⟨(mul_ne_zero_iff.mp h.1).1, (mul_ne_zero_iff.mp h.1).2, h.2⟩

theorem generic_candidate_injective (U : Mat 3) (hU : GenericData U) :
    Function.Injective (candidate U) := by
  have hn := generic_coordinates_ne_zero U hU
  intro i j h
  have h01 := congrArg (fun Z : Mat 3 ↦ Z 0 1) h
  have h02 := congrArg (fun Z : Mat 3 ↦ Z 0 2) h
  have h12 := congrArg (fun Z : Mat 3 ↦ Z 1 2) h
  fin_cases i <;> fin_cases j <;> simp_all [candidate, hollow]

#assert_trust kernel hollow_frobenius_differential
#print axioms hollow_frobenius_differential
#assert_trust kernel generic_candidate_injective
#print axioms generic_candidate_injective

theorem exactlyOneZero_product_zero (a b c : ℂ) (h : ExactlyOneZero a b c) :
    a * b * c = 0 := by
  rcases h with h | h | h
  · simp only [h.1, zero_mul]
  · simp only [h.2.1, mul_zero, zero_mul]
  · simp only [h.2.2, mul_zero]

/-- The full-ideal tangent characterization on arbitrary hollow directions. -/
theorem hollow_tangent_iff (a b c u v w : ℂ) (hz : a * b * c = 0) :
    TangentVector 3 3 (hollow a b c) (hollow u v w) ↔
      b * c * u + a * c * v + a * b * w = 0 := by
  rw [algebraic_tangent_space_proved a b c hz]
  constructor
  · intro h
    exact h.2.2
  · intro h
    refine ⟨hollow_isSymm u v w, ?_, h⟩
    intro i; fin_cases i <;> rfl

/-- Orthogonality to the actual entire-ideal tangent space, derived from the
genuine derivative. The quantifiers range over every complex tangent direction. -/
theorem smoothCritical_hollow_iff (U : Mat 3) (hU : U.IsSymm) (a b c : ℂ) :
    SmoothCriticalPoint 3 3 U (hollow a b c) ↔
      ExactlyOneZero a b c ∧ ∀ u v w : ℂ,
        b * c * u + a * c * v + a * b * w = 0 →
        (a - U 0 1) * u + (b - U 0 2) * v + (c - U 1 2) * w = 0 := by
  constructor
  · rintro ⟨hs, hc⟩
    have hone := (smoothPoint_hollow_iff a b c).mp hs
    have hz := exactlyOneZero_product_zero a b c hone
    refine ⟨hone, ?_⟩
    intro u v w ht
    have hd := hc (hollow u v w) ((hollow_tangent_iff a b c u v w hz).mpr ht)
    rw [hollow_frobenius_differential U hU] at hd
    exact (mul_eq_zero.mp hd).resolve_left (by norm_num)
  · rintro ⟨hone, hc⟩
    refine ⟨(smoothPoint_hollow_iff a b c).mpr hone, ?_⟩
    intro Z hZ
    have hz := exactlyOneZero_product_zero a b c hone
    have ht := (algebraic_tangent_space_proved a b c hz Z).mp hZ
    have he := matrix_eq_hollow_of_symm_diag Z ht.1 ht.2.1
    have hsum := hc (Z 0 1) (Z 0 2) (Z 1 2) ht.2.2
    rw [he, hollow_frobenius_differential U hU, hsum, mul_zero]

theorem critical_first_plane (U : Mat 3) (hU : U.IsSymm) (b c : ℂ)
    (hb : b ≠ 0) (hc : c ≠ 0) :
    SmoothCriticalPoint 3 3 U (hollow 0 b c) ↔ b = U 0 2 ∧ c = U 1 2 := by
  rw [smoothCritical_hollow_iff U hU]
  constructor
  · rintro ⟨_, h⟩
    have h1 := h 0 1 0 (by simp)
    have h2 := h 0 0 1 (by simp)
    exact ⟨sub_eq_zero.mp (by simpa using h1), sub_eq_zero.mp (by simpa using h2)⟩
  · rintro ⟨rfl, rfl⟩
    refine ⟨Or.inl ⟨rfl, hb, hc⟩, ?_⟩
    intro u v w h
    have hu : u = 0 := (mul_eq_zero.mp (by simpa using h)).resolve_left (mul_ne_zero hb hc)
    simp [hu]

theorem critical_second_plane (U : Mat 3) (hU : U.IsSymm) (a c : ℂ)
    (ha : a ≠ 0) (hc : c ≠ 0) :
    SmoothCriticalPoint 3 3 U (hollow a 0 c) ↔ a = U 0 1 ∧ c = U 1 2 := by
  rw [smoothCritical_hollow_iff U hU]
  constructor
  · rintro ⟨_, h⟩
    have h1 := h 1 0 0 (by simp)
    have h2 := h 0 0 1 (by simp)
    exact ⟨sub_eq_zero.mp (by simpa using h1), sub_eq_zero.mp (by simpa using h2)⟩
  · rintro ⟨rfl, rfl⟩
    refine ⟨Or.inr (Or.inl ⟨ha, rfl, hc⟩), ?_⟩
    intro u v w h
    have hv : v = 0 := (mul_eq_zero.mp (by simpa using h)).resolve_left (mul_ne_zero ha hc)
    simp [hv]

theorem critical_third_plane (U : Mat 3) (hU : U.IsSymm) (a b : ℂ)
    (ha : a ≠ 0) (hb : b ≠ 0) :
    SmoothCriticalPoint 3 3 U (hollow a b 0) ↔ a = U 0 1 ∧ b = U 0 2 := by
  rw [smoothCritical_hollow_iff U hU]
  constructor
  · rintro ⟨_, h⟩
    have h1 := h 1 0 0 (by simp)
    have h2 := h 0 1 0 (by simp)
    exact ⟨sub_eq_zero.mp (by simpa using h1), sub_eq_zero.mp (by simpa using h2)⟩
  · rintro ⟨rfl, rfl⟩
    refine ⟨Or.inr (Or.inr ⟨ha, hb, rfl⟩), ?_⟩
    intro u v w h
    have hw : w = 0 := (mul_eq_zero.mp (by simpa using h)).resolve_left (mul_ne_zero ha hb)
    simp [hw]

#assert_trust kernel smoothCritical_hollow_iff
#print axioms smoothCritical_hollow_iff
#assert_trust kernel critical_first_plane
#print axioms critical_first_plane
#assert_trust kernel critical_second_plane
#print axioms critical_second_plane
#assert_trust kernel critical_third_plane
#print axioms critical_third_plane

theorem generic_candidate_critical (U : Mat 3) (hU : GenericData U) (i : Fin 3) :
    SmoothCriticalPoint 3 3 U (candidate U i) := by
  obtain ⟨h01, h02, h12⟩ := generic_coordinates_ne_zero U hU
  fin_cases i
  · change SmoothCriticalPoint 3 3 U (hollow 0 (U 0 2) (U 1 2))
    exact (critical_first_plane U hU.1 _ _ h02 h12).mpr ⟨rfl, rfl⟩
  · change SmoothCriticalPoint 3 3 U (hollow (U 0 1) 0 (U 1 2))
    exact (critical_second_plane U hU.1 _ _ h01 h12).mpr ⟨rfl, rfl⟩
  · change SmoothCriticalPoint 3 3 U (hollow (U 0 1) (U 0 2) 0)
    exact (critical_third_plane U hU.1 _ _ h01 h02).mpr ⟨rfl, rfl⟩

/-- Every actual smooth critical point lies in one of the three proved charts. -/
theorem generic_critical_exhaustion (U : Mat 3) (hU : GenericData U)
    (X : Mat 3) (hX : SmoothCriticalPoint 3 3 U X) :
    ∃ i : Fin 3, candidate U i = X := by
  obtain ⟨hshape, hone⟩ := (algebraic_smooth_locus_proved X).mp hX.1
  have hx : SmoothCriticalPoint 3 3 U (hollow (X 0 1) (X 0 2) (X 1 2)) := hshape ▸ hX
  rcases hone with ⟨h0, h1, h2⟩ | ⟨h0, h1, h2⟩ | ⟨h0, h1, h2⟩
  · rw [h0] at hx
    obtain ⟨hb, hc⟩ := (critical_first_plane U hU.1 _ _ h1 h2).mp hx
    refine ⟨0, ?_⟩
    change hollow 0 (U 0 2) (U 1 2) = X
    rw [hshape, h0, hb, hc]
  · rw [h1] at hx
    obtain ⟨ha, hc⟩ := (critical_second_plane U hU.1 _ _ h0 h2).mp hx
    refine ⟨1, ?_⟩
    change hollow (U 0 1) 0 (U 1 2) = X
    rw [hshape, h1, ha, hc]
  · rw [h2] at hx
    obtain ⟨ha, hb⟩ := (critical_third_plane U hU.1 _ _ h0 h1).mp hx
    refine ⟨2, ?_⟩
    change hollow (U 0 1) (U 0 2) 0 = X
    rw [hshape, h2, ha, hb]

/-- Exact frozen contract 7: equality with the entire actual critical set and
injectivity of its three-matrix enumeration, for every datum in the full open set. -/
theorem generic_critical_locus_proved (U : Mat 3) (hU : GenericData U) :
    criticalSet 3 3 U = Set.range (candidate U) ∧ Function.Injective (candidate U) := by
  refine ⟨?_, generic_candidate_injective U hU⟩
  ext X
  constructor
  · exact generic_critical_exhaustion U hU X
  · rintro ⟨i, rfl⟩
    exact generic_candidate_critical U hU i

#assert_trust kernel generic_candidate_critical
#print axioms generic_candidate_critical
#assert_trust kernel generic_critical_exhaustion
#print axioms generic_critical_exhaustion
#assert_trust kernel generic_critical_locus_proved
#print axioms generic_critical_locus_proved

end NLA.RA20
