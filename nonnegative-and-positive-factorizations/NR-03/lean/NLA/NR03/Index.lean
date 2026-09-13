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

/- The abstract sum splitter keeps the finite family decomposition cheap: it
   is proved once for an arbitrary summand, without unfolding any certificate
   data. -/
theorem fin127_sum_split (f : AtomIndex → ℕ) :
    (∑ k : AtomIndex, f k) =
      (∑ k : Fin 64, f (coreIndex k)) +
        (∑ k : Fin 7, f (singletonIndex k)) +
        (∑ k : Fin 21, f (pairIndex k)) +
        (∑ k : Fin 35, f (fourIndex k)) := by
  have houter := Fin.sum_univ_add f
  have hmid := Fin.sum_univ_add
    (fun k : Fin (64 + 7 + 21) => f (Fin.castAdd 35 k))
  have hinner := Fin.sum_univ_add
    (fun k : Fin (64 + 7) => f (Fin.castAdd 35 (Fin.castAdd 21 k)))
  rw [houter, hmid, hinner]
  rfl

theorem sourceW_core (a : Mask7) (k : Fin 64) :
    sourceW a (coreIndex k) = coreW a k := by
  simp [sourceW, coreIndex, k.isLt]

theorem sourceV_core (k : Fin 64) (b : Mask7) :
    sourceV (coreIndex k) b = coreV k b := by
  simp [sourceV, coreIndex, k.isLt]

theorem sourceW_singleton (a : Mask7) (k : Fin 7) :
    sourceW a (singletonIndex k) = singletonW a k := by
  have hk : k.val < 7 := k.isLt
  have h64 : ¬ (64 + k.val < 64) := by omega
  have h71 : 64 + k.val < 71 := by omega
  simp [sourceW, singletonIndex, h64, h71]

theorem sourceV_singleton (k : Fin 7) (b : Mask7) :
    sourceV (singletonIndex k) b = singletonV k b := by
  have hk : k.val < 7 := k.isLt
  have h64 : ¬ (64 + k.val < 64) := by omega
  have h71 : 64 + k.val < 71 := by omega
  simp [sourceV, singletonIndex, h64, h71]

theorem sourceW_pair (a : Mask7) (k : Fin 21) :
    sourceW a (pairIndex k) = pairW a k := by
  have hk : k.val < 21 := k.isLt
  have h64 : ¬ (71 + k.val < 64) := by omega
  have h71 : ¬ (71 + k.val < 71) := by omega
  have h92 : 71 + k.val < 92 := by omega
  simp [sourceW, pairIndex, h64, h71, h92]

theorem sourceV_pair (k : Fin 21) (b : Mask7) :
    sourceV (pairIndex k) b = pairV k b := by
  have hk : k.val < 21 := k.isLt
  have h64 : ¬ (71 + k.val < 64) := by omega
  have h71 : ¬ (71 + k.val < 71) := by omega
  have h92 : 71 + k.val < 92 := by omega
  simp [sourceV, pairIndex, h64, h71, h92]

theorem sourceW_four (a : Mask7) (k : Fin 35) :
    sourceW a (fourIndex k) = fourW a k := by
  have hk : k.val < 35 := k.isLt
  have h64 : ¬ (92 + k.val < 64) := by omega
  have h71 : ¬ (92 + k.val < 71) := by omega
  have h92 : ¬ (92 + k.val < 92) := by omega
  simp [sourceW, fourIndex, h64, h71, h92]

theorem sourceV_four (k : Fin 35) (b : Mask7) :
    sourceV (fourIndex k) b = fourV k b := by
  have hk : k.val < 35 := k.isLt
  have h64 : ¬ (92 + k.val < 64) := by omega
  have h71 : ¬ (92 + k.val < 71) := by omega
  have h92 : ¬ (92 + k.val < 92) := by omega
  simp [sourceV, fourIndex, h64, h71, h92]

end NLA.NR03
