import NLA.IS02.Definitions

set_option autoImplicit false
namespace NLA.IS02

/-!
Statement boundary only. These declarations intentionally contain no proof
and are never imported by Solution.lean. They retain the full canonical
counterexample: exact stochastic constraints, characteristic-polynomial
spectrum with multiplicities, uniqueness up to permutation, and exclusion
from the vertex-segment locus.
-/

theorem counterexample_symmetric_nonnegative_stochastic :
    counterexample ∈ symmetricStochastic 4 := by
  sorry

theorem counterexample_trace :
    trace counterexample = 1 := by
  sorry

theorem counterexample_positive_trace :
    0 < trace counterexample := by
  sorry

theorem counterexample_spectrum :
    sameSpectrum counterexample
      (!![(1 : ℝ), 0, 0, 0;
          0, 1, 0, 0;
          0, 0, 0, 0;
          0, 0, 0, (-1 : ℝ)]) := by
  sorry

theorem sameSpectrum_iff_realEigenvalueMultiset_eq {n : ℕ}
    {A B : Mat n} (hA : symmetric A) (hB : symmetric B) :
    sameSpectrum A B ↔ realEigenvalueMultiset A = realEigenvalueMultiset B := by
  sorry

theorem counterexample_spectral_uniqueness :
    spectrallyUnique counterexample := by
  sorry

theorem counterexample_outside_locus :
    counterexample ∉ assertedLocus 4 := by
  sorry

theorem counterexample_claim : counterexampleClaim := by
  sorry

theorem not_targetNecessaryCondition : ¬ targetNecessaryCondition := by
  sorry

end NLA.IS02
