import NLA.IE05.Definitions

noncomputable section

open NLA.IE05

namespace Referee1Expected

def type_0 : Prop :=
    ∀ {n : ℕ} (hn : 1 ≤ n) (A : Mat n),
    0 ≤ entryMax A ∧ (∀ i j, |A i j| ≤ entryMax A) ∧
      ∃ i j, entryMax A = |A i j|


def type_1 : Prop :=
    ∀ {n : ℕ} (S : Mat n) (k p : Fin n)
    (hp : AdmissiblePivot S k p),
    activeMax (schurStep S k p) (k.val + 1) ≤ 2 * activeMax S k.val


def type_2 : Prop :=
    ∀ {n : ℕ} (hn : 1 ≤ n) (A : Mat n)
    (path : PivotPath n) (hp : AdmissiblePath A path),
    0 < entryMax A ∧ 1 ≤ growth A path ∧ growth A path ≤ (2 : ℝ) ^ (n - 1)


def type_3 : Prop :=
    ∀ {n : ℕ} (A : Mat n) (hA : A.det ≠ 0),
    FirstAvailablePath A (firstPath A) ∧
      (∀ k, trajectory A (firstPath A) k = firstTrajectory A k) ∧
      ∀ path, FirstAvailablePath A path → path = firstPath A


def type_4 : Prop :=
    ∀ (n : ℕ) (hn : 2 ≤ n),
    (orthogonalGrowthSet n).Nonempty ∧ BddAbove (orthogonalGrowthSet n) ∧
      ∀ r ∈ orthogonalGrowthSet n, 1 ≤ r ∧ r ≤ (2 : ℝ) ^ (n - 1)


def type_5 : Prop :=
    ∀ (n : ℕ) (hn : 2 ≤ n),
    PositiveQR (prescribedLower n) (candidateQ n) (candidateR n) ∧
      ∀ Q R, PositiveQR (prescribedLower n) Q R →
        Q = candidateQ n ∧ R = candidateR n


def type_6 : Prop :=
    ∀ {n : ℕ} (H : Mat n) (d : Fin n → ℝ)
    (hd : ∀ j, 0 < d j) (hH : H.transpose * H = Matrix.diagonal d),
    Orthogonal (scaledColumns H d)


def type_7 : Prop :=
    ∀ {n : ℕ} (L T : Mat n) (d : Fin n → ℝ)
    (hL : UnitLower L) (hLb : ∀ i j, j < i → |L i j| ≤ 1)
    (hT : UpperTriangular T) (hTp : ∀ i, 0 < T i i) (hd : ∀ j, 0 < d j),
    FirstAvailablePath (scaledColumns (L * T) d) (noSwapPath n) ∧
      firstPath (scaledColumns (L * T) d) = noSwapPath n ∧
      ∀ k, k ≤ n → trajectory (scaledColumns (L * T) d) (noSwapPath n) k =
        scaledColumns (tailProduct L T k) d


def type_8 : Prop :=
    ∀ b : Bool,
      (integerH b).transpose * integerH b = Matrix.diagonal (integerD b) ∧
      integerH b = integerLower b * integerT b ∧
      UnitLower (integerLower b) ∧ UpperTriangular (integerT b) ∧
      (∀ i j, j < i → |integerLower b i j| ≤ 1) ∧
      (∀ i, 0 < integerT b i i) ∧ (∀ j, 0 < integerD b j)


def type_9 : Prop :=
    (∀ i j : Fin 8, 5272 * (integerH true i j) ^ 2 ≤ 3969 * integerD true j) ∧
    integerD true 7 = 5272 ∧
    integerH false 2 2 = 51 ∧ integerD false 2 = 3286 ∧
    (∀ k i j : Fin 8, k ≤ i → k ≤ j →
      (tailProduct (integerLower false) (integerT false) k.val i j) ^ 2 ≤
        5462 * integerD false j) ∧
    tailProduct (integerLower true) (integerT true) 7 7 7 = 5272


def type_10 : Prop :=
    candidateQ 8 = normalizedInteger false ∧
      firstPath (candidateQ 8) = noSwapPath 8


def type_11 : Prop :=
    Orthogonal witnessQ ∧ firstPath witnessQ = noSwapPath 8 ∧
      FirstAvailablePath witnessQ (noSwapPath 8) ∧
      AdmissiblePath witnessQ (noSwapPath 8)


def type_12 : Prop :=
    entryMax witnessQ ≤ 63 / Real.sqrt 5272 ∧
      (5272 : ℝ) / 63 ≤ firstGrowth witnessQ ∧
      51 / Real.sqrt 3286 ≤ entryMax (candidateQ 8) ∧
      0 ≤ firstGrowth (candidateQ 8) ∧
      (firstGrowth (candidateQ 8)) ^ 2 ≤ (17948132 : ℝ) / 2601


def type_13 : Prop :=
    ((5272 : ℝ) / 63) ^ 2 - (17948132 : ℝ) / 2601 =
      (117335164 : ℝ) / 1147041 ∧
      0 < (117335164 : ℝ) / 1147041


def type_14 : Prop :=
    firstGrowth (candidateQ 8) < firstGrowth witnessQ


def type_15 : Prop :=
    firstGrowth (candidateQ 8) < orthogonalGrowthSup 8


def type_16 : Prop :=
    ¬ OrthogonalExtremizerConjecture


end Referee1Expected
