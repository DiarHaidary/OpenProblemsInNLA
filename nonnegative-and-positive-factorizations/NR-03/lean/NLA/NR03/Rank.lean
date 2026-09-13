/-
NR-03 modular bounded development draft.

This file is a mechanically separated portion of the source candidate at
commit d8b65ab13ee9c27e8909052de792f10322a51e1b. It preserves the approved
Definitions/Challenge boundary. This scratch package is not a verification
claim; authoritative LeanCert, Comparator, kernel and sandbox checks remain
pending.
-/
import NLA.NR03.Certificate
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

/- General denominator bridge.  The proof explicitly distributes the common
   positive denominator through the finite matrix sum. -/
theorem scaled_certificate_gives_factorization
    {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ) (r : ℕ)
    (h : HasScaledIntegerCertificate X r) :
    ∃ W : Matrix ι (Fin r) ℕ,
      ∃ V : Matrix (Fin r) κ ℕ,
        ∃ d : κ → ℕ,
          (∀ j, 0 < d j) ∧
          (∀ i j,
            (castNatMatrix W * castNatMatrix V) i j =
              (d j : ℝ) * X i j) ∧
          FactorizationData X r (castNatMatrix W)
            (scaledRightFactor V d) := by
  rcases h with ⟨W, V, d, hd, hid⟩
  refine ⟨W, V, d, hd, hid, ?_⟩
  refine ⟨?_, ?_, ?_⟩
  · intro i k
    change (0 : ℝ) ≤ (W i k : ℝ)
    exact_mod_cast (Nat.zero_le (W i k))
  · intro k j
    apply div_nonneg
    · exact_mod_cast (Nat.zero_le (V k j))
    · exact_mod_cast (Nat.zero_le (d j))
  · ext i j
    have hdj : (d j : ℝ) ≠ 0 := by
      exact_mod_cast (Nat.ne_of_gt (hd j))
    calc
      (castNatMatrix W * scaledRightFactor V d) i j =
          (castNatMatrix W * castNatMatrix V) i j / (d j : ℝ) := by
        simp only [Matrix.mul_apply, castNatMatrix, scaledRightFactor,
          div_eq_mul_inv]
        rw [Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro k hk
        ring
      _ = ((d j : ℝ) * X i j) / (d j : ℝ) := by rw [hid i j]
      _ = X i j := by
        apply (div_eq_iff hdj).2
        ring

theorem witness_scaled_certificate :
    HasScaledIntegerCertificate (cMatrix 7) 127 := by
  refine ⟨genericW, genericV, genericD, genericD_positive, ?_⟩
  exact generic_scaled_identity

theorem witness_factorization :
    HasNonnegativeFactorization (cMatrix 7) 127 := by
  rcases scaled_certificate_gives_factorization (cMatrix 7) 127
      witness_scaled_certificate with ⟨W, V, d, hd, hid, hfac⟩
  exact ⟨castNatMatrix W, scaledRightFactor V d, hfac⟩

theorem cMatrix_nonnegative (n : ℕ) :
    EntrywiseNonnegative (cMatrix n) := by
  intro a b
  exact sq_nonneg _

theorem boolVec_seven_card : Fintype.card (BoolVec 7) = 128 := by
  norm_num [BoolVec]

theorem nonnegative_rank_attained_minimal
    {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ)
    (hX : ∃ r : ℕ, HasNonnegativeFactorization X r) :
    HasNonnegativeFactorization X (nonnegativeRank X) ∧
      ∀ r : ℕ, HasNonnegativeFactorization X r →
        nonnegativeRank X ≤ r := by
  classical
  have hspec : HasNonnegativeFactorization X (Nat.find hX) :=
    Nat.find_spec hX
  have hmin : ∀ r : ℕ, HasNonnegativeFactorization X r →
      Nat.find hX ≤ r := fun r hr => Nat.find_min' hX hr
  simpa [nonnegativeRank, hX] using And.intro hspec hmin

theorem rank_le_of_factorization
    {ι κ : Type} [Fintype ι] [Fintype κ]
    (X : Matrix ι κ ℝ) (r : ℕ)
    (h : HasNonnegativeFactorization X r) :
    nonnegativeRank X ≤ r := by
  exact (nonnegative_rank_attained_minimal X ⟨r, h⟩).2 r h

theorem witness_rank_upper_bound :
    nonnegativeRank (cMatrix 7) ≤ 127 := by
  exact rank_le_of_factorization (cMatrix 7) 127 witness_factorization

theorem witness_not_full_rank :
    nonnegativeRank (cMatrix 7) < 2 ^ 7 := by
  have h := witness_rank_upper_bound
  norm_num at h ⊢
  omega

theorem not_targetStatement : ¬ targetStatement := by
  intro h
  have h7 := h 7 (by norm_num)
  have hu := witness_not_full_rank
  norm_num at h7 hu
  omega


end NLA.NR03
