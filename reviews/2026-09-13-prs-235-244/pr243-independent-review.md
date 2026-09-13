# PR #243 independent mathematical audit

**Verdict: PASS for the new restricted-class and distribution-specific partial results. No actionable blocker found.**

Audited head: `1f3191cb16304fa6faed5b398f24dc8c2030b735` against base `b73cd1804e40e0d101294eedb156984f0d62b4a6`. Source: `/private/tmp/nla-audit-243`. Review date: 13 September 2026. This is independent informal AI review, not external human peer review or formal verification.

## Scope and original target

The original target is the all-simultaneous finite-parameter query complexity for arbitrary measurable adaptive `Av`/`A^T v` queries, pointwise 0.99 success and individually charged vector products. Theorem 2.2 restricts algorithms to a deterministic initial width, fully charged rounds, no fresh directions and no within-round adaptation; arbitrary measurable output subspaces are allowed. Theorem 10.1 applies only while `J > hI`. Theorem 11.2 averages over a particular shifted-Wishart rank-one input law and the random start. These qualifications are present in the manuscript, canonical README/TeX/PDF, submission record and new RESOLVED entry.

The PR appends to the canonical page without removing earlier mathematical claims, references, credit or their qualifications. The original unrestricted target, permanent path/ID, earlier #190/#220 contributions and Partially resolved status remain intact. It does not claim to close the unrestricted finite-accuracy transition.

## Argument coverage

Read the entire new 860-line report and both appendices, compared it with the preserved package/report.tex, read all new implementation and component-test source plus check/manifest drivers, and independently checked the used v5 charged warm-start theorem and its full Appendix A proof. The attributed report differs only in author/affiliation/date/metadata, title spacing, prior-directory locations and the informal-review notice; mathematical arguments are unchanged. Prior reviewer PASS language was not used as mathematical evidence.

### Theorem 2.2: restricted full-block classification

- The residual graph criterion follows by applying the residual inequality to every perpendicular vector `(-F^T y,y)`. It is a weighted cone, including negative tail eigenvalues; replacing it by a constant-angle criterion would be invalid.
- Chebyshev extrema cardinal signs, weighted interpolation mass and the exact hyperbolic denominator identity check. The endpoint bound and harmonic sum estimate give the claimed `10 s H_d T_d(a)` bound for all `d>=1` and original accuracies.
- The reciprocal Gaussian Gram bound follows from the shrinking net, chi-square small-ball bound and norm exception; integration is finite for `m>=8B`, including the worst endpoint `m=8`. Constants 3000 and the leading-block exceptional probability are valid.
- Integer multiplicities explicitly fit `n-k` and satisfy every rank condition. Matrix Cauchy–Schwarz acts simultaneously on the complete coefficient space, so the polynomial may be selected after observing the Gaussian block. Markov plus the leading norm event genuinely excludes every nonzero cone vector with the advertised probability.
- The compact-group averaging proof supplies a conditional-law version invariant under the observed-prefix stabilizer. Replacing the external output frame by a fresh projected Gaussian frame preserves its Gram matrix and average success probability. The augmented initial span is independent of the Haar input; after rotation it has the needed uniform Grassmann law. Thus arbitrary outputs are covered without pretending arbitrary queries have been simulated.
- The projector argument rules out insufficient fixed starting widths. Large-rank, small `n/b`, and large `n/b` cases cover all finite parameters. The threshold at `log(n/b)=48`, multiplicity cost, floor absorption, and monotonicity of `b log(en/b)` have the correct direction. The spectrum may depend on deterministic width; no minimax exchange over randomized widths is used.
- The upper algorithm concatenates both starts before replies, uses two fully charged rounds per normal-matrix power and chooses exact recovery before observing the input. Degree `2d2` supplies both polynomial image stages. Appendix B supplies Gaussian estimates, rank-zero handling, scale estimation, right-singular-vector extraction for the possibly indefinite surrogate, and the scalar-to-matrix residual certificate. There is no hidden selective-column saving or omitted product.

### Theorem 10.1 and Corollary 10.2: shifted posterior

The base singular Gaussian completion is preserved for predictable adaptive directions. The pseudodeterminant factors as `det(J) pdet(S) det(I+Q^T KQ)`. The tilt cancels the positive-block determinant exponent and leaves the stated angular density. Conditioning the global spectral wall and eliminating `J-hI` yields `S-h R_h`; eliminating its forced negative kernel block yields the shorted wall. Translation of the determinant-exponent-zero Wishart density produces both the shifted positive block and the angular exponential factor. The trace/shorting identity and normalized full-kernel graph are correct. The compact angular density is finite for each transcript on the explicitly stated domain.

The next compression pivot is exactly `gamma_Q chi-square_(m+1)-h eta_Q`; the first-exit CDF follows. This is a one-step identity, not a stopping-time lower bound. The subsequent necessary-exit implication uses the v5 warm-start theorem with a valid gap and fully charged output directions. Its used proof was checked, including the noncommuting trace estimate and Chebyshev/Fejer bound.

### Lemma 11.1 and Theorem 11.2: ensemble upper bound

Direct Gaussian integration by parts gives `r=(N-r-1+t) E tr R + t E tr R^2 + t E(tr R)^2`; taking `N=r+1` and Jensen proves the mean-resolvent bound. Translation of the positive Gram density gives the exact exponential law for the least eigenvalue. Resolvent derivatives are integrable for fixed positive shift.

The rank-one algorithm depends only on the known ensemble parameters and oracle products. On the spectral events its tail interval is `[0,1-4 epsilon]`; the comparison threshold is below the actual `(1+epsilon) sigma2(A)` target. Weighted residual-cone control, the resolvent expectation, Markov bound, Gaussian leading-coordinate event and Chebyshev growth combine with total exceptional probability below 0.002. Exact-recovery branches and the ceiling/log bounds establish the finite advertised query cap. This gives an averaged `O(n log log n/log n)` algorithm at the stated transition and therefore rules out this particular input law as a linear lower-bound witness; it does not give a pointwise all-input upper bound.

## Primary sources checked

- [Bakshi–Narayanan v1](https://arxiv.org/html/2304.03191v1), Lemma 6.3/Section 6.2: the imported comparison really has a triangular family of starts/powers and a quadratic dimension condition. The report correctly declines to use it as a same-cost arbitrary-query reduction.
- [Braverman–Hazan–Simchowitz–Woodworth v3](https://arxiv.org/html/1911.02212v3), Lemma 3.4 and associated Wishart method: relevant antecedent, not a source of an unproved shifted-posterior theorem.
- [Chen et al. v2](https://arxiv.org/html/2508.06486v2), Sections 2.1 and 3.5: logarithmic gap/condition-number qualifications and the input-perturbation mechanism support the distinction from the present fixed-span class. The unusual HTML body date does not change the arXiv version identifier.
- [Official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) confirms the credited CCB/Flatiron affiliation. This is not independent proof of authorship or priority.

The new restricted/resolvent arguments use explicit elementary proofs, not an unseen external lower-bound theorem. The older unrestricted v5 lower-bound chain and its Rudelson–Vershynin dependency were not re-audited as a new theorem here; their existing canonical contribution is preserved. The specific v5 warm-start argument actually used in Section 10.4 was independently read.

## Fresh checks and independent adversarial work

Runtime: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0. All 45 new component tests passed, log `/private/tmp/nla-243-new-tests.log`. Source was read before execution; bytecode was disabled. Main diagnostics were executed from the scratch copy `/private/tmp/nla-243-check-package`, with output outside the archive.

Fresh `/private/tmp/nla-243-new-results/summary.json` reproduces:

- 72 whole-coefficient-space diagnostics: 42 no-cone outcomes, 30 not excluded, zero numerical errors; none meets the deliberately conservative sufficient analytic condition. The report truthfully says this.
- 12,000 reciprocal-Gram draws over 12 cases; 42 scalar cases; 45 shifted geometry cases, maximum trace-identity error `1.43e-14`.
- 8,000 resolvent draws across 16 parameter cases. The finite-sample discrepancy remains; it is not treated as a theorem refutation or hidden by rerunning until favorable.
- 96 ensemble rank-one trials: all passed the actual-target diagnostic, 64 polynomial/32 exact branches, maximum queries/F approximately 2.2972.

Independent scratch code `/private/tmp/nla-independent-239-243.py`, which does not import manuscript helpers, checked 15 Schur geometries including empty transcript, residual codimension one, noncommuting blocks and compression only `1e-4` above the wall. It checked the reciprocal-compression version of shorting, the full kernel residual, spectral wall and pseudodeterminant. Maximum relative shorting error was `1.58e-12`, normalized kernel residual `1.67e-16`, log-pseudodeterminant error `9.33e-13`.

A separate direct rejection-disintegration experiment with residual dimension two and `k=1` compared the angular posterior against quadrature: 250,000 proposals / 193,526 accepted, predicted `E[Q11]=0.5061251`, sampled `0.5048400` with standard error `0.0008032`. The independently shifted positive Gram remainder had mean 1.99898 versus exact 2. Conditional first-exit samples covered near-kernel, intermediate and near-complement directions; CDFs agreed within the stated sampling tolerances. Evidence is in `/private/tmp/nla-independent-239-243-results.json`. These are supplemental diagnostics, not proof of disintegration on zero-probability transcripts.

The original package verifier passed all 39 manifest-listed payloads. The nested prior v5 PDF is byte-identical to the already-published base submission `references/holden-ra14-v5-2026-09-13/submitted/report.pdf` (SHA-256 `a9c10478b4d8a70a0d14a48aab859e8f1186ade7f9579bda02d33c0587fd7f47`). The older nested v3–v5 suites and 500,000-draw resolvent holdout were not rerun; no claim of 110 freshly rerun tests is made.

## PDFs and preservation

Used the PDF skill read-only, rendering and visually inspecting all 21 attributed-report pages and all three canonical problem pages. Rendered all 21 original package-report pages too; pages 3–20 are pixel-identical to the inspected attributed version, and all three differing pages 1, 2 and 21 were separately inspected. The differences are consistent with the source attribution/review/provenance edits. No clipped/overlapping equations or damaged symbols were found. Relevant retained v5 warm-start pages 15–16 (plus surrounding page 14) were also visually inspected; the rest of that inherited PDF is unchanged from published base.

The report and canonical PDF maintain clear scope restrictions and prior-source credit. No PDF/source/GitHub mutation was performed, and source worktrees remained clean. Root review owns common catalog/ID/CI checks.

## Disposition limits

Acceptable as incremental partial progress. This audit does not certify a full RA-14 solution, a randomized-width lower bound, a cost-preserving all-adaptive reduction, or a first-exit lower bound. No Lean proof exists or is claimed. Acceptance of the new mathematical scopes rests on the complete arguments above, with computations as corroboration.
