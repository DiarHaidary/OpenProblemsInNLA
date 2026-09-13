import NLA.RA20.Proof

/-!
# RA-20: exact reviewed final exports

Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
Original negative resolution: the repository's Codex automated maintainer audit;
original conjecture: Kubjas, Sodomaco and Tsigaridas.

Every type below is the unchanged reviewed contract. Each proof is supplied by
its genuine implementation; the reference Challenge is never imported.
All original parameter ranges and algebraic geometric semantics are retained.
Actual Linux Comparator verification and independent final review are separate
subsequent gates, not asserted by this source file.
-/

noncomputable section
open scoped BigOperators
namespace NLA.RA20

theorem hollow_variety_semantics :
    (∀ a b c : ℂ, (hollow a b c).det = 2 * a * b * c ∧
      (hollow a b c ∈ variety 3 3 ↔ a * b * c = 0)) ∧
    (∀ X : Mat 3, X ∈ variety 3 3 ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧ X 0 1 * X 0 2 * X 1 2 = 0) := by
  exact hollow_variety_semantics_proved

/-- An actual coordinate-preserving isomorphism of the reduced coordinate rings. -/
theorem reduced_coordinate_ring :
    ∃ e : CoordinateRing 3 3 ≃ₐ[ℂ] ABCCoordinateRing,
      ∀ i j : Fin 3,
        e (Ideal.Quotient.mk (definingIdeal 3 3) (MvPolynomial.X (i, j))) =
          Ideal.Quotient.mk abcIdeal (polynomialHollow i j) := by
  exact reduced_coordinate_ring_proved

theorem algebraic_smooth_locus (X : Mat 3) :
    SmoothPoint 3 3 X ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧
        ExactlyOneZero (X 0 1) (X 0 2) (X 1 2) := by
  exact algebraic_smooth_locus_proved X

/-- Includes singular points: their larger Zariski tangent space is retained. -/
theorem algebraic_tangent_space (a b c : ℂ) (h : a * b * c = 0) (Z : Mat 3) :
    TangentVector 3 3 (hollow a b c) Z ↔
      Z.IsSymm ∧ (∀ i : Fin 3, Z i i = 0) ∧
        b * c * Z 0 1 + a * c * Z 0 2 + a * b * Z 1 2 = 0 := by
  exact algebraic_tangent_space_proved a b c h Z

theorem full_frobenius_differential (n : ℕ) (U X Z : Mat n) :
    fderiv ℂ (fullFrobeniusDistance U) X Z =
      2 * ∑ i, ∑ j, (X i j - U i j) * Z i j := by
  exact full_frobenius_differential_proved n U X Z

theorem hollow_distance_semantics (U : Mat 3) (hU : U.IsSymm) (a b c : ℂ) :
    fullFrobeniusDistance U (hollow a b c) =
      (∑ i, U i i ^ 2) +
        2 * ((a - U 0 1) ^ 2 + (b - U 0 2) ^ 2 + (c - U 1 2) ^ 2) := by
  exact hollow_distance_semantics_proved U hU a b c

/-- Exhaustion on an explicit nonempty open set, not just a single data matrix. -/
theorem generic_critical_locus (U : Mat 3) (hU : GenericData U) :
    criticalSet 3 3 U = Set.range (candidate U) ∧ Function.Injective (candidate U) := by
  exact generic_critical_locus_proved U hU

/-- The actual second complex Fréchet derivative in each component chart.
The final implication states nondegeneracy of this bilinear Hessian. -/
theorem component_hessians (U : Mat 3) (i : Fin 3) (z h v : Fin 2 → ℂ) :
    ((fderiv ℂ (fun w => fderiv ℂ
      (fun y => fullFrobeniusDistance U (planeCoordinates i y)) w) z) h) v =
        4 * ∑ j, h j * v j ∧
    ((∀ v : Fin 2 → ℂ, (4 : ℂ) * ∑ j, h j * v j = 0) → h = 0) := by
  exact component_hessians_proved U i z h v

/-- Every nonempty principal open set of symmetric data meets the displayed
generic set. This supplies generic-count uniqueness without assuming it. -/
theorem generic_data_intersection (q : Poly 3)
    (hq : ∃ U : Mat 3, U.IsSymm ∧ MvPolynomial.eval (coordinates U) q ≠ 0) :
    ∃ U : Mat 3, GenericData U ∧ MvPolynomial.eval (coordinates U) q ≠ 0 := by
  exact generic_data_intersection_proved q hq

theorem generic_count_three : HasGenericCriticalCount 3 3 3 := by
  exact generic_count_three_proved

theorem generic_count_not_four : ¬ HasGenericCriticalCount 3 3 4 := by
  exact generic_count_not_four_proved

theorem not_criticalCountConjecture : ¬ criticalCountConjecture := by
  exact not_criticalCountConjecture_proved

set_option leancert.trust "kernel"

#assert_trust kernel hollow_variety_semantics
#print axioms hollow_variety_semantics
#assert_trust kernel reduced_coordinate_ring
#print axioms reduced_coordinate_ring
#assert_trust kernel algebraic_smooth_locus
#print axioms algebraic_smooth_locus
#assert_trust kernel algebraic_tangent_space
#print axioms algebraic_tangent_space
#assert_trust kernel full_frobenius_differential
#print axioms full_frobenius_differential
#assert_trust kernel hollow_distance_semantics
#print axioms hollow_distance_semantics
#assert_trust kernel generic_critical_locus
#print axioms generic_critical_locus
#assert_trust kernel component_hessians
#print axioms component_hessians
#assert_trust kernel generic_data_intersection
#print axioms generic_data_intersection
#assert_trust kernel generic_count_three
#print axioms generic_count_three
#assert_trust kernel generic_count_not_four
#print axioms generic_count_not_four
#assert_trust kernel not_criticalCountConjecture
#print axioms not_criticalCountConjecture

end NLA.RA20
