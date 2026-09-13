import NLA.RA20.Definitions

/-!
# RA-20 frozen-contract candidate (statement stage only)

The `sorry` terms in this reference module are intentional placeholders, not
proofs or accepted axioms. No `Proof.lean` or `Solution.lean` may be implemented
until two independent statement reviews and the coordinating gate are accepted.
The future Solution must export these exact theorem names and types, without
importing this module. Pure exact algebra; LeanCert kernel trust auditing only.
-/

noncomputable section
open scoped BigOperators
namespace NLA.RA20.AssemblyReference

theorem hollow_variety_semantics :
    (∀ a b c : ℂ, (hollow a b c).det = 2 * a * b * c ∧
      (hollow a b c ∈ variety 3 3 ↔ a * b * c = 0)) ∧
    (∀ X : Mat 3, X ∈ variety 3 3 ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧ X 0 1 * X 0 2 * X 1 2 = 0) := by
  sorry

/-- An actual coordinate-preserving isomorphism of the reduced coordinate rings. -/
theorem reduced_coordinate_ring :
    ∃ e : CoordinateRing 3 3 ≃ₐ[ℂ] ABCCoordinateRing,
      ∀ i j : Fin 3,
        e (Ideal.Quotient.mk (definingIdeal 3 3) (MvPolynomial.X (i, j))) =
          Ideal.Quotient.mk abcIdeal (polynomialHollow i j) := by
  sorry

theorem algebraic_smooth_locus (X : Mat 3) :
    SmoothPoint 3 3 X ↔
      X = hollow (X 0 1) (X 0 2) (X 1 2) ∧
        ExactlyOneZero (X 0 1) (X 0 2) (X 1 2) := by
  sorry

/-- Includes singular points: their larger Zariski tangent space is retained. -/
theorem algebraic_tangent_space (a b c : ℂ) (h : a * b * c = 0) (Z : Mat 3) :
    TangentVector 3 3 (hollow a b c) Z ↔
      Z.IsSymm ∧ (∀ i : Fin 3, Z i i = 0) ∧
        b * c * Z 0 1 + a * c * Z 0 2 + a * b * Z 1 2 = 0 := by
  sorry

theorem full_frobenius_differential (n : ℕ) (U X Z : Mat n) :
    fderiv ℂ (fullFrobeniusDistance U) X Z =
      2 * ∑ i, ∑ j, (X i j - U i j) * Z i j := by
  sorry

theorem hollow_distance_semantics (U : Mat 3) (hU : U.IsSymm) (a b c : ℂ) :
    fullFrobeniusDistance U (hollow a b c) =
      (∑ i, U i i ^ 2) +
        2 * ((a - U 0 1) ^ 2 + (b - U 0 2) ^ 2 + (c - U 1 2) ^ 2) := by
  sorry

/-- Exhaustion on an explicit nonempty open set, not just a single data matrix. -/
theorem generic_critical_locus (U : Mat 3) (hU : GenericData U) :
    criticalSet 3 3 U = Set.range (candidate U) ∧ Function.Injective (candidate U) := by
  sorry

/-- The actual second complex Fréchet derivative in each component chart.
The final implication states nondegeneracy of this bilinear Hessian. -/
theorem component_hessians (U : Mat 3) (i : Fin 3) (z h v : Fin 2 → ℂ) :
    ((fderiv ℂ (fun w => fderiv ℂ
      (fun y => fullFrobeniusDistance U (planeCoordinates i y)) w) z) h) v =
        4 * ∑ j, h j * v j ∧
    ((∀ v : Fin 2 → ℂ, (4 : ℂ) * ∑ j, h j * v j = 0) → h = 0) := by
  sorry

/-- Every nonempty principal open set of symmetric data meets the displayed
generic set. This supplies generic-count uniqueness without assuming it. -/
theorem generic_data_intersection (q : Poly 3)
    (hq : ∃ U : Mat 3, U.IsSymm ∧ MvPolynomial.eval (coordinates U) q ≠ 0) :
    ∃ U : Mat 3, GenericData U ∧ MvPolynomial.eval (coordinates U) q ≠ 0 := by
  sorry

theorem generic_count_three : HasGenericCriticalCount 3 3 3 := by
  sorry

theorem generic_count_not_four : ¬ HasGenericCriticalCount 3 3 4 := by
  sorry

theorem not_criticalCountConjecture : ¬ criticalCountConjecture := by
  sorry

end NLA.RA20.AssemblyReference
