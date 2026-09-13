/-
NR-03 modular bounded development draft.

This file is a mechanically separated portion of the source candidate at
commit d8b65ab13ee9c27e8909052de792f10322a51e1b. It preserves the approved
Definitions/Challenge boundary. This scratch package is not a verification
claim; authoritative LeanCert, Comparator, kernel and sandbox checks remain
pending.
-/
import NLA.NR03.Definitions
import Init.Data.Nat.Bitwise.Lemmas
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

abbrev Mask7 := Fin 128

def natBool (b : Bool) : ℕ := if b = true then 1 else 0

/- Encode the coordinates recursively from the least significant bit.  The
   recursive presentation avoids enumerating all 2^7 Boolean functions in
   the kernel proof of the mask/vector correspondence. -/
def encodeNat : (n : ℕ) → (Fin n → Bool) → ℕ
  | 0, _ => 0
  | n + 1, a =>
      2 ^ n * natBool (a (Fin.last n)) +
        encodeNat n (fun i => a i.castSucc)

theorem encodeNat_lt_pow : ∀ (n : ℕ) (a : Fin n → Bool),
    encodeNat n a < 2 ^ n := by
  intro n
  induction n with
  | zero =>
      intro a
      simp [encodeNat]
  | succ n ih =>
      intro a
      have ht := ih (fun i => a i.castSucc)
      cases h : a (Fin.last n) <;>
        simp [encodeNat, natBool, h, Nat.pow_succ] at * <;> omega

def maskOfVector (a : BoolVec 7) : Mask7 :=
  ⟨encodeNat 7 a, by
    have h := encodeNat_lt_pow 7 a
    norm_num at h ⊢
    exact h⟩

def maskBit (m : Mask7) (i : Fin 7) : Bool :=
  decide (((m.val / (2 ^ i.val)) % 2) = 1)

def maskVector (m : Mask7) : BoolVec 7 := fun i => maskBit m i

def maskDot (m n : Mask7) : ℕ :=
  ∑ i : Fin 7, natBool (maskVector m i) * natBool (maskVector n i)

def maskCard (m : Mask7) : ℕ :=
  ∑ i : Fin 7, natBool (maskVector m i)

def natSquareOneMinus (t : ℕ) : ℕ :=
  if t ≤ 1 then (1 - t) ^ 2 else (t - 1) ^ 2

def natTarget (m n : Mask7) : ℕ := natSquareOneMinus (maskDot m n)

def maskComplement (m : Mask7) : Mask7 :=
  ⟨127 - m.val, by omega⟩
/- The all-Boolean-vector to mask correspondence is proved before the
   certificate is consumed.  This is intentionally a structural kernel
   proof, not a Python-side indexing assumption or a 128^2 finite table. -/
theorem encodeNat_testBit : ∀ (n : ℕ) (a : Fin n → Bool) (i : Fin n),
    Nat.testBit (encodeNat n a) i.val = a i := by
  intro n
  induction n with
  | zero =>
      intro a i
      exact Fin.elim0 i
  | succ n ih =>
      intro a i
      refine Fin.lastCases ?_ (fun j => ?_) i
      · change Nat.testBit (encodeNat (n + 1) a) n = a (Fin.last n)
        have ht := encodeNat_lt_pow n (fun j => a j.castSucc)
        rw [show encodeNat (n + 1) a =
          2 ^ n * natBool (a (Fin.last n)) +
            encodeNat n (fun j => a j.castSucc) by rfl]
        rw [Nat.testBit_two_pow_mul_add
          (natBool (a (Fin.last n))) ht n]
        cases h : a (Fin.last n) <;> simp [natBool, h]
      · change Nat.testBit (encodeNat (n + 1) a) j.val = a j.castSucc
        have ht := encodeNat_lt_pow n (fun j => a j.castSucc)
        rw [show encodeNat (n + 1) a =
          2 ^ n * natBool (a (Fin.last n)) +
            encodeNat n (fun j => a j.castSucc) by rfl]
        rw [Nat.testBit_two_pow_mul_add
          (natBool (a (Fin.last n))) ht j.val]
        simp [j.isLt, ih]

theorem maskVector_maskOfVector (a : BoolVec 7) :
    maskVector (maskOfVector a) = a := by
  funext i
  change decide (((encodeNat 7 a / (2 ^ i.val)) % 2) = 1) = a i
  rw [← Nat.testBit_eq_decide_div_mod_eq]
  exact encodeNat_testBit 7 a i

theorem maskDot_maskOfVector (a b : BoolVec 7) :
    maskDot (maskOfVector a) (maskOfVector b) =
      ∑ i : Fin 7, natBool (a i) * natBool (b i) := by
  simp [maskDot, maskVector_maskOfVector]

theorem maskCard_maskOfVector (a : BoolVec 7) :
    maskCard (maskOfVector a) = ∑ i : Fin 7, natBool (a i) := by
  simp [maskCard, maskVector_maskOfVector]

theorem natBool_cast (b : Bool) :
    (natBool b : ℝ) = boolToReal b := by
  cases b <;> simp [natBool, boolToReal]

theorem natSquareOneMinus_cast (t : ℕ) :
    (natSquareOneMinus t : ℝ) = (1 - (t : ℝ)) ^ 2 := by
  by_cases ht : t ≤ 1
  · simp [natSquareOneMinus, ht, Nat.cast_sub ht]
  · have ht' : 1 ≤ t := by omega
    simp [natSquareOneMinus, ht, Nat.cast_sub ht']
    ring

theorem natTarget_cast (a b : BoolVec 7) :
    (natTarget (maskOfVector a) (maskOfVector b) : ℝ) =
      cMatrix 7 a b := by
  rw [natTarget, natSquareOneMinus_cast, maskDot_maskOfVector]
  simp only [cMatrix, boolDot, Nat.cast_sum, Nat.cast_mul, natBool_cast]

end NLA.NR03
