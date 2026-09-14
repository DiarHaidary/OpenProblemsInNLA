# RA-11 independent review

Reviewer: independent Codex AI agent `/root/review_ra11_sp10` (separate from the submitting coordinator).
Date: 2026-09-14 (UTC).
Review type: informal mathematical audit, not external human peer review or formal verification. No Lean verification was performed, as requested. Attached-document directives were treated as source data, not as authorization.

**Verdict: PASS for the new partial results listed below; FAIL to satisfy the full-resolution criterion. Retain Partially resolved.**

The canonical target is unrestricted randomized full-vector real product-query complexity Q(n,q,epsilon), to universal constant factors simultaneously in all parameters. CONTRIBUTING.md and RESOLVED.md require a complete argument for that exact target before Solved is appropriate. The submitted manuscript expressly leaves this target open.

## Accepted scope and mathematical review

- Theorem 3.2: convex-order domination for arbitrary Hermitian PSD matrices. The rank-one contraction has a PSD partial trace of trace one; conditional unitary invariance supplies an independent scaled Beta variable. Spectral Jensen extends the conclusion to all PSD matrices. Tensor factorization of the unknown matrix is not assumed.
- Theorem 2.1 and Corollary 2.3: the fractional-moment upper bound, its q+1 real-query implementation, and entropy-rate estimate. I checked symmetrization, the nonnegative-difference moment bound, Markov constants, interpolation degree and Taylor optimization. The sample count has the required epsilon exponent and confidence 2/3. The real oracle returns enough information to reconstruct each complex response by exact interpolation.
- Theorem 5.1: sharp exponential rate for the specified empirical-average estimator. Size-biasing and truncation prove the lower statement; the moment estimate proves the converse. This is not an unrestricted oracle lower bound: the manuscript correctly exhibits one-query recovery of a fixed rank-one matrix from a generic continuous product query.
- Section 6: existence of a bounded-fair-bit isotropic approximation sufficient for the fractional-moment estimate. Permutation and coordinate phase symmetries give exact isotropy; compactness and uniform continuity give uniform directional moments; the tensor moment induction and doubled sample count are valid. This is an existence/preparatory-computation result. No certified implementation or practical bit-complexity bound is established. Exact convex-order domination is not claimed for the finite law.
- Theorem 2.2: explicit nonadaptive diagonal-control bound min{N, 2 ceil(sqrt(6N)/epsilon)}, improving 6 to 3 for power-of-two N. Product Rademacher isotropy suffices for the diagonal squared-error identity because x_i squared equals one. Conditional unbiasedness removes the training-mean variance term. The dyadic modulo sampler has p_i at least 1/(2N), so Chebyshev yields the stated confidence. Coordinate corrections are legitimate product inputs.

## Checks actually run

After inspecting the code, I imported and ran the functions in code/exact_checks.py without changing source artifacts. Five exhaustive diagonal cases and twelve Gaussian-rational interpolation cases passed; the 6,300-point moment grid passed. The diagonal/interpolation calculations use exact fractions, while the moment grid uses floating point. Fresh results are in [RA-11-checks.json](RA-11-checks.json). These checks supplement, rather than replace, the mathematical review. The numerical simulation suite was not rerun.

## Exclusions and unresolved target

Earlier packages' lower bounds, fixed-q optimality, and previous upper envelopes were not independently re-audited here. The manuscript clearly labels those as inherited. Claims of improvement relative to those envelopes are conditional on their correctness. No literature novelty conclusion is made. At fixed binary local dimension and fixed accuracy, the new upper bound remains exponential in q while the reported unrestricted lower bound is polynomial; the estimator-specific sharp rate does not close that gap. The full resolution therefore does not pass repository policy.

## Source binding

SHA-256 hashes of the reviewed original files:

- `manuscript/ra11_probability_diagonal.md`: `45d8702ecf627c46ab799ec13ec569438e521ba49259546a3c0323f8d258956c`
- `PROOF_SCOPE.md`: `0ef2cbccf13115a3aacca02fc5f3a28003ec1924639f0edc3f6d876c7a943e51`
- `code/exact_checks.py`: `fbf5f3ce8ce1e948f42d9b01aadbf41e383f282f90c59c421839dea7e11e7275`

Signed: independent Codex AI reviewer `/root/review_ra11_sp10`, 2026-09-14 UTC.

## Final integration check — 2026-09-14 UTC

PASS. I compared the attributed manuscript against the reviewed original: differences are author/affiliation/disposition/review frontmatter, title presentation, and URL autolinks; the mathematical body is unchanged. I reviewed the canonical notice and this submission’s RESOLVED.md entry: they accurately retain Partially resolved, describe the accepted partial scope, and do not extend the fresh audit to excluded inherited claims. Original targets are retained. This integration check does not independently verify authorship/affiliation, PDF rendering, or other problems’ outcomes.

- `references/holden-further-2026-09-14/RA-11/manuscript.md`: SHA-256 `a3aae7ab132f32a343cddfc73f871190411dfcef5dbee6b29b5b6f19b5eb09da`
- `randomized-and-low-rank-approximation/RA-11/README.md`: SHA-256 `4112f023f4e319d332de6bd2b3efe1c8908f65fe0043446d60bf0e758ae0d334`
- `RESOLVED.md`: SHA-256 `0bb64b8c078e6780ce4282bb55cc99f777da1cbf3e62d06b58613aacc876acb8`

Signed: independent Codex AI reviewer `/root/review_ra11_sp10`.
