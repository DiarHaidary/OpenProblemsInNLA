/-
Copyright (c) 2026 George Stepaniants. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: George Stepaniants

Department of Computing and Mathematical Sciences, California Institute of
Technology, Pasadena, California, USA. AI-assisted formalization.
The negative-resolution mathematics retains the Codex automated maintainer audit
attribution. This proves the generic-open intersection required by its exact target.
-/
import NLA.RA20.Definitions
import Mathlib.Algebra.MvPolynomial.Funext
import Mathlib.Tactic.FinCases
import LeanCert.Tactic.Verification

set_option autoImplicit false
set_option leancert.trust "kernel"
noncomputable section
namespace NLA.RA20

/-- Six independent coordinates of a symmetric three-by-three data matrix. -/
def symmetricParameterIndex (ij : Variables 3) : Fin 6 :=
  !![(0 : Fin 6), 3, 4; 3, 1, 5; 4, 5, 2] ij.1 ij.2

def symmetricParameter (z : Fin 6 → ℂ) : Mat 3 :=
  fun i j => z (symmetricParameterIndex (i,j))

def symmetricDataCoordinates (U : Mat 3) : Fin 6 → ℂ :=
  ![U 0 0, U 1 1, U 2 2, U 0 1, U 0 2, U 1 2]

theorem symmetricParameter_isSymm (z : Fin 6 → ℂ) :
    (symmetricParameter z).IsSymm := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem symmetricParameter_reconstruct (U : Mat 3) (hU : U.IsSymm) :
    symmetricParameter (symmetricDataCoordinates U) = U := by
  have h01 := hU.apply 0 1
  have h02 := hU.apply 0 2
  have h12 := hU.apply 1 2
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [symmetricParameter, symmetricParameterIndex, symmetricDataCoordinates,
      h01, h02, h12]

theorem eval_rename_symmetricParameter (z : Fin 6 → ℂ) (q : Poly 3) :
    MvPolynomial.eval z (MvPolynomial.rename symmetricParameterIndex q) =
      MvPolynomial.eval (coordinates (symmetricParameter z)) q := by
  rw [MvPolynomial.eval_rename]
  rfl

/-- The unknown exceptional polynomial remains arbitrary. Restrict it to the
full six-dimensional symmetric space and multiply by the three off-diagonal
coordinates. Nonzero polynomial evaluation over the infinite field supplies a
point avoiding both exceptional sets; diagonal coordinates stay unrestricted. -/
theorem generic_data_intersection_proved (q : Poly 3)
    (hq : ∃ U : Mat 3, U.IsSymm ∧ MvPolynomial.eval (coordinates U) q ≠ 0) :
    ∃ U : Mat 3, GenericData U ∧ MvPolynomial.eval (coordinates U) q ≠ 0 := by
  classical
  obtain ⟨U, hU, hqU⟩ := hq
  let f : MvPolynomial (Fin 6) ℂ := MvPolynomial.rename symmetricParameterIndex q
  have hf : f ≠ 0 := by
    intro hfzero
    apply hqU
    have h := eval_rename_symmetricParameter (symmetricDataCoordinates U) q
    rw [symmetricParameter_reconstruct U hU] at h
    change MvPolynomial.eval (symmetricDataCoordinates U) f = _ at h
    rw [hfzero, map_zero] at h
    exact h.symm
  let g : MvPolynomial (Fin 6) ℂ :=
    f * MvPolynomial.X 3 * MvPolynomial.X 4 * MvPolynomial.X 5
  have hg : g ≠ 0 := by
    dsimp [g]
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero hf
      (MvPolynomial.X_ne_zero 3)) (MvPolynomial.X_ne_zero 4))
      (MvPolynomial.X_ne_zero 5)
  have hex : ∃ z : Fin 6 → ℂ, MvPolynomial.eval z g ≠ 0 := by
    by_contra hn
    push Not at hn
    apply hg
    apply MvPolynomial.funext
    intro z
    simpa only [map_zero] using hn z
  obtain ⟨z, hz⟩ := hex
  have hproduct : MvPolynomial.eval z f * (z 3 * z 4 * z 5) ≠ 0 := by
    simpa only [g, map_mul, MvPolynomial.eval_X, mul_assoc] using hz
  obtain ⟨hfz, hcoords⟩ := mul_ne_zero_iff.mp hproduct
  refine ⟨symmetricParameter z, ⟨symmetricParameter_isSymm z, ?_⟩, ?_⟩
  · change z 3 * z 4 * z 5 ≠ 0
    exact hcoords
  · change MvPolynomial.eval z f ≠ 0 at hfz
    rw [show f = MvPolynomial.rename symmetricParameterIndex q from rfl,
      eval_rename_symmetricParameter] at hfz
    exact hfz

#assert_trust kernel symmetricParameter_isSymm
#print axioms symmetricParameter_isSymm
#assert_trust kernel symmetricParameter_reconstruct
#print axioms symmetricParameter_reconstruct
#assert_trust kernel eval_rename_symmetricParameter
#print axioms eval_rename_symmetricParameter
#assert_trust kernel generic_data_intersection_proved
#print axioms generic_data_intersection_proved

end NLA.RA20
