/-
NR-03 modular bounded development draft.

This file is a mechanically separated portion of the source candidate at
commit d8b65ab13ee9c27e8909052de792f10322a51e1b. It preserves the approved
Definitions/Challenge boundary. This scratch package is not a verification
claim; authoritative LeanCert, Comparator, kernel and sandbox checks remain
pending.
-/
import NLA.NR03.Encoding
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

def coreMask (k : Fin 64) : Mask7 :=
  ⟨k.val, by omega⟩

def singletonMask (i : Fin 7) : Mask7 :=
  ⟨(2 ^ i.val) % 128, Nat.mod_lt _ (by decide)⟩

def pairMasks : Array Nat :=
  #[3, 5, 9, 17, 33, 65, 6, 10, 18, 34, 66, 12, 20, 36, 68, 24, 40, 72,
    48, 80, 96]

def fourMasks : Array Nat :=
  #[15, 23, 39, 71, 27, 43, 75, 51, 83, 99, 29, 45, 77, 53, 85, 101,
    57, 89, 105, 113, 30, 46, 78, 54, 86, 102, 58, 90, 106, 114, 60, 92,
    108, 116, 120]

def pairMask (k : Fin 21) : Mask7 :=
  ⟨pairMasks[k.val]! % 128, Nat.mod_lt _ (by decide)⟩

def fourMask (k : Fin 35) : Mask7 :=
  ⟨fourMasks[k.val]! % 128, Nat.mod_lt _ (by decide)⟩

def maskSubset (s a : Mask7) : Prop :=
  ∀ i : Fin 7, maskVector s i = true → maskVector a i = true

instance : DecidableRel maskSubset := by
  intro s a
  unfold maskSubset
  infer_instance

def hFour (t : ℕ) : ℕ := t - 2

abbrev AtomIndex := Fin (64 + 7 + 21 + 35)

def coreIndex (k : Fin 64) : AtomIndex :=
  Fin.castAdd 35 (Fin.castAdd 21 (Fin.castAdd 7 k))

def singletonIndex (k : Fin 7) : AtomIndex :=
  Fin.castAdd 35 (Fin.castAdd 21 (Fin.natAdd 64 k))

def pairIndex (k : Fin 21) : AtomIndex :=
  Fin.castAdd 35 (Fin.natAdd (64 + 7) k)

def fourIndex (k : Fin 35) : AtomIndex :=
  Fin.natAdd (64 + 7 + 21) k

def coreW (a : Mask7) (k : Fin 64) : ℕ :=
  if a = coreMask k ∨ a = maskComplement (coreMask k) then 1 else 0

def coreV (k : Fin 64) (b : Mask7) : ℕ :=
  natSquareOneMinus (maskDot (coreMask k) b) *
    natSquareOneMinus (maskDot (maskComplement (coreMask k)) b)

def singletonW (a : Mask7) (i : Fin 7) : ℕ :=
  if maskBit a i = false then 1 else 0

def singletonV (i : Fin 7) (b : Mask7) : ℕ :=
  if b = singletonMask i then 1 else 0

def pairW (a : Mask7) (k : Fin 21) : ℕ :=
  if maskSubset (pairMask k) a then 1 else 0

def pairV (k : Fin 21) (b : Mask7) : ℕ :=
  if maskSubset (pairMask k) b then 4 * (maskCard b - 2) else 0

def fourW (a : Mask7) (k : Fin 35) : ℕ :=
  hFour (maskDot (fourMask k) a)

def fourV (k : Fin 35) (b : Mask7) : ℕ :=
  if maskSubset (fourMask k) b then 12 else 0

def sourceW (a : Mask7) (k : AtomIndex) : ℕ :=
  if hk : k.val < 64 then
    coreW a ⟨k.val, hk⟩
  else if hk : k.val < 71 then
    singletonW a ⟨k.val - 64, by omega⟩
  else if hk : k.val < 92 then
    pairW a ⟨k.val - 71, by omega⟩
  else
    fourW a ⟨k.val - 92, by omega⟩

def sourceV (k : AtomIndex) (b : Mask7) : ℕ :=
  if hk : k.val < 64 then
    coreV ⟨k.val, hk⟩ b
  else if hk : k.val < 71 then
    singletonV ⟨k.val - 64, by omega⟩ b
  else if hk : k.val < 92 then
    pairV ⟨k.val - 71, by omega⟩ b
  else
    fourV ⟨k.val - 92, by omega⟩ b

def sourceD (b : Mask7) : ℕ :=
  if maskCard b ≤ 1 then 1 else (maskCard b - 1) ^ 2

def coreSum (a b : Mask7) : ℕ :=
  ∑ k : Fin 64, coreW a k * coreV k b

def singletonSum (a b : Mask7) : ℕ :=
  ∑ k : Fin 7, singletonW a k * singletonV k b

def pairSum (a b : Mask7) : ℕ :=
  ∑ k : Fin 21, pairW a k * pairV k b

def fourSum (a b : Mask7) : ℕ :=
  ∑ k : Fin 35, fourW a k * fourV k b

def fullSum (a b : Mask7) : ℕ :=
  ∑ k : AtomIndex, sourceW a k * sourceV k b

def coreClosed (a b : Mask7) : ℕ :=
  natSquareOneMinus (maskDot a b) *
    natSquareOneMinus (maskCard b - maskDot a b)

def singletonClosed (a b : Mask7) : ℕ :=
  if maskCard b = 1 then 1 - maskDot a b else 0

def pairClosed (a b : Mask7) : ℕ :=
  4 * (maskCard b - 2) * Nat.choose (maskDot a b) 2

def fourClosed (a b : Mask7) : ℕ :=
  12 * ((maskCard b - maskDot a b) * Nat.choose (maskDot a b) 3 +
    2 * Nat.choose (maskDot a b) 4)

end NLA.NR03
