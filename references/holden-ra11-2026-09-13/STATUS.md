# Mathematical status and proof audit

## The requested target is not fully resolved

RA-11 asks for the unrestricted adaptive minimax query complexity for **every**
real PSD input, up to universal constants simultaneously in n, q, and epsilon.
The lower bound L/80000 and upper bound U in manuscript Theorem 1.1 do not
match in general. This package is therefore a **partial-result package**.
The matching result for PSD tensor products is not a matching result for all
PSD matrices.

## Arguments supplied

| Result | Evidence and scope |
|---|---|
| q+1 real simulation of one complex product response | Finite polynomial interpolation identity; exact finite symbolic checks. |
| Projection-conjecture counterexample for n=2 | Parity-vector proof for all q; exact symbolic checks for q=2,...,8. Refutes the universal polynomial-span statement of arXiv v2 Conjecture 23, not a conditioning-restricted variant. |
| r-query PSD reconstruction under rank <= r | Nonzero-polynomial genericity argument and an exact Nyström identity; finite rational tests. A rank promise is needed for the stopping budget. |
| n-query exact recovery of PSD tensor products | Explicit normalization-and-shift reduction and basis recovery. Exact trace recovery is also shown to require n calls, using the atomless residual posterior. The product promise is essential. |
| Theta(min(n,sqrt(q)/epsilon)) for the product subclass | Parallel unbiased local Hutch++ upper bound and independent bounded-probability lower-bound proof. |
| Blocking lower bound for arbitrary PSD inputs | Simulation into a stronger parallel block oracle followed by the product-factor lower bound. |
| General upper bounds | Basis reconstruction, real sphere estimator, real-simulated complex sphere estimator, and ordinary Hutch++ simulation. |
| Theta(n**q) at epsilon <= n**(-q) | Matching lower scale from one large block and the exact basis upper bound. |

## Critical proof checks

**Full-vector versus scalar information.** The source's conditioned scalar
quadratic-form trace lower bound is not imported into the full-vector model.
For example, a generic full-vector response already determines rank-one PSD
trace exactly.

**Adaptivity.** The Wishart posterior proof is an induction on the chronological
query transcript. A new local direction is measurable from already exposed
information. Conditional rotational invariance permits choosing it as a new
basis direction, and the newly exposed column leaves a fresh, independent
square Wishart Schur complement. Cross-factor interleaving is allowed. The
proof does not condition on a fixed adaptive subspace as though it had been
chosen independently of the matrix.

**Probability, not RMSE.** Conditional traces have the form a_i+X_i. The logs
have log-concave densities, and the variance lower bound is converted to a
uniform upper bound on the probability of a short interval. This explicitly
bounds success probability below 2/3 on a prior independent of the algorithm's
random seed.

**Unknown factor scales.** The reference query exposes gamma = product gamma_i,
not the individual gamma_i. The algorithm uses only gamma and B_i g_i obtained
by contractions. Shifts normalize all unwanted contractions to one, so no
unknown normalization is needed. Scale-equivariance of the local estimator
makes its relative errors independent of the reference randomness.

**Singular and zero inputs.** Nonzero PSD factors have positive generic reference
quadratic forms almost surely. The global zero input is detected by zero gamma;
the exceptional reference event for any fixed nonzero promised input has
probability zero. Rank selection handles singular local sketches in exact
arithmetic. Numerical rank thresholds are only part of the demonstration code.

**Call counts.** Interpolation uses q+1 real calls, not a direct complex oracle.
Exact product recovery uses one reference plus n-1 rounds. The local Hutch++
construction uses at most 5r+4 ordinary calls and parallel access adds one
reference call. Ordinary unstructured-vector simulation is charged
n**(q-1) original product calls per ordinary call.

**Exact arithmetic.** Large interpolation coefficients are allowed by RA-11.
Theoretical identities require no limiting, infinitesimal, or digit-extraction
operations. Gaussian samples are understood in the standard exact-real
randomized oracle convention used in the source literature.

## Verification limitations

No independent reviewer has certified the arguments. No formal proof assistant
has checked them. The finite symbolic tests do not quantify over every input,
and the Monte Carlo tests do not prove independence, minimax hardness, or a
uniform success probability. The lower-bound proof and its adaptive conditional
independence step merit particular independent scrutiny.

The literature search was not a proof of novelty. The Gaussian range-finding,
Hutch++ and Wishart ingredients have prior precedents; the manuscript cites
those precedents and states the additional reductions and probability argument
explicitly.

## What a complete RA-11 resolution would still need

A matching upper or lower bound for **arbitrary PSD matrices**, in every
parameter regime, not only tensor products or low-rank promises. In particular,
none of the following is justified by this package: a universal polynomial-in-q
algorithm; an unconditional exponential-in-q lower bound for fixed relative
error; applying parallel factor access without a factorization promise; or
promoting a seed-dependent deterministic adversary to a randomized minimax
lower bound.
