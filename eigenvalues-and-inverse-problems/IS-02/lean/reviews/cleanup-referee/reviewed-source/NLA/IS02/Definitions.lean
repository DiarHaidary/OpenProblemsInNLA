import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Polynomial.Roots

set_option autoImplicit false
noncomputable section
open scoped BigOperators

namespace NLA.IS02

abbrev Mat (n : ℕ) := Matrix (Fin n) (Fin n) ℝ

def symmetric {n : ℕ} (A : Mat n) : Prop := ∀ i j, A i j = A j i

def entrywiseNonnegative {n : ℕ} (A : Mat n) : Prop := ∀ i j, 0 ≤ A i j

def stochastic {n : ℕ} (A : Mat n) : Prop :=
  ∀ i, (∑ j : Fin n, A i j) = 1

def symmetricStochastic (n : ℕ) : Set (Mat n) :=
  {A | symmetric A ∧ entrywiseNonnegative A ∧ stochastic A}

def trace {n : ℕ} (A : Mat n) : ℝ := ∑ i : Fin n, A i i

def permute {n : ℕ} (σ : Equiv.Perm (Fin n)) (A : Mat n) : Mat n :=
  fun i j => A (σ i) (σ j)

def permutationSimilar {n : ℕ} (A B : Mat n) : Prop :=
  ∃ σ : Equiv.Perm (Fin n), B = permute σ A

/-- For real symmetric matrices, characteristic-polynomial equality is the
exact finite-dimensional encoding of equality of eigenvalues with
multiplicities used by the source theorem. The explicit bridge contract below
must connect this encoding to the real root multiset. -/
def sameSpectrum {n : ℕ} (A B : Mat n) : Prop :=
  Matrix.charpoly A = Matrix.charpoly B

/- The roots multiset retains algebraic multiplicity. For a symmetric matrix
the characteristic polynomial splits over ℝ; that splitting and the converse
monic-polynomial reconstruction are part of the Challenge bridge theorem. -/
def realEigenvalueMultiset {n : ℕ} (A : Mat n) : Multiset ℝ :=
  (Matrix.charpoly A).roots

def spectrallyUnique {n : ℕ} (A : Mat n) : Prop :=
  ∀ B, B ∈ symmetricStochastic n → sameSpectrum A B → permutationSimilar A B

def segment {n : ℕ} (X Y : Mat n) : Set (Mat n) :=
  {Z | ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ Z = (1 - t) • X + t • Y}

def vertex (n : ℕ) (V : Mat n) : Prop :=
  V ∈ symmetricStochastic n ∧
    ∀ U W, U ∈ symmetricStochastic n → W ∈ symmetricStochastic n →
      ∀ t : ℝ, 0 ≤ t → t ≤ 1 →
        V = (1 - t) • U + t • W → t = 0 ∨ t = 1 ∨ U = W

def flatMatrix (n : ℕ) : Mat n :=
  fun i j => if i = j then 0 else (1 : ℝ) / ((n - 1 : ℕ) : ℝ)

def assertedLocus (n : ℕ) : Set (Mat n) :=
  segment (1 : Mat n) (flatMatrix n) ∪
    {A | ∃ V, vertex n V ∧ (A ∈ segment (1 : Mat n) V ∨
      A ∈ segment (flatMatrix n) V)}

def counterexample : Mat 4 :=
  !![(0 : ℝ), 1, 0, 0;
     1, 0, 0, 0;
     0, 0, (1 / 2 : ℝ), (1 / 2 : ℝ);
     0, 0, (1 / 2 : ℝ), (1 / 2 : ℝ)]

def targetNecessaryCondition : Prop :=
  ∀ n, 4 ≤ n → ∀ A : Mat n,
    A ∈ symmetricStochastic n → 0 < trace A →
    spectrallyUnique A → A ∈ assertedLocus n

def counterexampleClaim : Prop :=
  counterexample ∈ symmetricStochastic 4 ∧
  0 < trace counterexample ∧
  sameSpectrum counterexample
    (!![(1 : ℝ), 0, 0, 0;
        0, 1, 0, 0;
        0, 0, 0, 0;
        0, 0, 0, (-1 : ℝ)]) ∧
  spectrallyUnique counterexample ∧
  counterexample ∉ assertedLocus 4

end NLA.IS02
