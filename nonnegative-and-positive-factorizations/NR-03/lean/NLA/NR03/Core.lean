/-
NR-03 modular bounded development draft.

This file is a mechanically separated portion of the source candidate at
commit d8b65ab13ee9c27e8909052de792f10322a51e1b. It preserves the approved
Definitions/Challenge boundary. This scratch package is not a verification
claim; authoritative LeanCert, Comparator, kernel and sandbox checks remain
pending.
-/
import NLA.NR03.FamilyDefs
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

def coreRep (a : Mask7) : Fin 64 :=
  if h : a.val < 64 then ⟨a.val, h⟩ else ⟨127 - a.val, by omega⟩

/- This structural Fin-index argument replaces a 64-term symbolic sum by its
   unique nonzero complementary-pair summand. -/
theorem coreW_indicator (a : Mask7) (k : Fin 64) :
    coreW a k = if k = coreRep a then 1 else 0 := by
  have halt : a.val < 128 := a.isLt
  have hklt : k.val < 64 := k.isLt
  by_cases ha : a.val < 64
  · have hrep : coreRep a = ⟨a.val, ha⟩ := by
      simp [coreRep, ha]
    rw [hrep]
    by_cases h : a = coreMask k
    · have hk : k = ⟨a.val, ha⟩ := by
        apply Fin.ext
        have hv := congrArg (fun z : Mask7 => z.val) h
        simpa [coreMask] using hv.symm
      have hcomp : a ≠ maskComplement (coreMask k) := by
        intro h'
        have hv := congrArg (fun z : Mask7 => z.val) h'
        simp [maskComplement, coreMask] at hv
        omega
      simp only [coreW, if_pos (Or.inl h), if_pos hk]
    · have hk : k ≠ ⟨a.val, ha⟩ := by
        intro hk'
        apply h
        apply Fin.ext
        have hv := congrArg (fun z : Fin 64 => z.val) hk'
        simpa [coreMask] using hv.symm
      have hcomp : a ≠ maskComplement (coreMask k) := by
        intro h'
        have hv := congrArg (fun z : Mask7 => z.val) h'
        simp [maskComplement, coreMask] at hv
        omega
      simp [coreW, h, hcomp, hk]
  · have hrep : coreRep a = ⟨127 - a.val, by omega⟩ := by
      simp [coreRep, ha]
    rw [hrep]
    have hlow : a ≠ coreMask k := by
      intro h'
      have hv := congrArg (fun z : Mask7 => z.val) h'
      simp [coreMask] at hv
      omega
    by_cases h : a = maskComplement (coreMask k)
    · have hk : k = ⟨127 - a.val, by omega⟩ := by
        apply Fin.ext
        have hv := congrArg (fun z : Mask7 => z.val) h
        change a.val = 127 - k.val at hv
        change k.val = 127 - a.val
        omega
      simp only [coreW, if_pos (Or.inr h), if_pos hk]
    · have hk : k ≠ ⟨127 - a.val, by omega⟩ := by
        intro hk'
        apply h
        apply Fin.ext
        have hv := congrArg (fun z : Fin 64 => z.val) hk'
        change k.val = 127 - a.val at hv
        change a.val = 127 - k.val
        omega
      simp [coreW, h, hlow, hk]

/- The complement mask flips each of the seven Boolean coordinates.  This
   finite check has only 128*7 primitive bit cases; it is independent of the
   128-by-128 matrix identities below. -/
theorem maskBit_complement (a : Mask7) (i : Fin 7) :
    maskBit (maskComplement a) i = !(maskBit a i) := by
  revert i a
  decide +kernel

theorem maskDot_complement_add (a b : Mask7) :
    maskDot a b + maskDot (maskComplement a) b = maskCard b := by
  unfold maskDot maskCard
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i hi
  change natBool (maskBit a i) * natBool (maskBit b i) +
      natBool (maskBit (maskComplement a) i) * natBool (maskBit b i) =
        natBool (maskBit b i)
  rw [maskBit_complement]
  cases hA : maskBit a i <;> cases hB : maskBit b i <;>
    simp [natBool, hA, hB]

theorem maskComplement_involutive (a : Mask7) :
    maskComplement (maskComplement a) = a := by
  have ha : a.val < 128 := a.isLt
  apply Fin.ext
  dsimp [maskComplement]
  omega

theorem coreV_at_rep (a b : Mask7) :
    coreV (coreRep a) b = coreClosed a b := by
  have hsum :
      maskDot a b + maskDot (maskComplement a) b = maskCard b :=
    maskDot_complement_add a b
  have hsub :
      maskDot (maskComplement a) b = maskCard b - maskDot a b := by
    omega
  by_cases ha : a.val < 64
  · let k : Fin 64 := ⟨a.val, ha⟩
    have hrep : coreRep a = k := by
      simp [coreRep, ha, k]
    have hcore : coreMask k = a := by
      apply Fin.ext
      rfl
    rw [hrep]
    simp only [coreV, hcore]
    rw [hsub]
    rfl
  · let k : Fin 64 := ⟨127 - a.val, by omega⟩
    have hrep : coreRep a = k := by
      simp [coreRep, ha, k]
    have hcore : coreMask k = maskComplement a := by
      apply Fin.ext
      rfl
    rw [hrep]
    simp only [coreV, hcore, maskComplement_involutive]
    rw [hsub]
    exact Nat.mul_comm _ _

theorem core_identity (a b : Mask7) :
    coreSum a b = coreClosed a b := by
  change (∑ k : Fin 64, coreW a k * coreV k b) = coreClosed a b
  calc
    (∑ k : Fin 64, coreW a k * coreV k b) =
        ∑ k : Fin 64, (if k = coreRep a then 1 else 0) * coreV k b := by
      apply Finset.sum_congr rfl
      intro k hk
      rw [coreW_indicator]
    _ = coreV (coreRep a) b := by simp
    _ = coreClosed a b := coreV_at_rep a b

end NLA.NR03
