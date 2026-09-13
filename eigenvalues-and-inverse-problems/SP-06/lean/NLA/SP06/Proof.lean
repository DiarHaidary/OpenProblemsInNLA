/-
Copyright (c) 2026 George Stepaniants. Released under Apache 2.0.
Formalization: Department of Computing and Mathematical Sciences,
California Institute of Technology. AI-assisted.
-/
import NLA.SP06.Curve

set_option autoImplicit false
set_option leancert.trust "kernel"

namespace NLA.SP06

theorem witness_nonreal_finite_spectrum : ¬ allFiniteSpectraReal witness := by
  intro h
  have hz := h 2 (by norm_num) nonrealEigenvalue witness_eigenvalue_mem
  rw [witness_eigenvalue_im] at hz
  norm_num at hz

theorem witness_counterexample : counterexampleClaim :=
  ⟨witness_admissible, witness_real_jordan_curve, witness_nonreal_finite_spectrum⟩

theorem not_targetImplication : ¬ targetImplication := by
  intro h
  exact witness_nonreal_finite_spectrum
    (h witness witness_admissible witness_real_jordan_curve)

-- Audit every exported contract and every transparent target definition.
-- LeanCert rejects sorryAx, compiler-trust dependencies and custom axioms.
#assert_trust kernel LaurentCoefficients
#assert_trust kernel laurentEval
#assert_trust kernel hasAdmissibleBand
#assert_trust kernel toeplitz
#assert_trust kernel hasRealJordanCurve
#assert_trust kernel allFiniteSpectraReal
#assert_trust kernel targetImplication
#assert_trust kernel witness
#assert_trust kernel auxiliary
#assert_trust kernel radialEquation
#assert_trust kernel radiusProfile
#assert_trust kernel radialCurve
#assert_trust kernel nonrealEigenvalue
#assert_trust kernel counterexampleClaim
#assert_trust kernel witness_admissible
#assert_trust kernel witness_composition
#assert_trust kernel radial_lower_endpoint
#assert_trust kernel radial_upper_endpoint
#assert_trust kernel radial_uniform_slope
#assert_trust kernel radial_root_exists_unique
#assert_trust kernel radial_roots_lipschitz
#assert_trust kernel continuous_radius_exists
#assert_trust kernel radial_curve_continuous
#assert_trust kernel radial_curve_injective
#assert_trust kernel radial_curve_nonzero
#assert_trust kernel auxiliary_radial_im
#assert_trust kernel radial_curve_symbol_real
#assert_trust kernel witness_real_jordan_curve
#assert_trust kernel witness_toeplitz_two
#assert_trust kernel witness_eigenvalue_mem
#assert_trust kernel witness_eigenvalue_im
#assert_trust kernel witness_nonreal_finite_spectrum
#assert_trust kernel witness_counterexample
#assert_trust kernel not_targetImplication

end NLA.SP06
