import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.LinearAlgebra.Matrix.PosDef

/-!
# KE-04: block Krylov spaces and genuine compression spectra

Original mathematical proof: Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge.
Prospective formalization: George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California, USA.

This is an AI-assisted statement-only draft. No proof implementation is included.
All spaces, matrix actions, orthogonality and eigenvalues below are actual
Mathlib objects; interval occupancy and nonannihilation are not data assumptions.
-/

noncomputable section
open scoped BigOperators

namespace NLA.KE04

abbrev Vec (n : ℕ) := EuclideanSpace ℝ (Fin n)
abbrev Rect (n m : ℕ) := Matrix (Fin n) (Fin m) ℝ
abbrev Mat (n : ℕ) := Rect n n

def column {n m : ℕ} (M : Rect n m) (j : Fin m) : Vec n :=
  WithLp.toLp 2 (fun i => M i j)

/-- The genuine matrix action on the L2 Euclidean space. -/
def act {n m : ℕ} (M : Rect n m) : Vec m →ₗ[ℝ] Vec n :=
  Matrix.toEuclideanLin M

def columnSpace {n m : ℕ} (M : Rect n m) : Submodule ℝ (Vec n) :=
  Submodule.span ℝ (Set.range (column M))

def FullColumnRank {n p : ℕ} (V : Rect n p) : Prop :=
  LinearIndependent ℝ (column V)

/-- Degree is the first index; the second index selects a starting-block column. -/
def krylovColumns {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    Fin ell × Fin p → Vec n :=
  fun rc => column (A ^ rc.1.val * V) rc.2

/-- Exactly the span of the columns of [V, A V, ..., A^(ell-1) V]. -/
def krylov {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    Submodule ℝ (Vec n) :=
  Submodule.span ℝ (Set.range (krylovColumns A V ell))

def krylovCombination {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) :
    (Fin ell × Fin p → ℝ) →ₗ[ℝ] Vec n :=
  Fintype.linearCombination ℝ (krylovColumns A V ell)

/-- Actual dimension, with no eigenvalue or polynomial condition attached. -/
def FullBlockDimension {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ) : Prop :=
  Module.finrank ℝ (krylov A V ell) = ell * p

/-- The canonical maximality convention. For p=0 there is no largest such index. -/
def LastFullBlockIteration {n p : ℕ} (A : Mat n) (V : Rect n p) (s : ℕ) : Prop :=
  FullBlockDimension A V s ∧ ∀ t, FullBlockDimension A V t → t ≤ s

/-- Arbitrary orthonormal columns spanning the exact Krylov space.
No compatibility or block-tridiagonal premise is imposed between iterations. -/
def IsKrylovBasis {n p : ℕ} (A : Mat n) (V : Rect n p) (ell : ℕ)
    (Q : Rect n (ell * p)) : Prop :=
  Q.transpose * Q = 1 ∧ columnSpace Q = krylov A V ell

def frameProjection {n m : ℕ} (Q : Rect n m) : Mat n :=
  Q * Q.conjTranspose

/-- Over the real field this is exactly Q.transpose * A * Q. -/
def compression {n m : ℕ} (A : Mat n) (Q : Rect n m) : Mat m :=
  Q.conjTranspose * A * Q

/-- Mathlib sorts self-adjoint eigenvalues in decreasing order; `Fin.rev`
reverses that order. The genuine spectral theorem retains all multiplicities. -/
def orderedEigenvalues {m : ℕ} (M : Mat m) (hM : M.IsHermitian) : Fin m → ℝ :=
  fun r => (Matrix.isSymmetric_toEuclideanLin_iff.mpr hM).eigenvalues
    finrank_euclideanSpace_fin r.rev

/-- The matching actual orthonormal eigenbasis, with the same reversed indexing. -/
def orderedEigenbasis {m : ℕ} (M : Mat m) (hM : M.IsHermitian) :
    OrthonormalBasis (Fin m) ℝ (Vec m) :=
  ((Matrix.isSymmetric_toEuclideanLin_iff.mpr hM).eigenvectorBasis
    finrank_euclideanSpace_fin).reindex Fin.revPerm

/-- Total zero-based indexing. The target's index bounds guarantee the first
branch; a separate index contract makes that fact explicit. -/
def eigenvalueAt {m : ℕ} (M : Mat m) (hM : M.IsHermitian) (i : ℕ) : ℝ :=
  if h : i < m then orderedEigenvalues M hM ⟨i, h⟩ else 0

/-- Only real symmetry is required to obtain the genuine compression spectrum.
The imported elementary Hermitian-congruence lemma supplies its symmetry. -/
def ritzValues {n m : ℕ} (A : Mat n) (hA : A.IsHermitian) (Q : Rect n m) :
    Fin m → ℝ :=
  orderedEigenvalues (compression A Q) (Matrix.isHermitian_conjTranspose_mul_mul Q hA)

def ritzValueAt {n m : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (Q : Rect n m) (i : ℕ) : ℝ :=
  eigenvalueAt (compression A Q) (Matrix.isHermitian_conjTranspose_mul_mul Q hA) i

def monicQuadratic (a b : ℝ) : Polynomial ℝ :=
  (Polynomial.X - Polynomial.C a) * (Polynomial.X - Polynomial.C b)

def quadraticMatrix {m : ℕ} (M : Mat m) (a b : ℝ) : Mat m :=
  (M - a • (1 : Mat m)) * (M - b • (1 : Mat m))

/-- Q q(Q^T A Q) Q^T is q of the compression on its subspace, extended by zero.
It is not q(Q Q^T A Q Q^T) on the whole ambient space. -/
def compressedQuadratic {n m : ℕ} (A : Mat n) (Q : Rect n m) (a b : ℝ) : Mat n :=
  Q * quadraticMatrix (compression A Q) a b * Q.conjTranspose

def form {m : ℕ} (M : Mat m) (x : Vec m) : ℝ :=
  inner ℝ x (act M x)

/-- The complete occupancy assertion through s, for all permitted k,j,i and
independently chosen orthonormal bases. The natural i is one-based as in the source. -/
def IterationOccupancy {n p : ℕ} (A : Mat n) (hA : A.IsHermitian)
    (V : Rect n p) (s : ℕ) : Prop :=
  ∀ k j : ℕ, 1 ≤ k → k < j → j ≤ s →
    ∀ (Qk : Rect n (k * p)) (Qj : Rect n (j * p)),
      IsKrylovBasis A V k Qk → IsKrylovBasis A V j Qj →
      ∀ i : ℕ, 1 ≤ i → i ≤ (k - 1) * p →
        ∃ r : Fin (j * p),
          ritzValueAt A hA Qk (i - 1) < ritzValues A hA Qj r ∧
          ritzValues A hA Qj r < ritzValueAt A hA Qk (i + p - 1)

/-- The proof establishes this stronger arbitrary-full-prefix formulation. -/
def FullPrefixBlockLanczosClaim : Prop :=
  ∀ (n p : ℕ) (A : Mat n) (hA : A.IsHermitian) (V : Rect n p),
    FullColumnRank V → ∀ s, FullBlockDimension A V s → IterationOccupancy A hA V s

/-- The complete original claim with the canonical largest-full-iteration convention. -/
def BlockLanczosConjecture : Prop :=
  ∀ (n p : ℕ) (A : Mat n) (hA : A.IsHermitian) (V : Rect n p),
    FullColumnRank V → ∀ s, LastFullBlockIteration A V s → IterationOccupancy A hA V s

end NLA.KE04
