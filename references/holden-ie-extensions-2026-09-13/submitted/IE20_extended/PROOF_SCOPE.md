# Proof-scope audit

**This package is an extended partial resolution, not a complete solution
to the all-parameter IE-20 target.** The manuscript's analytic arguments
have not been independently refereed or checked by a proof assistant.

## Target and quantifiers

The upper bounds concern the specified scalar-error envelope and fixed
short recurrence. They guarantee that some produced iterate succeeds by
step n at every precision at least the displayed threshold. Success uses
the true residual against stored inputs. A recursively zero residual or a
zero divisor is not by itself success.

Upper proofs apply after homogeneous normalization to all real inputs
with the stated spectral bounds; this includes normalized versions of all
admissible stored inputs. No unjustified representability of normalized
entries is assumed. Lower constructions check stored-input significant
bits separately from the allowed intermediate error equations.

## Analytic claims and dependencies

| Manuscript location | Claim and scope |
| --- | --- |
| Theorem 2.1 | Exact scalar threshold. Counts nine factors influencing x1 and proves which corner maximizes backward error. Valid for all allowed scalar errors, not just enumerated signs. |
| Theorem 3.1 | Retained identity and conditioning-breakdown lower bounds. Failure at one precision rules out every threshold at or below that precision. |
| Theorem 3.2 | Joint n/K breakdown for K >= 15 using active first/last coordinates and rational accumulation factors. Implies P >= log2(nK)-5 for all n >= 2, K >= 1. |
| Theorem 4.1 | Exact real-input first-step extremum M(K). Does not claim its maximizing vector is p-bit representable at an arbitrary fixed p. |
| Theorem 4.2 / Corollary 4.3 | Finite-precision first-step guarantee, and matching coarse-tolerance/near-identity regions. |
| Lemma 5.1 | Prefix-wise matvec error bound with linear n. Algebraic regrouping of the frozen executed errors does not change operation order. |
| Lemma 5.2 | Local recurrence envelopes with omega = 64(n+1)Ku; actual K controls denominator perturbations. |
| Lemma 5.3 | Failure-conditioned bootstrap, including nonzero directions, positive divisors, coefficient bounds, orthogonality defects, and true-residual gaps. |
| Lemma 6.1 | Approximate polynomial containment in the actual computed direction and iterate spans. No exact rounded Krylov identity is assumed. |
| Theorem 7.1 | Three sufficient stopping horizons: n-dimensional Gram contradiction, Chebyshev approximation, or reciprocal-polynomial comparison. The last case uses the cited exact approximation lemma plus a transfer proved in this manuscript. |
| Section 8 | Exact/Theta/additive conclusions on the specified domains. In the fixed-tolerance formula the additive constant depends on epsilon, but not n or K. |
| Section 9 / prior ZIP | Retained path/outlier asymptotics for each fixed dimension followed by sufficiently large dyadic outlier. No uniform exponent threshold in growing dimension is supplied. |

The cap H = min(K,64/epsilon^2) is conditional on all iterates failing:
a step longer than the cap would itself give small backward error.
The proof first establishes a nonzero direction and legal next division;
only then does it use failure of the newly produced iterate. Thus it does
not assume the legality of a step to prove that legality.

The universal backward horizon uses Lemmas 12–13 of Dereziński,
Nakatsukasa, and Rebrova for an exact positive polynomial approximating
the reciprocal. The spectral application and rounded-span transfer are
separate arguments here. Removing that approximation fact leaves the
self-contained dimension/Chebyshev branches, but not the universal
fixed-tolerance result uniform in n.

## Remaining mathematical gap

At K=n^2 and epsilon=n^(-2), the bounds in this package remain
Omega(log n) and O(n log n). They do not determine the requested
worst-case dependence to universal multiplicative constants. No precise
order on that regime is asserted.

In particular, neither the main upper expression nor the universal
backward horizon is claimed to have a matching lower bound throughout
its domain. A stable-polynomial lower bound is not automatically a lower
bound on an admissible execution of the fixed CG recurrence.

## What the exact checks establish

The exact executor verifies significant-bit restrictions, symmetry,
positive definiteness through rational LDL^T, operation-error magnitudes,
and all recorded recursive updates. Particular input-family spectral
norms and condition bounds are justified analytically in the manuscript
or test comments; the generic executor does not compute arbitrary
matrix spectral norms or condition numbers.

For scalar sign corners and the additional first-step cases, the backward
error is compared by exact squared rational inequalities. Dense matvec
checks use matrices with analytically known norm. The joint witnesses
verify exact immediate breakdown. The retained path/outlier witnesses
check every produced iterate with a strict sufficient failure certificate
and check equality of true and recursive residuals.

The 31 reciprocal polynomial constructions have their coefficients,
degree, and double-zero division checked exactly. The 3,999 grid tests
check only the stated rational points; their universal interval bound
comes from the cited analytic lemma, not from sampling.

The 90 parameter cases check evaluator consistency on those cases. They
do not prove that a printed upper bound succeeds on all inputs; that is
the role of the analytic proof.

## What is not claimed

No full IE-20 solution, independent referee approval, formal proof,
exhaustive search over general operation-error boxes, general IEEE
round-to-nearest lower bound, or external priority claim is represented.
