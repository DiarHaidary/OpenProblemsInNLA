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

set_option pp.universes true
set_option pp.explicit true
#check NLA.IS02.counterexample_symmetric_nonnegative_stochastic
#print axioms NLA.IS02.counterexample_symmetric_nonnegative_stochastic
#check NLA.IS02.counterexample_trace
#print axioms NLA.IS02.counterexample_trace
#check NLA.IS02.counterexample_positive_trace
#print axioms NLA.IS02.counterexample_positive_trace
#check NLA.IS02.counterexample_spectrum
#print axioms NLA.IS02.counterexample_spectrum
#check NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq
#print axioms NLA.IS02.sameSpectrum_iff_realEigenvalueMultiset_eq
#check NLA.IS02.counterexample_spectral_uniqueness
#print axioms NLA.IS02.counterexample_spectral_uniqueness
#check NLA.IS02.counterexample_outside_locus
#print axioms NLA.IS02.counterexample_outside_locus
#check NLA.IS02.counterexample_claim
#print axioms NLA.IS02.counterexample_claim
#check NLA.IS02.not_targetNecessaryCondition
#print axioms NLA.IS02.not_targetNecessaryCondition
