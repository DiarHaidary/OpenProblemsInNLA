import Solution
set_option autoImplicit false
namespace NLA.IS02.RefereeBoundary
open NLA.IS02
example :
    counterexample ∈ symmetricStochastic 4 := by
  exact NLA.IS02.counterexample_symmetric_nonnegative_stochastic

example :
    trace counterexample = 1 := by
  exact NLA.IS02.counterexample_trace

example :
    0 < trace counterexample := by
  exact NLA.IS02.counterexample_positive_trace

example :
    sameSpectrum counterexample
      (!![(1 : ℝ), 0, 0, 0;
          0, 1, 0, 0;
          0, 0, 0, 0;
          0, 0, 0, (-1 : ℝ)]) := by
  exact NLA.IS02.counterexample_spectrum

example {n : ℕ}
    {A B : Mat n} (hA : symmetric A) (hB : symmetric B) :
    sameSpectrum A B ↔ realEigenvalueMultiset A = realEigenvalueMultiset B := by
  exact NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq hA hB

example :
    spectrallyUnique counterexample := by
  exact NLA.IS02.counterexample_spectral_uniqueness

example :
    counterexample ∉ assertedLocus 4 := by
  exact NLA.IS02.counterexample_outside_locus

example : counterexampleClaim := by
  exact NLA.IS02.counterexample_claim

example : ¬ targetNecessaryCondition := by
  exact NLA.IS02.not_targetNecessaryCondition

end NLA.IS02.RefereeBoundary
