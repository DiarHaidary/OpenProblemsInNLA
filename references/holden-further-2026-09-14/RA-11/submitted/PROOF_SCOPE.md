# Proof scope and audit

## New claims proved in the manuscript

1. Convex-order domination of a normalized PSD product-spherical quadratic form by a product of independent scaled Beta(1,n-1) variables.
2. A fractional-moment, bounded-probability upper bound for arbitrary PSD inputs; q+1 real product queries implement each complex response.
3. An explicit entropy-rate upper bound, and a matching exponential-rate lower bound ONLY for the specified empirical-average estimator on a rank-one product input.
4. A finite-support, bounded-fair-bit approximation preserving exact isotropy and the required fractional moment, with at most a factor two in sample count.
5. A two-stage, finite-bit, nonadaptive diagonal-control estimator with variance at most 2 n^q ||M||_F^2/(m s). This yields the displayed square-root-dimension query bound.

## Important exclusions

- There is NO new unrestricted minimax lower bound matching either upper bound.
- A hard example for empirical averaging is not a hard example for the full-vector oracle. In fact a fixed rank-one PSD matrix is recovered from one generic continuous product query.
- None of the proofs assumes arbitrary M is a tensor product or separable.
- All oracle calls are real product inputs. An output-derived dense vector is never submitted as an input.
- The convex-order result is stated for ideal spherical probes. The finite-support reduction preserves the needed moment bound, not exact convex-order domination.
- Numerical Gaussian sampling and floating-point interpolation are reference diagnostics, not the exact finite-bit construction in the proof.
- The finite-bit fractional-moment result is constructive existence via finite, symmetry-preserving discretization. A fully certified implementation of the discretization is not included. The diagonal estimator's finite-bit implementation is explicit.
- Previous package results are identified as inherited; this package does not claim a fresh audit of all of their proofs or establish novelty relative to all literature.
- No independent mathematical review or proof-assistant certification has been obtained.

## Unresolved full RA-11 requirement

Universal-constant matching dependence on n, q, and epsilon remains unproved. At n=2, epsilon=1/4, the retained lower scale is only Omega(sqrt(q/log q)); the new upper scale remains exp[(log 2 - 1/2) q + O(sqrt q)] times a polynomial in q.

## Execution status

Read the JSON files in `results`. A script marked passed completed its assertions; that is a check of its finite instances, not of all-parameter theorem validity. No claim is made that a huge-query estimator was run at parameters beyond the recorded tests.
