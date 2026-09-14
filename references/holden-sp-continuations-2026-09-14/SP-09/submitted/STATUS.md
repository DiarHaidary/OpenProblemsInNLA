# Scope and status

**PARTIAL — not a full solution of SP-09.**

## New result established

For any fixed repetition r of the reference pair, independently split its 6r complex eigenvalues in arbitrary fixed directions. Equivalently, use the six normal r-by-r direction matrices in Theorem 1.1 of the manuscript. The squared orbit distance has right derivative equal to the explicitly specified minimum largest eigenvalue of a sum of four independently conjugated Hermitian matrices.

For each fixed r and k this derivative is unchanged by k-fold amplification. The squared amplification gain is at most O(t^(3/2)) as t tends to zero from the right. This includes splittings of all repeated eigenvalues, unlike the prior neighborhood theorem for only six scalar eigenvalues.

The new finite exact identities and their tensor lifting are proved in Sections 3-4. The lower and upper expansions are proved in Sections 5-6. The classical block-averaging theorem is explicitly attributed, with the integral-to-average normalization explained. A closed formula is given when r=2.

## Retained results

The reference-pair exact distance, its finite-amplification equality classification, the six-eigenvalue open neighborhood, and the earlier normalized Hilbert-Schmidt quantitative rigidity bound remain included under prior_round2/. Their eight exact checkers are rerun rather than replaced by numerical experiments.

## Not established

No proof or normal-matrix counterexample for arbitrary SP-09 inputs is established.

The O(t^(3/2)) gain estimate does not imply equality at a nonzero t. Its constants and validity radius are not certified numerically and are not uniform in amplification size. It therefore cannot be used to interchange the limits t -> 0 and k -> infinity.

No O(t^2) lower-error estimate, exact all-orders cancellation, or global continuation across arbitrary spectral parameter space is claimed.

One additional n=7, k=2 numerical comparison is retained as a checked feasible construction. Neither its base value nor its amplified value is a certified lower bound. It supplies no counterexample.

## Exact missing step

The reverse inequality delta_(nk)(A tensor I_k, B tensor I_k) >= delta_n(A,B) for arbitrary normal A and B remains unproved here. The first-order Hermitian deamplification theorem applies only after the local perturbation reduction, not directly to the full normal residual.

## Review status

Exact computer-assisted finite algebra, written analytic proof, and exploratory floating-point calculations are distinguished. No proof-assistant formalization, independent human peer review, or complete priority review has been completed. No repository edit was made.
