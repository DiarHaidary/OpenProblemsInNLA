# Source and proof-scope audit

## Exact problem and current literature

1. **Canonical RA-01 repository entry**, accessed September 13, 2026:
   https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-01/README.md
   Used for the exact quantifiers, the residual-diagonal pivot law, and the
   displayed Open status. The website was read directly; no GitHub plugin was used.

2. **Ethan N. W. Epperly, A new analysis of the randomly pivoted Cholesky
   algorithm**, arXiv:2608.20633v1:
   https://arxiv.org/html/2608.20633v1
   Attribution: determinant-path probability method, the general oversampled
   guarantee, and the explicitly stated uniform conjecture. The retained
   denominator is used in the present proofs; the determinant method is not
   represented as invented here.

3. **Yifan Chen, Ethan N. Epperly, Joel A. Tropp, Robert J. Webber, Randomly
   pivoted Cholesky: Practical approximation of a kernel matrix with few entry
   evaluations**, CPAM 78(5), 2025, 995–1041:
   https://doi.org/10.1002/cpa.22234
   Accessible manuscript: https://arxiv.org/html/2207.06503v6
   Attribution: the RPCholesky algorithm, conditional expected-residual identity,
   scalar comparison framework, and error-doubling lemma. The rank-two starting
   bound is re-derived in the current report rather than imported without proof.

4. **Ryan Divan and Marc Aurèle Gilles, Convergence rates of randomly pivoted
   methods for low-rank approximation**, arXiv:2609.06287v1, September 5, 2026:
   https://arxiv.org/html/2609.06287v1
   Attribution: pivot-product analysis and elementary-symmetric-polynomial decay
   estimates. Their Section 3 hypotheses concern full-spectrum envelopes. The
   current note retains the head denominator and states explicit tail-normalized
   relative-error assumptions. The general power-envelope proof uses the same
   established generating-function technique, with a conservative elementary
   integral constant. No priority claim is made for this extension.

5. **NIST DLMF equation 4.36.1**:
   https://dlmf.nist.gov/4.36.E1
   External classical identity used: the infinite product for sinh. It supplies
   the inverse-square sequence's exact elementary-symmetric coefficients. Its
   application and all later constant inequalities are written out in the report.

## Relationship to prior packages

The latest prior ZIP is copied unchanged to `provenance/`. It contains the
second-round package, which contains the first-round package. The round-one
`exact_rpcholesky.py` engine is reused unchanged and its arithmetic is inspected
by the new wrapper through exact finite checks.

The sharp rank-one estimate, scalar-completion mechanism, residual identities,
and basic determinant-path framework are inherited or established tools. The
current report supplies proofs sufficient for its positive results without
assuming an unrestricted warm start.

The current package adds the explicit C=3 half-geometric-tail theorem, C=4
inverse-square-tail theorem, the displayed fixed-power constant, the unit
clock-tail-rate obstruction, and the saturation calculation. “Adds” means adds
to this conversation's written package, not a claim of mathematical novelty
relative to every external publication.

The prior all-subsets necessary bound C>=2 is retained in provenance and mentioned
as a prior claim. Its probabilistic-existence proof was not independently
re-audited in this round. None of the present upper theorems relies on it.

## Quantifiers and safeguards

The envelope scale in every new upper theorem is the first tail eigenvalue.
The tail index begins at one after the target rank. Leading eigenvalues and
complex eigenvectors are unrestricted, but tail shape is not. No unitary
invariance of the multistep sampling law is assumed.

A zero tail, a rank-deficient input, and an active dimension cap are explicitly
handled by termination. Every scalar ceiling estimate is displayed. The
finite-dimensional clock construction does not require an infinite matrix or
an interchange of asymptotic limits. Its large scalar certificate does not
instantiate the enormous matrix.

The saturation result is about a particular upper comparison, not the error
of RPCholesky. The diagonal family in that result is not a counterexample to
RA-01. Likewise the clock obstruction is not a counterexample to RA-01.

## Verification limits

The verification outputs are from programs actually executed for this package.
Rational checks certify their finite calculations, not the infinite-dimensional
quantifiers or analytic proofs. Floating subset enumeration still uses numerical
matrix arithmetic; Monte Carlo trials are weaker diagnostics. No independent
human/separate-agent audit or Lean/Coq/Isabelle verification occurred.

**Unrestricted RA-01 remains unproved and unrefuted by this package.**
