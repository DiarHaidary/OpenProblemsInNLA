import Mathlib.Analysis.Complex.Circle
import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Finsupp.Basic

set_option autoImplicit false
noncomputable section

namespace NLA.SP06

/-- The coefficients of a finite complex Laurent polynomial. -/
abbrev LaurentCoefficients := ℤ →₀ ℂ

def laurentEval (b : LaurentCoefficients) (z : ℂ) : ℂ :=
  b.sum (fun k a => a * z ^ k)

/-- The original positive lower and upper bandwidths and nonzero extremes. -/
def hasAdmissibleBand (b : LaurentCoefficients) : Prop :=
  ∃ r s : ℕ, 1 ≤ r ∧ 1 ≤ s ∧
    (∀ k : ℤ, k < -(r : ℤ) ∨ (s : ℤ) < k → b k = 0) ∧
    b (-(r : ℤ)) * b (s : ℤ) ≠ 0

def toeplitz (b : LaurentCoefficients) (n : ℕ) :
    Matrix (Fin n) (Fin n) ℂ :=
  fun i j => b ((i.val : ℤ) - (j.val : ℤ))

/-- A genuine Jordan curve, as the continuous injective image of the unit
circle, avoiding zero and contained in the real locus of the symbol. -/
def hasRealJordanCurve (b : LaurentCoefficients) : Prop :=
  ∃ γ : Circle → ℂ, Continuous γ ∧ Function.Injective γ ∧
    (∀ u, γ u ≠ 0) ∧ (∀ u, (laurentEval b (γ u)).im = 0)

/-- The actual algebra spectrum of every positive finite Toeplitz section. -/
def allFiniteSpectraReal (b : LaurentCoefficients) : Prop :=
  ∀ n : ℕ, 1 ≤ n → ∀ z : ℂ, z ∈ spectrum ℂ (toeplitz b n) → z.im = 0

def targetImplication : Prop :=
  ∀ b : LaurentCoefficients,
    hasAdmissibleBand b → hasRealJordanCurve b → allFiniteSpectraReal b

def witness : LaurentCoefficients :=
  Finsupp.single (-2) (-64) + Finsupp.single (-1) 8 +
  Finsupp.single 0 (-128) + Finsupp.single 1 (-8) +
  Finsupp.single 2 (-63) + Finsupp.single 3 (-16) +
  Finsupp.single 4 (-1)

def auxiliary (z : ℂ) : ℂ := 8 / z + 8 * z + z ^ 2

def radialEquation (r c : ℝ) : ℝ := r ^ 2 - 1 + (r ^ 3 / 4) * c

def radiusProfile (ρ : Circle → ℝ) : Prop :=
  Continuous ρ ∧ ∀ u : Circle,
    ρ u ∈ Set.Ioo (1 / 2 : ℝ) 2 ∧ radialEquation (ρ u) (u : ℂ).re = 0

def radialCurve (ρ : Circle → ℝ) (u : Circle) : ℂ :=
  (ρ u : ℂ) * (u : ℂ)

def nonrealEigenvalue : ℂ := -128 + 8 * Complex.I

def counterexampleClaim : Prop :=
  hasAdmissibleBand witness ∧ hasRealJordanCurve witness ∧
    ¬ allFiniteSpectraReal witness

end NLA.SP06
