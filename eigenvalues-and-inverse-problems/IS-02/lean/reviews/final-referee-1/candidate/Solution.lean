/- Complete proof of the frozen IS-02 statement boundary.
Formalization: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
Substantial AI-agent assistance; source mathematical credit remains with the
canonical repository and its cited authors.
-/
import NLA.IS02.Proof
import LeanCert.Tactic.Verification

set_option autoImplicit false
set_option leancert.trust "kernel"
open scoped BigOperators Matrix
noncomputable section

namespace NLA.IS02

 theorem counterexample_symmetric_nonnegative_stochastic :
    counterexample ∈ symmetricStochastic 4 := by
  exact test_membership

theorem counterexample_trace :
    trace counterexample = 1 := by
  exact test_trace

theorem counterexample_positive_trace :
    0 < trace counterexample := by
  exact test_positive_trace

theorem counterexample_spectrum :
    sameSpectrum counterexample
      (!![(1 : ℝ), 0, 0, 0;
          0, 1, 0, 0;
          0, 0, 0, 0;
          0, 0, 0, (-1 : ℝ)]) := by
  exact test_spectrum

theorem sameSpectrum_iff_realEigenvalueMultiset_eq {n : ℕ}
    {A B : Mat n} (hA : symmetric A) (hB : symmetric B) :
    sameSpectrum A B ↔ realEigenvalueMultiset A = realEigenvalueMultiset B := by
  exact test_spectrum_bridge hA hB

theorem counterexample_spectral_uniqueness :
    spectrallyUnique counterexample := by
  exact test_spectral_uniqueness

theorem counterexample_outside_locus :
    counterexample ∉ assertedLocus 4 := by
  exact test_outside_locus

theorem counterexample_claim : counterexampleClaim := by
  exact test_counterexample_claim

theorem not_targetNecessaryCondition : ¬ targetNecessaryCondition := by
  exact test_not_targetNecessaryCondition

#assert_trust kernel counterexample_symmetric_nonnegative_stochastic
#print axioms counterexample_symmetric_nonnegative_stochastic
#assert_trust kernel counterexample_trace
#print axioms counterexample_trace
#assert_trust kernel counterexample_positive_trace
#print axioms counterexample_positive_trace
#assert_trust kernel counterexample_spectrum
#print axioms counterexample_spectrum
#assert_trust kernel sameSpectrum_iff_realEigenvalueMultiset_eq
#print axioms sameSpectrum_iff_realEigenvalueMultiset_eq
#assert_trust kernel counterexample_spectral_uniqueness
#print axioms counterexample_spectral_uniqueness
#assert_trust kernel counterexample_outside_locus
#print axioms counterexample_outside_locus
#assert_trust kernel counterexample_claim
#print axioms counterexample_claim
#assert_trust kernel not_targetNecessaryCondition
#print axioms not_targetNecessaryCondition

end NLA.IS02
