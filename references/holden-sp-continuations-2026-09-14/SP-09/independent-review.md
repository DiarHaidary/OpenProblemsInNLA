# Independent informal review of SP-09 round 3

Reviewer: a separate Codex AI agent, delegated only to review SP-09, independently of the agent preparing the repository submission. Review date: 14 September 2026 (UTC). This is an informal mathematical and computational audit, not external human peer review or formal verification. No Lean verification was performed.

**Verdict: PASS for Theorem 1.1 and its stated first-order amplification corollary; NOT a full solution of SP-09. Keep `Partially resolved`.**

## Target and scope

I compared the submission against `eigenvalues-and-inverse-problems/SP-09/README.md`, `CONTRIBUTING.md`, and the status rules in `RESOLVED.md`. The canonical question quantifies over every finite normal pair and every finite amplification. The submission instead proves a right-derivative formula for independent linear spectral splittings of finite repetitions of one specific three-point reference pair. The squared amplification gain is bounded by O(t^(3/2)) for fixed repetition, fixed amplification, and fixed directions. Neither exact equality at positive t nor dimension-uniform constants follow. The manuscript explicitly recognizes this distinction. Repository policy permits audited partial results to be recorded, but does not permit `Solved` for this scope.

This is mathematically beyond the canonical page's previously recorded two-point-spectrum subclass: the reference pair has three distinct points in each spectrum, and the split directions may introduce still more distinct points. Screening all pushed branches and PRs for duplicate full solutions belongs to the coordinating agent; this review makes no claim to have performed that remote-history screen.

## Analytic audit

I read all sections of `manuscript/SP09_first_order_splitting.tex`, the prior exact-reference certificate and equality argument, and the quantitative rigidity proof used by the new theorem. I also inspected the proof-critical exact checker implementations. The submitted self-audit was treated as evidence to check, not as independent approval.

The imported reference certificate is dimension independent: its word reductions use orthogonal projections, cyclicity, and the specified normalized traces, without adding rank-one identities. Positive Gram matrices and a distinguished polynomial of trace one rule out a smaller norm. At equality, the complete degree-four relation kernel forces a unital representation of M_3, giving the claimed block-gauge orbit. The quantitative estimate bounds four relation errors through the positive Gram block and rounds the three column isometries by polar alignment. The singular-value inequalities and common Hilbert–Schmidt normalization used there are consistent.

The scalar tangent map has rank three, gauge dimension five, and one remaining flat direction. Tensoring a real skew-Hermitian basis with Hermitian coefficient matrices correctly spans the full skew-Hermitian space in dimension 3r. The lifted face map consequently has range equal to the kernel of the positive unital partial-trace map. The gauge slice follows from a complementary tangent space and the finite-dimensional inverse function theorem; compactness permits constants uniform over gauge choices at fixed r.

The lower argument does not discard noncommuting directions. Initial rigidity gives X = O(sqrt(t)); the Schur complement has the positive correction with coefficient 13/23. The positive-density face bound and inverse on the transverse complement then improve S to O(t). Only after that improvement are transverse quadratic and mixed terms O(t^(3/2)). The pure flat contribution is Q(X_*) tensor T^2, whose partial trace is the positive matrix T^2/52. Dropping this matrix is legitimate for the lower bound. This verifies the key rate-sensitive step; using the unreduced coefficient 19/2080 instead would not be the stated calculation.

For the upper bound, independent block gauges attain the four-orbit Hermitian minimum. The range identity solves the entire active-matrix correction L_r(S_0) = E tensor Gamma - G. The reference spectral gap then makes off-diagonal coupling contribute O(t^2), even though the active top eigenvalue is multiple. This establishes the stated asymmetric lower/upper expansion and hence its right derivative.

I verified the external Horn input against the primary source, Bercovici–Collins–Dykema–Li–Timotin, *Intersections of Schubert varieties and eigenvalue inequalities in an arbitrary finite factor*, [arXiv:0805.4817v1, Theorem 0.2](https://arxiv.org/html/0805.4817v1). It provides zero-sum Hermitian triples with spectra given by block integrals. For the normalized embedding of M_(rk), multiplying the r-dimensional outputs by r converts each block integral to the average of k consecutive eigenvalues. The submission's normalization is correct. Negation reverses the ordered averaged spectrum; gluing triples along unitarily equivalent partial sums preserves each individual summand spectrum. The resulting largest eigenvalue is at most the amplified largest eigenvalue. Thus the four-orbit first-order optimum is amplification invariant. This does not deamplify the original coupled normal residual, and the manuscript does not claim otherwise.

The r=2 Pauli-matrix/polygon formula and its displayed coefficient 603/364 agree with the defined spectra. Floating-point feasible constructions are unnecessary to this acceptance and are not certified lower bounds.

## Reproduction and outcome

The system Python initially lacked NumPy; this was an environment failure, not a mathematical failure. I reran the complete exact suite with an existing Python environment containing NumPy 2.3.5:

```sh
/tmp/mi27-verify-env/bin/python -O /tmp/sp-new-review/SP09_round3_proof_pack/verify_all.py --report-dir /tmp/sp-new-review/SP09-checks
```

The run exited successfully. All 208 top-level manifest entries and all 163 retained prior manifest entries matched. The eight retained exact programs passed, including the trace certificate, equality kernel, finite geometry, modular and integer minors, quantitative rigidity, and regressions. The new exact geometry calculation and all nine new corruption tests also passed. Logs and machine-readable results are in the adjacent `SP09-checks` directory, including `all_checks.json`, `new_exact_geometry.json`, and the retained-program reports. Checks run with Python optimization enabled retain explicit exception-based acceptance criteria.

No mathematical correction is required for the new first-order theorem on the evidence examined. This verdict does not separately certify every ancillary claim in the retained previous manuscripts (in particular their entire open-neighborhood transport theorem), nor establish novelty or a comprehensive later-literature search. The imported reference distance, equality classification, and quantitative rigidity needed for the new theorem were examined as described above. The unresolved universal reverse inequality must remain visible in the canonical entry.
