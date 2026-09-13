/-
NR-03 modular bounded development draft.

This file is a mechanically separated portion of the source candidate at
commit d8b65ab13ee9c27e8909052de792f10322a51e1b. It preserves the approved
Definitions/Challenge boundary. This scratch package is not a verification
claim; authoritative LeanCert, Comparator, kernel and sandbox checks remain
pending.
-/
import NLA.NR03.Core
import NLA.NR03.RowCertificate.Four.Block15
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open scoped BigOperators Matrix
noncomputable section

namespace NLA.NR03

/- Each remaining source family is explicitly finite.  The singleton, pair,
   and four-set identities inspect only 7, 21, or 35 summands per row-local
   check; the closed-family identity below is reduced further to its two
   cardinality parameters.  The large 128-by-127 matrix multiplication is
   never unfolded. -/
theorem singleton_identity : ∀ a b : Mask7,
    singletonSum a b = singletonClosed a b := by
  intro a
  fin_cases a
  · exact RowCertificate.Singleton.row0
  · exact RowCertificate.Singleton.row1
  · exact RowCertificate.Singleton.row2
  · exact RowCertificate.Singleton.row3
  · exact RowCertificate.Singleton.row4
  · exact RowCertificate.Singleton.row5
  · exact RowCertificate.Singleton.row6
  · exact RowCertificate.Singleton.row7
  · exact RowCertificate.Singleton.row8
  · exact RowCertificate.Singleton.row9
  · exact RowCertificate.Singleton.row10
  · exact RowCertificate.Singleton.row11
  · exact RowCertificate.Singleton.row12
  · exact RowCertificate.Singleton.row13
  · exact RowCertificate.Singleton.row14
  · exact RowCertificate.Singleton.row15
  · exact RowCertificate.Singleton.row16
  · exact RowCertificate.Singleton.row17
  · exact RowCertificate.Singleton.row18
  · exact RowCertificate.Singleton.row19
  · exact RowCertificate.Singleton.row20
  · exact RowCertificate.Singleton.row21
  · exact RowCertificate.Singleton.row22
  · exact RowCertificate.Singleton.row23
  · exact RowCertificate.Singleton.row24
  · exact RowCertificate.Singleton.row25
  · exact RowCertificate.Singleton.row26
  · exact RowCertificate.Singleton.row27
  · exact RowCertificate.Singleton.row28
  · exact RowCertificate.Singleton.row29
  · exact RowCertificate.Singleton.row30
  · exact RowCertificate.Singleton.row31
  · exact RowCertificate.Singleton.row32
  · exact RowCertificate.Singleton.row33
  · exact RowCertificate.Singleton.row34
  · exact RowCertificate.Singleton.row35
  · exact RowCertificate.Singleton.row36
  · exact RowCertificate.Singleton.row37
  · exact RowCertificate.Singleton.row38
  · exact RowCertificate.Singleton.row39
  · exact RowCertificate.Singleton.row40
  · exact RowCertificate.Singleton.row41
  · exact RowCertificate.Singleton.row42
  · exact RowCertificate.Singleton.row43
  · exact RowCertificate.Singleton.row44
  · exact RowCertificate.Singleton.row45
  · exact RowCertificate.Singleton.row46
  · exact RowCertificate.Singleton.row47
  · exact RowCertificate.Singleton.row48
  · exact RowCertificate.Singleton.row49
  · exact RowCertificate.Singleton.row50
  · exact RowCertificate.Singleton.row51
  · exact RowCertificate.Singleton.row52
  · exact RowCertificate.Singleton.row53
  · exact RowCertificate.Singleton.row54
  · exact RowCertificate.Singleton.row55
  · exact RowCertificate.Singleton.row56
  · exact RowCertificate.Singleton.row57
  · exact RowCertificate.Singleton.row58
  · exact RowCertificate.Singleton.row59
  · exact RowCertificate.Singleton.row60
  · exact RowCertificate.Singleton.row61
  · exact RowCertificate.Singleton.row62
  · exact RowCertificate.Singleton.row63
  · exact RowCertificate.Singleton.row64
  · exact RowCertificate.Singleton.row65
  · exact RowCertificate.Singleton.row66
  · exact RowCertificate.Singleton.row67
  · exact RowCertificate.Singleton.row68
  · exact RowCertificate.Singleton.row69
  · exact RowCertificate.Singleton.row70
  · exact RowCertificate.Singleton.row71
  · exact RowCertificate.Singleton.row72
  · exact RowCertificate.Singleton.row73
  · exact RowCertificate.Singleton.row74
  · exact RowCertificate.Singleton.row75
  · exact RowCertificate.Singleton.row76
  · exact RowCertificate.Singleton.row77
  · exact RowCertificate.Singleton.row78
  · exact RowCertificate.Singleton.row79
  · exact RowCertificate.Singleton.row80
  · exact RowCertificate.Singleton.row81
  · exact RowCertificate.Singleton.row82
  · exact RowCertificate.Singleton.row83
  · exact RowCertificate.Singleton.row84
  · exact RowCertificate.Singleton.row85
  · exact RowCertificate.Singleton.row86
  · exact RowCertificate.Singleton.row87
  · exact RowCertificate.Singleton.row88
  · exact RowCertificate.Singleton.row89
  · exact RowCertificate.Singleton.row90
  · exact RowCertificate.Singleton.row91
  · exact RowCertificate.Singleton.row92
  · exact RowCertificate.Singleton.row93
  · exact RowCertificate.Singleton.row94
  · exact RowCertificate.Singleton.row95
  · exact RowCertificate.Singleton.row96
  · exact RowCertificate.Singleton.row97
  · exact RowCertificate.Singleton.row98
  · exact RowCertificate.Singleton.row99
  · exact RowCertificate.Singleton.row100
  · exact RowCertificate.Singleton.row101
  · exact RowCertificate.Singleton.row102
  · exact RowCertificate.Singleton.row103
  · exact RowCertificate.Singleton.row104
  · exact RowCertificate.Singleton.row105
  · exact RowCertificate.Singleton.row106
  · exact RowCertificate.Singleton.row107
  · exact RowCertificate.Singleton.row108
  · exact RowCertificate.Singleton.row109
  · exact RowCertificate.Singleton.row110
  · exact RowCertificate.Singleton.row111
  · exact RowCertificate.Singleton.row112
  · exact RowCertificate.Singleton.row113
  · exact RowCertificate.Singleton.row114
  · exact RowCertificate.Singleton.row115
  · exact RowCertificate.Singleton.row116
  · exact RowCertificate.Singleton.row117
  · exact RowCertificate.Singleton.row118
  · exact RowCertificate.Singleton.row119
  · exact RowCertificate.Singleton.row120
  · exact RowCertificate.Singleton.row121
  · exact RowCertificate.Singleton.row122
  · exact RowCertificate.Singleton.row123
  · exact RowCertificate.Singleton.row124
  · exact RowCertificate.Singleton.row125
  · exact RowCertificate.Singleton.row126
  · exact RowCertificate.Singleton.row127

#print axioms NLA.NR03.singleton_identity

theorem pair_identity : ∀ a b : Mask7,
    pairSum a b = pairClosed a b := by
  intro a
  fin_cases a
  · exact RowCertificate.Pair.row0
  · exact RowCertificate.Pair.row1
  · exact RowCertificate.Pair.row2
  · exact RowCertificate.Pair.row3
  · exact RowCertificate.Pair.row4
  · exact RowCertificate.Pair.row5
  · exact RowCertificate.Pair.row6
  · exact RowCertificate.Pair.row7
  · exact RowCertificate.Pair.row8
  · exact RowCertificate.Pair.row9
  · exact RowCertificate.Pair.row10
  · exact RowCertificate.Pair.row11
  · exact RowCertificate.Pair.row12
  · exact RowCertificate.Pair.row13
  · exact RowCertificate.Pair.row14
  · exact RowCertificate.Pair.row15
  · exact RowCertificate.Pair.row16
  · exact RowCertificate.Pair.row17
  · exact RowCertificate.Pair.row18
  · exact RowCertificate.Pair.row19
  · exact RowCertificate.Pair.row20
  · exact RowCertificate.Pair.row21
  · exact RowCertificate.Pair.row22
  · exact RowCertificate.Pair.row23
  · exact RowCertificate.Pair.row24
  · exact RowCertificate.Pair.row25
  · exact RowCertificate.Pair.row26
  · exact RowCertificate.Pair.row27
  · exact RowCertificate.Pair.row28
  · exact RowCertificate.Pair.row29
  · exact RowCertificate.Pair.row30
  · exact RowCertificate.Pair.row31
  · exact RowCertificate.Pair.row32
  · exact RowCertificate.Pair.row33
  · exact RowCertificate.Pair.row34
  · exact RowCertificate.Pair.row35
  · exact RowCertificate.Pair.row36
  · exact RowCertificate.Pair.row37
  · exact RowCertificate.Pair.row38
  · exact RowCertificate.Pair.row39
  · exact RowCertificate.Pair.row40
  · exact RowCertificate.Pair.row41
  · exact RowCertificate.Pair.row42
  · exact RowCertificate.Pair.row43
  · exact RowCertificate.Pair.row44
  · exact RowCertificate.Pair.row45
  · exact RowCertificate.Pair.row46
  · exact RowCertificate.Pair.row47
  · exact RowCertificate.Pair.row48
  · exact RowCertificate.Pair.row49
  · exact RowCertificate.Pair.row50
  · exact RowCertificate.Pair.row51
  · exact RowCertificate.Pair.row52
  · exact RowCertificate.Pair.row53
  · exact RowCertificate.Pair.row54
  · exact RowCertificate.Pair.row55
  · exact RowCertificate.Pair.row56
  · exact RowCertificate.Pair.row57
  · exact RowCertificate.Pair.row58
  · exact RowCertificate.Pair.row59
  · exact RowCertificate.Pair.row60
  · exact RowCertificate.Pair.row61
  · exact RowCertificate.Pair.row62
  · exact RowCertificate.Pair.row63
  · exact RowCertificate.Pair.row64
  · exact RowCertificate.Pair.row65
  · exact RowCertificate.Pair.row66
  · exact RowCertificate.Pair.row67
  · exact RowCertificate.Pair.row68
  · exact RowCertificate.Pair.row69
  · exact RowCertificate.Pair.row70
  · exact RowCertificate.Pair.row71
  · exact RowCertificate.Pair.row72
  · exact RowCertificate.Pair.row73
  · exact RowCertificate.Pair.row74
  · exact RowCertificate.Pair.row75
  · exact RowCertificate.Pair.row76
  · exact RowCertificate.Pair.row77
  · exact RowCertificate.Pair.row78
  · exact RowCertificate.Pair.row79
  · exact RowCertificate.Pair.row80
  · exact RowCertificate.Pair.row81
  · exact RowCertificate.Pair.row82
  · exact RowCertificate.Pair.row83
  · exact RowCertificate.Pair.row84
  · exact RowCertificate.Pair.row85
  · exact RowCertificate.Pair.row86
  · exact RowCertificate.Pair.row87
  · exact RowCertificate.Pair.row88
  · exact RowCertificate.Pair.row89
  · exact RowCertificate.Pair.row90
  · exact RowCertificate.Pair.row91
  · exact RowCertificate.Pair.row92
  · exact RowCertificate.Pair.row93
  · exact RowCertificate.Pair.row94
  · exact RowCertificate.Pair.row95
  · exact RowCertificate.Pair.row96
  · exact RowCertificate.Pair.row97
  · exact RowCertificate.Pair.row98
  · exact RowCertificate.Pair.row99
  · exact RowCertificate.Pair.row100
  · exact RowCertificate.Pair.row101
  · exact RowCertificate.Pair.row102
  · exact RowCertificate.Pair.row103
  · exact RowCertificate.Pair.row104
  · exact RowCertificate.Pair.row105
  · exact RowCertificate.Pair.row106
  · exact RowCertificate.Pair.row107
  · exact RowCertificate.Pair.row108
  · exact RowCertificate.Pair.row109
  · exact RowCertificate.Pair.row110
  · exact RowCertificate.Pair.row111
  · exact RowCertificate.Pair.row112
  · exact RowCertificate.Pair.row113
  · exact RowCertificate.Pair.row114
  · exact RowCertificate.Pair.row115
  · exact RowCertificate.Pair.row116
  · exact RowCertificate.Pair.row117
  · exact RowCertificate.Pair.row118
  · exact RowCertificate.Pair.row119
  · exact RowCertificate.Pair.row120
  · exact RowCertificate.Pair.row121
  · exact RowCertificate.Pair.row122
  · exact RowCertificate.Pair.row123
  · exact RowCertificate.Pair.row124
  · exact RowCertificate.Pair.row125
  · exact RowCertificate.Pair.row126
  · exact RowCertificate.Pair.row127

#print axioms NLA.NR03.pair_identity

theorem four_identity : ∀ a b : Mask7,
    fourSum a b = fourClosed a b := by
  intro a
  fin_cases a
  · exact RowCertificate.Four.row0
  · exact RowCertificate.Four.row1
  · exact RowCertificate.Four.row2
  · exact RowCertificate.Four.row3
  · exact RowCertificate.Four.row4
  · exact RowCertificate.Four.row5
  · exact RowCertificate.Four.row6
  · exact RowCertificate.Four.row7
  · exact RowCertificate.Four.row8
  · exact RowCertificate.Four.row9
  · exact RowCertificate.Four.row10
  · exact RowCertificate.Four.row11
  · exact RowCertificate.Four.row12
  · exact RowCertificate.Four.row13
  · exact RowCertificate.Four.row14
  · exact RowCertificate.Four.row15
  · exact RowCertificate.Four.row16
  · exact RowCertificate.Four.row17
  · exact RowCertificate.Four.row18
  · exact RowCertificate.Four.row19
  · exact RowCertificate.Four.row20
  · exact RowCertificate.Four.row21
  · exact RowCertificate.Four.row22
  · exact RowCertificate.Four.row23
  · exact RowCertificate.Four.row24
  · exact RowCertificate.Four.row25
  · exact RowCertificate.Four.row26
  · exact RowCertificate.Four.row27
  · exact RowCertificate.Four.row28
  · exact RowCertificate.Four.row29
  · exact RowCertificate.Four.row30
  · exact RowCertificate.Four.row31
  · exact RowCertificate.Four.row32
  · exact RowCertificate.Four.row33
  · exact RowCertificate.Four.row34
  · exact RowCertificate.Four.row35
  · exact RowCertificate.Four.row36
  · exact RowCertificate.Four.row37
  · exact RowCertificate.Four.row38
  · exact RowCertificate.Four.row39
  · exact RowCertificate.Four.row40
  · exact RowCertificate.Four.row41
  · exact RowCertificate.Four.row42
  · exact RowCertificate.Four.row43
  · exact RowCertificate.Four.row44
  · exact RowCertificate.Four.row45
  · exact RowCertificate.Four.row46
  · exact RowCertificate.Four.row47
  · exact RowCertificate.Four.row48
  · exact RowCertificate.Four.row49
  · exact RowCertificate.Four.row50
  · exact RowCertificate.Four.row51
  · exact RowCertificate.Four.row52
  · exact RowCertificate.Four.row53
  · exact RowCertificate.Four.row54
  · exact RowCertificate.Four.row55
  · exact RowCertificate.Four.row56
  · exact RowCertificate.Four.row57
  · exact RowCertificate.Four.row58
  · exact RowCertificate.Four.row59
  · exact RowCertificate.Four.row60
  · exact RowCertificate.Four.row61
  · exact RowCertificate.Four.row62
  · exact RowCertificate.Four.row63
  · exact RowCertificate.Four.row64
  · exact RowCertificate.Four.row65
  · exact RowCertificate.Four.row66
  · exact RowCertificate.Four.row67
  · exact RowCertificate.Four.row68
  · exact RowCertificate.Four.row69
  · exact RowCertificate.Four.row70
  · exact RowCertificate.Four.row71
  · exact RowCertificate.Four.row72
  · exact RowCertificate.Four.row73
  · exact RowCertificate.Four.row74
  · exact RowCertificate.Four.row75
  · exact RowCertificate.Four.row76
  · exact RowCertificate.Four.row77
  · exact RowCertificate.Four.row78
  · exact RowCertificate.Four.row79
  · exact RowCertificate.Four.row80
  · exact RowCertificate.Four.row81
  · exact RowCertificate.Four.row82
  · exact RowCertificate.Four.row83
  · exact RowCertificate.Four.row84
  · exact RowCertificate.Four.row85
  · exact RowCertificate.Four.row86
  · exact RowCertificate.Four.row87
  · exact RowCertificate.Four.row88
  · exact RowCertificate.Four.row89
  · exact RowCertificate.Four.row90
  · exact RowCertificate.Four.row91
  · exact RowCertificate.Four.row92
  · exact RowCertificate.Four.row93
  · exact RowCertificate.Four.row94
  · exact RowCertificate.Four.row95
  · exact RowCertificate.Four.row96
  · exact RowCertificate.Four.row97
  · exact RowCertificate.Four.row98
  · exact RowCertificate.Four.row99
  · exact RowCertificate.Four.row100
  · exact RowCertificate.Four.row101
  · exact RowCertificate.Four.row102
  · exact RowCertificate.Four.row103
  · exact RowCertificate.Four.row104
  · exact RowCertificate.Four.row105
  · exact RowCertificate.Four.row106
  · exact RowCertificate.Four.row107
  · exact RowCertificate.Four.row108
  · exact RowCertificate.Four.row109
  · exact RowCertificate.Four.row110
  · exact RowCertificate.Four.row111
  · exact RowCertificate.Four.row112
  · exact RowCertificate.Four.row113
  · exact RowCertificate.Four.row114
  · exact RowCertificate.Four.row115
  · exact RowCertificate.Four.row116
  · exact RowCertificate.Four.row117
  · exact RowCertificate.Four.row118
  · exact RowCertificate.Four.row119
  · exact RowCertificate.Four.row120
  · exact RowCertificate.Four.row121
  · exact RowCertificate.Four.row122
  · exact RowCertificate.Four.row123
  · exact RowCertificate.Four.row124
  · exact RowCertificate.Four.row125
  · exact RowCertificate.Four.row126
  · exact RowCertificate.Four.row127

#print axioms NLA.NR03.four_identity

theorem natBool_le_one (b : Bool) : natBool b ≤ 1 := by
  cases b <;> simp [natBool]

theorem maskCard_le_seven (b : Mask7) : maskCard b ≤ 7 := by
  unfold maskCard
  calc
    (∑ i : Fin 7, natBool (maskVector b i)) ≤ ∑ i : Fin 7, 1 := by
      apply Finset.sum_le_sum
      intro i hi
      exact natBool_le_one _
    _ = 7 := by simp

theorem maskDot_le_card (a b : Mask7) :
    maskDot a b ≤ maskCard b := by
  unfold maskDot maskCard
  apply Finset.sum_le_sum
  intro i hi
  cases ha : maskVector a i <;> cases hb : maskVector b i <;>
    simp [natBool, ha, hb]

/- The closed family calculation depends only on the two cardinality
   parameters s = |b| and t = |a ∩ b|.  It is checked over Fin 8 squared
   (with the implication t ≤ s), rather than by expanding all 128^2 mask
   pairs. -/
theorem closed_arithmetic :
    ∀ s t : Fin 8, t.val ≤ s.val →
      natSquareOneMinus t.val * natSquareOneMinus (s.val - t.val) +
          (if s.val = 1 then 1 - t.val else 0) +
          4 * (s.val - 2) * Nat.choose t.val 2 +
          12 * ((s.val - t.val) * Nat.choose t.val 3 +
            2 * Nat.choose t.val 4) =
        (if s.val ≤ 1 then 1 else (s.val - 1) ^ 2) *
          natSquareOneMinus t.val := by
  decide +kernel

theorem closed_family_identity : ∀ a b : Mask7,
    coreClosed a b + singletonClosed a b + pairClosed a b + fourClosed a b =
      sourceD b * natTarget a b := by
  intro a b
  have hs : maskCard b ≤ 7 := maskCard_le_seven b
  have ht : maskDot a b ≤ maskCard b := maskDot_le_card a b
  let s : Fin 8 := ⟨maskCard b, by omega⟩
  let t : Fin 8 := ⟨maskDot a b, by omega⟩
  have hst : t.val ≤ s.val := by
    simpa [s, t] using ht
  have h := closed_arithmetic s t hst
  simpa [coreClosed, singletonClosed, pairClosed, fourClosed,
    sourceD, natTarget, s, t] using h

end NLA.NR03
