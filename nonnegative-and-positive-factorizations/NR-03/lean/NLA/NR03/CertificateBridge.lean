/-
NR-03 conditional certificate algebra, isolated for bounded diagnostics.

The interfaces in certificate-bridge/INTERFACES.md were reviewed before these
proof bodies. This module deliberately imports no computed row certificate.
The original unconditional Certificate module supplies every helper premise
from the complete core and family proofs. Development only: canonical gates
remain pending.
-/
import NLA.NR03.Index
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

/- These four original declarations retain their exact names, values, types,
   and positivity proof body; only their module location changes. -/
def genericW : Matrix (BoolVec 7) (Fin 127) ℕ :=
  fun a k => sourceW (maskOfVector a) k

def genericV : Matrix (Fin 127) (BoolVec 7) ℕ :=
  fun k b => sourceV k (maskOfVector b)

def genericD : BoolVec 7 → ℕ :=
  fun b => sourceD (maskOfVector b)

theorem genericD_positive : ∀ b : BoolVec 7, 0 < genericD b := by
  intro b
  unfold genericD sourceD
  split
  · norm_num
  · have hp : 0 < maskCard (maskOfVector b) - 1 := by omega
    exact Nat.pow_pos hp

#check genericW
#check genericV
#check genericD
#print axioms genericD_positive

namespace CertificateBridge

theorem full_sum_decomposition (a b : Mask7) :
    fullSum a b = coreSum a b + singletonSum a b + pairSum a b + fourSum a b := by
  have hc :
      (∑ k : Fin 64, sourceW a (coreIndex k) * sourceV (coreIndex k) b) =
        coreSum a b := by
    change (∑ k : Fin 64, sourceW a (coreIndex k) * sourceV (coreIndex k) b) =
      ∑ k : Fin 64, coreW a k * coreV k b
    apply Finset.sum_congr rfl
    intro k hk
    exact congrArg₂ (fun x y : ℕ => x * y) (sourceW_core a k) (sourceV_core k b)
  have hs :
      (∑ k : Fin 7, sourceW a (singletonIndex k) * sourceV (singletonIndex k) b) =
        singletonSum a b := by
    change (∑ k : Fin 7, sourceW a (singletonIndex k) * sourceV (singletonIndex k) b) =
      ∑ k : Fin 7, singletonW a k * singletonV k b
    apply Finset.sum_congr rfl
    intro k hk
    exact congrArg₂ (fun x y : ℕ => x * y)
      (sourceW_singleton a k) (sourceV_singleton k b)
  have hp :
      (∑ k : Fin 21, sourceW a (pairIndex k) * sourceV (pairIndex k) b) =
        pairSum a b := by
    change (∑ k : Fin 21, sourceW a (pairIndex k) * sourceV (pairIndex k) b) =
      ∑ k : Fin 21, pairW a k * pairV k b
    apply Finset.sum_congr rfl
    intro k hk
    exact congrArg₂ (fun x y : ℕ => x * y) (sourceW_pair a k) (sourceV_pair k b)
  have hf :
      (∑ k : Fin 35, sourceW a (fourIndex k) * sourceV (fourIndex k) b) =
        fourSum a b := by
    change (∑ k : Fin 35, sourceW a (fourIndex k) * sourceV (fourIndex k) b) =
      ∑ k : Fin 35, fourW a k * fourV k b
    apply Finset.sum_congr rfl
    intro k hk
    exact congrArg₂ (fun x y : ℕ => x * y) (sourceW_four a k) (sourceV_four k b)
  change (∑ k : AtomIndex, sourceW a k * sourceV k b) = _
  exact (fin127_sum_split (fun k => sourceW a k * sourceV k b)).trans
    (congrArg₂ (fun x y : ℕ => x + y)
      (congrArg₂ (fun x y : ℕ => x + y)
        (congrArg₂ (fun x y : ℕ => x + y) hc hs) hp) hf)

#print axioms full_sum_decomposition

theorem full_identity_of_components
    (hcore : ∀ a b : Mask7, coreSum a b = coreClosed a b)
    (hsingleton : ∀ a b : Mask7, singletonSum a b = singletonClosed a b)
    (hpair : ∀ a b : Mask7, pairSum a b = pairClosed a b)
    (hfour : ∀ a b : Mask7, fourSum a b = fourClosed a b)
    (hclosed : ∀ a b : Mask7,
      coreClosed a b + singletonClosed a b + pairClosed a b + fourClosed a b =
        sourceD b * natTarget a b) :
    ∀ a b : Mask7, fullSum a b = sourceD b * natTarget a b := by
  intro a b
  exact (full_sum_decomposition a b).trans
    ((congrArg₂ (fun x y : ℕ => x + y)
      (congrArg₂ (fun x y : ℕ => x + y)
        (congrArg₂ (fun x y : ℕ => x + y) (hcore a b) (hsingleton a b))
        (hpair a b)) (hfour a b)).trans (hclosed a b))

#print axioms full_identity_of_components

theorem scaled_identity_of_full
    (hfull : ∀ a b : Mask7, fullSum a b = sourceD b * natTarget a b) :
    ∀ a b : BoolVec 7,
      (castNatMatrix genericW * castNatMatrix genericV) a b =
        (genericD b : ℝ) * cMatrix 7 a b := by
  intro a b
  calc
    (castNatMatrix genericW * castNatMatrix genericV) a b =
        ∑ k : AtomIndex,
          (sourceW (maskOfVector a) k : ℝ) *
            (sourceV k (maskOfVector b) : ℝ) := by
      rw [Matrix.mul_apply]
      rfl
    _ = (fullSum (maskOfVector a) (maskOfVector b) : ℝ) := by
      change (∑ k : AtomIndex,
        (sourceW (maskOfVector a) k : ℝ) * (sourceV k (maskOfVector b) : ℝ)) =
        ((∑ k : AtomIndex,
          sourceW (maskOfVector a) k * sourceV k (maskOfVector b) : ℕ) : ℝ)
      calc
        _ = ∑ k : AtomIndex,
            ((sourceW (maskOfVector a) k * sourceV k (maskOfVector b) : ℕ) : ℝ) := by
          apply Finset.sum_congr rfl
          intro k hk
          exact (Nat.cast_mul _ _).symm
        _ = _ := (Nat.cast_sum Finset.univ (fun k : AtomIndex =>
          sourceW (maskOfVector a) k * sourceV k (maskOfVector b))).symm
    _ = ((sourceD (maskOfVector b) *
          natTarget (maskOfVector a) (maskOfVector b) : ℕ) : ℝ) :=
      congrArg (fun z : ℕ => (z : ℝ)) (hfull (maskOfVector a) (maskOfVector b))
    _ = (sourceD (maskOfVector b) : ℝ) *
          (natTarget (maskOfVector a) (maskOfVector b) : ℝ) :=
      Nat.cast_mul _ _
    _ = (genericD b : ℝ) * cMatrix 7 a b :=
      congrArg (fun z : ℝ => (sourceD (maskOfVector b) : ℝ) * z) (natTarget_cast a b)

#print axioms scaled_identity_of_full

end CertificateBridge
end NLA.NR03
