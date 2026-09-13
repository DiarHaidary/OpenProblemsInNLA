/-
Copyright (c) 2026 George Stepaniants. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: George Stepaniants

Proof-independent statement boundary for IE-16.  The original negative
resolution and analytic proof are due to Sidney Holden.  This file records
the exact finite-set, complex-polynomial formulation and the disclosed
nine-point counterexample; it contains no proof or imported solution.
-/
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.Polynomial.Basic
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Algebra.Polynomial.Degree.Defs
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Finset.Powerset

set_option autoImplicit false
open scoped BigOperators Classical
noncomputable section

namespace NLA.IE16

abbrev Poly := Polynomial ℂ

/- The finite maximum is totalized at the empty set.  All occurrences in the
   canonical target have nonempty sets, since k >= 1 and |L| >= 3. -/
def maxModulus (L : Finset ℂ) (p : Poly) : ℝ :=
  if hL : L.Nonempty then L.sup' hL (fun z => ‖p.eval z‖) else 0

def feasible (L : Finset ℂ) (k : ℕ) (p : Poly) : Prop :=
  p.natDegree ≤ k ∧ p.eval 0 = 1

def feasibleValues (L : Finset ℂ) (k : ℕ) : Set ℝ :=
  {r | ∃ p : Poly, feasible L k p ∧ maxModulus L p = r}

/- This is exactly M_k(L), with the finite maximum above and the infimum over
   all complex polynomials of degree at most k normalized by p(0)=1. -/
def M (L : Finset ℂ) (k : ℕ) : ℝ := sInf (feasibleValues L k)

def subsetFamily (L : Finset ℂ) (k : ℕ) : Finset (Finset ℂ) :=
  L.powerset.filter (fun S => S.card = k + 1)

/- This is B_k(L) = max_{S subset L, |S|=k+1} M_k(S).  The empty-family
   branch is irrelevant under the canonical admissibility hypotheses. -/
def subsetMax (L : Finset ℂ) (k : ℕ) : ℝ :=
  if hS : (subsetFamily L k).Nonempty then
    (subsetFamily L k).sup' hS (fun S => M S k)
  else 0

def admissible (L : Finset ℂ) (n : ℕ) : Prop :=
  L.card = n ∧ ∀ z ∈ L, z ≠ 0

/- The complete original universal assertion.  Finset membership already
   supplies distinctness, while admissible records cardinality and exclusion
   of zero. -/
def IE16Conjecture : Prop :=
  ∀ n : ℕ, 3 ≤ n → ∀ L : Finset ℂ, admissible L n →
    ∀ k : ℕ, 1 ≤ k → k ≤ n - 2 →
      M L k ≤ (4 / Real.pi) * subsetMax L k

/- Exact data from Holden's nine-point counterexample. -/
def omega : ℂ :=
  (-1 / 2 : ℂ) + (Complex.ofReal (Real.sqrt 3) / 2) * Complex.I

def epsilon : ℂ := (1 / 1000 : ℂ)

def clusterPoint (a b : Fin 3) : ℂ :=
  omega ^ (a : ℕ) + epsilon * omega ^ (b : ℕ)

def explicitL : Finset ℂ :=
  (Finset.univ : Finset (Fin 3 × Fin 3)).image
    (fun ab => clusterPoint ab.1 ab.2)

def denominator : ℂ :=
  1 + epsilon + 3 * epsilon ^ 2 + epsilon ^ 3 + epsilon ^ 4

def witnessPolynomial : Poly :=
  Polynomial.C 1 -
    Polynomial.C ((1 + epsilon) / denominator) * Polynomial.X ^ 3

def exactFullMinimum : ℝ := 3003003000 / 1001003001001
def fullLowerBound : ℝ := 299 / 100000
def subsetUpperBound : ℝ := 23 / 10000
def ratioLowerBound : ℝ := 13 / 10

/- The finite counterexample certificate is kept as separate propositions so
   each numerical bridge is visible to statement reviewers. -/
def ExplicitCertificate : Prop :=
  explicitL.card = 9 ∧
  admissible explicitL 9 ∧
  feasible explicitL 4 witnessPolynomial ∧
  M explicitL 4 = exactFullMinimum ∧
  IsLeast (feasibleValues explicitL 4) (M explicitL 4) ∧
  fullLowerBound < M explicitL 4 ∧
  (∀ S : Finset ℂ, S ∈ subsetFamily explicitL 4 →
    M S 4 < subsetUpperBound) ∧
  (∀ S : Finset ℂ, S ∈ subsetFamily explicitL 4 →
    IsLeast (feasibleValues S 4) (M S 4)) ∧
  subsetMax explicitL 4 < subsetUpperBound ∧
  0 < subsetMax explicitL 4 ∧
  ratioLowerBound < M explicitL 4 / subsetMax explicitL 4 ∧
  (4 / Real.pi) < ratioLowerBound

end NLA.IE16

/- Statement-only Comparator challenge for IE-16.  The placeholders are
   intentional and must be replaced in Solution.lean only after two
   independent statement reviews. -/
set_option autoImplicit false
open scoped BigOperators Classical
noncomputable section

namespace NLA.IE16

theorem explicitL_card : explicitL.card = 9 := by sorry

theorem explicitL_admissible : admissible explicitL 9 := by sorry

theorem witness_feasible : feasible explicitL 4 witnessPolynomial := by sorry

theorem witness_objective :
    maxModulus explicitL witnessPolynomial = exactFullMinimum := by sorry

theorem full_minimum_exact : M explicitL 4 = exactFullMinimum := by sorry

theorem full_minimum_isLeast :
    IsLeast (feasibleValues explicitL 4) (M explicitL 4) := by sorry

theorem full_lower_bound : fullLowerBound < M explicitL 4 := by sorry

theorem every_five_point_subset_upper :
    ∀ S : Finset ℂ, S ∈ subsetFamily explicitL 4 →
      M S 4 < subsetUpperBound := by sorry

theorem every_five_point_subset_minimum_isLeast :
    ∀ S : Finset ℂ, S ∈ subsetFamily explicitL 4 →
      IsLeast (feasibleValues S 4) (M S 4) := by sorry

theorem subset_max_upper : subsetMax explicitL 4 < subsetUpperBound := by sorry

theorem subset_max_positive : 0 < subsetMax explicitL 4 := by sorry

theorem ratio_lower_bound :
    ratioLowerBound < M explicitL 4 / subsetMax explicitL 4 := by sorry

theorem ratio_exceeds_candidate : (4 / Real.pi) < ratioLowerBound := by sorry

theorem counterexample : ExplicitCertificate := by sorry

/- This is the negation of the complete universal assertion, rather than a
   theorem restricted to the fixed witness or to the certificate's dimensions. -/
theorem not_IE16Conjecture : ¬ IE16Conjecture := by sorry

end NLA.IE16
