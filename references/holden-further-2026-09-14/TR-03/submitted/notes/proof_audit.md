# Proof audit

## Dependency structure

The new robust oversampled-profile theorem follows from the deterministic clipping certificate, rectangular Gaussian small-ball bounds, weighted Haar compression, and exact-spectrum grouping. The global finite-spectrum theorem then follows from spectral counting and the finite-to-infinite comparison. The all-spectrum theorem does not require a conjectural reduction to two-level spectra.

## Quantifiers

The construction first fixes the orientation and only then considers the selected subset. In comparable dimensions a union bound over row-type constraints fixes one common right rotation. In long-tail dimensions a union bound over heavy/singleton/unused group patterns fixes one Gaussian leading subspace. No part of either construction chooses a fresh orientation after learning the subset.

## Singular blocks

A singular limiting principal precision block has infinite inverse-trace cost. It is not assigned the trace of a pseudoinverse. The singular finite comparison uses the lower bound a. Covariance pseudoinverses are used only for explicitly auxiliary positive-semidefinite matrices after a positive covariance term is dropped. The two conventions answer different mathematical questions.

## Noncommuting normalization

From H >= delta*n*I, the valid matrix comparison is W H^{-1} W^T <= (delta*n)^{-1} W W^T. It gives an ordered-eigenvalue comparison for H^{-1/2} W^T W H^{-1/2}. The stronger direct column-Gram Loewner comparison is generally false; the verification suite deliberately records counterexamples to it. The proof never uses that stronger statement.

## Haar step

Harmonic compression has a conjugation-invariant marginal law and deterministic trace and norm bounds. Averaging an additional independent Haar conjugation justifies the weighted small-ball estimate without assuming a particular eigenvector parametrization at repeated eigenvalues. Different subset costs may be dependent; the union bound does not require their independence.

## Exact spectrum and additional observations

Each contrast block has the prescribed positive eigenvalues and one zero eigenvalue, with a calibrated diagonal B_ii = c*u_i^2. The group embedding is an isometry. Reserved core-tail eigenvalues and all contrast eigenvalues occupy orthogonal subspaces, so the full covariance has exactly the specified spectrum.

Positive covariance terms are dropped only after this construction, to obtain a lower comparison. Granting all coordinates in a multiply selected group favors the selector. Projection onto the leading subspace also lowers the trace error. The posterior formula after these relaxations is therefore a valid lower bound for the original error.

For a selection touching d' groups, u=k-d' and h heavy groups obey h<=u. When d'>=j=k-q, the remaining rectangular Gaussian system has r=j-h unknowns and r+(q-u) observations. The inequalities r>k/2 and 3(q-u)<r justify the uniform small-ball estimate. When d'<j, the leading posterior has an unobserved direction and diverges as the leading eigenvalues increase.

## Constants

The proof uses delta=exp(-256), a=2^{-20}delta, d0=2^{20}, epsilon=exp(-2048), c2=delta*a/64 and A=128/c2. The final profile constant is epsilon*delta*a/1024 = 2^{-30}exp(-2560). Dimensions below 2*d0 are handled by the spectral-tail baseline. Light clipping implies the dimensional feasibility inequality needed by the frame construction, so no small-dimension exception is silently passed to the Gaussian estimates.

## Boundary of the result

The upper-bound hypothesis in the preceding reduction addendum is discharged by the new proof. Matching growing lower bounds for R are not established. A lower bound for the square-frame minimax F yields an upper bound for a particular limiting ratio; it cannot be substituted into a lower-bound argument for the original supremum. The stronger sqrt(min(k,m)) denominator in the limiting theorem does not, by itself, prove a global O(sqrt(m)) estimate for arbitrary finite spectra.

## Verification limits

Finite tests can detect algebraic or implementation errors but cannot certify all orientations, dimensions, or spectra. High-precision evaluation of the probability constants verifies numerical margins, not the probabilistic lemmas themselves. No independent peer review or formal proof-assistant certification is claimed. Process logs and status files distinguish execution results from mathematical completion.
