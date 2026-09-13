/-
Copyright (c) 2026 George Stepaniants. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: George Stepaniants

Statement-stage formalization of NR-03.  This file deliberately contains
definitions only.  In particular, the finite n = 7 certificate is not
represented by an unverified imported data file: its exact entrywise identity
is a later proof obligation in Challenge.lean.

Department of Computing and Mathematical Sciences, California Institute of
Technology, Pasadena, California, USA.  AI-assisted formalization.
-/
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Notation

set_option autoImplicit false
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

/-- A Boolean vector with exactly `n` coordinates. -/
abbrev BoolVec (n : ℕ) := Fin n → Bool

/-- The real value represented by one Boolean coordinate. -/
def boolToReal (b : Bool) : ℝ := if b = true then 1 else 0

/-- The ordinary real dot product of two Boolean vectors. -/
def boolDot {n : ℕ} (a b : BoolVec n) : ℝ :=
  ∑ i : Fin n, boolToReal (a i) * boolToReal (b i)

/-- The complete prescribed quadratic correlation matrix.  The subtraction is
over `ℝ`, so entries with dot product greater than one are retained exactly. -/
def cMatrix (n : ℕ) : Matrix (BoolVec n) (BoolVec n) ℝ :=
  fun a b => (1 - boolDot a b) ^ 2

/-- Entrywise nonnegativity of a real matrix. -/
def EntrywiseNonnegative {ι κ : Type} (X : Matrix ι κ ℝ) : Prop :=
  ∀ i j, 0 ≤ X i j

/-- A genuine real nonnegative factorization of a matrix through `Fin r`. -/
def FactorizationData {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ) (r : ℕ)
    (W : Matrix ι (Fin r) ℝ) (H : Matrix (Fin r) κ ℝ) : Prop :=
  EntrywiseNonnegative W ∧ EntrywiseNonnegative H ∧ W * H = X

/-- Existence of a real entrywise-nonnegative factorization of width `r`. -/
def HasNonnegativeFactorization {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ) (r : ℕ) : Prop :=
  ∃ W : Matrix ι (Fin r) ℝ, ∃ H : Matrix (Fin r) κ ℝ,
    FactorizationData X r W H

/-- The actual minimum width whenever at least one finite factorization exists.
The value `0` in the impossible branch is only a totalization; all rank
claims below carry the explicit existence premise or establish it first. -/
def nonnegativeRank {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ) : ℕ :=
  by
    classical
    exact if h : ∃ r : ℕ, HasNonnegativeFactorization X r then Nat.find h else 0

/-- The original universal question, over all Boolean vectors and all entries
of the prescribed real matrix. -/
def targetStatement : Prop :=
  ∀ n : ℕ, 3 ≤ n → nonnegativeRank (cMatrix n) = 2 ^ n

/-- Integer-valued matrices are used only to state the exact finite certificate;
their entries are cast to `ℝ` before the matrix identity is asserted. -/
def castNatMatrix {ι κ : Type}
    (M : Matrix ι κ ℕ) : Matrix ι κ ℝ :=
  fun i j => (M i j : ℝ)

/-- The genuine right factor obtained by dividing each integer certificate
column by its positive integer denominator. -/
def scaledRightFactor {κ : Type} {r : ℕ}
    (V : Matrix (Fin r) κ ℕ) (d : κ → ℕ) : Matrix (Fin r) κ ℝ :=
  fun k j => (V k j : ℝ) / (d j : ℝ)

/-- A full exact integer certificate for a real matrix.  No correctness
hypothesis is hidden: the displayed entrywise identity is the obligation. -/
def HasScaledIntegerCertificate {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ) (r : ℕ) : Prop :=
  ∃ W : Matrix ι (Fin r) ℕ,
    ∃ V : Matrix (Fin r) κ ℕ,
      ∃ d : κ → ℕ,
        (∀ j, 0 < d j) ∧
        (∀ i j,
          (castNatMatrix W * castNatMatrix V) i j =
            (d j : ℝ) * X i j)

end NLA.NR03
