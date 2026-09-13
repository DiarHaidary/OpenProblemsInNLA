# Independent audit: PR #235 (RA-11)

**Verdict: PASS for the stated partial results. No actionable mathematical or publication blocker found.** This is an independent informal AI-agent audit, not human peer review or formal verification. The unrestricted target remains open.

Reviewed exact head `cd75dcd61013e0ec12191953c29755268e94106c` against published base `b73cd1804e40e0d101294eedb156984f0d62b4a6`, in `/private/tmp/nla-audit-235`. No source-worktree edits or GitHub mutations were made. The review used the full 1,083-line manuscript, reference implementation, both test suites, canonical-page diff, package records, and all 20 changed PDF pages (18 manuscript + 2 canonical). The source worktree remains clean.

## Claim coverage and proof assessment

- The canonical mathematical target, beginning with `Let n,q...`, and all following source/prior-status text are byte-identical to the published base. The arbitrary real PSD matrix, full-vector real product query oracle, adaptive/randomized quantifiers, worst-case call budget, exact arithmetic, and success probability 2/3 are preserved.
- Theorem 1.1 correctly supplies nonmatching bounds `L/80000 <= Q <= U`. Taking block size `b=q` gives `Theta(n^q)` for `epsilon <= n^(-q)`. It does not determine unrestricted complexity elsewhere.
- The interpolation proof evaluates a degree-q vector polynomial at i using q+1 real nodes. Applying the real linear map before interpolation is valid, with finite arithmetic on real/imaginary pairs. Ill-conditioning is acknowledged and permitted by this exact model.
- The projection construction has dimension q+1 by disjoint coefficient supports and Vandermonde invertibility. Its parity vectors lie in that span, are orthogonal, and have equal squared norm `2^(q-1)`. Every unit real product vector has squared combined parity contraction one. Thus its squared projection is at least `2^(1-q)`, contradicting the cited Conjecture 23 at n=2. The Fourier calculation for the Gram spectrum also checks out.
- The real fourth-moment induction, complex swap/partial-trace moment expansion, Chebyshev bounds, coordinate upper bound, and ordinary-vector fibre decomposition are valid for arbitrary PSD inputs. Low-rank exact recovery uses an appropriate nonzero polynomial minor and the PSD Nyström identity; the rank promise is explicitly necessary.
- Under the additional PSD-factor product promise, contraction after a reference query reveals the normalized local vectors. The specified shift makes every omitted-mode contraction one, including zero targets and singular factors. One reference plus n-1 basis-completion rounds gives n calls. This reduction is not asserted for arbitrary matrices.
- The local Hutch++ proof has the claimed call count, nonnegativity, unbiasedness, and scale equivariance. Its Gaussian range bound and inverse-Wishart reciprocal moment yield the variance estimate. Scale equivariance removes shared reference randomness from normalized local outputs, justifying multiplication of independent relative estimates.
- The adaptive Wishart proof is valid: conditional on an existing transcript, the next residual direction is fixed; rotation of the unexplored complement followed by the one-column Schur calculation leaves a fresh square Wishart residual. Cross-factor interleaving preserves conditional independence. Padding to t independent directions only grants information. The known trace contribution is nonnegative and observable.
- The shifted-log-chi-square density has the displayed nonpositive second log derivative. Integration by parts and two Cauchy–Schwarz inequalities give the variance lower bound. The log-concave density-height argument, good-transcript event, and logarithmic success interval establish a bounded-probability lower bound rather than inferring failure from RMSE. The hard prior is independent of the algorithm seed. The chosen dimension and small-d integer case support the universal constant 1/80000. Blocking moves to a stronger oracle in the correct direction. The zero-error corollary correctly uses atomless residuals even at one degree of freedom.

## Source verification

The source statements were opened independently; supplied reviews were not treated as proof.

- [Meyer–Swartworth–Woodruff, arXiv v2](https://arxiv.org/html/2502.08029v2): Definition 1 is the full-vector model, Theorem 7 concerns conditioned scalar vector-matrix-vector information, and Section 6 Conjecture 23 has exactly the fixed polynomial-size-span threshold contradicted here.
- [Meyer–Avron, arXiv v2](https://arxiv.org/html/2309.04952v2): Section 6 uses Wishart factors for an RMSE lower bound; Section 7/Theorem 47 records `kd+1` recovery; the rank-one one-call observation is attributed. This supports the manuscript's scope distinctions.
- [Original Hutch++ paper](https://arxiv.org/abs/2010.09649): source for the ordinary O(1/epsilon) method; the manuscript rederives the variant and constants it actually needs.
- [Prékopa's original paper, Theorems 6–7](https://rutcor.rutgers.edu/Prekopa/pdf/SCIENT2.pdf): marginalization and convolution preserve log-concavity. The manuscript's cited Saumard–Wellner review, Proposition 3.5, was also checked.
- [Official Sidney Holden profile](https://www.simonsfoundation.org/people/sidney-holden/) supports the CCB/Flatiron affiliation. This does not independently establish authorship or institutional endorsement.

## Reproduction and independent adversarial checks

All execution used scratch copies and `/private/tmp/nla-batch-python/bin/python`.

- Final package SHA-256 manifest: all 22 listed files match.
- Supplied `tests/exact_checks.py`: PASS. Exact interpolation, projection, factor recovery, zero-contraction/singular-factor, low-rank, and symbolic derivative checks pass.
- Supplied `tests/numerical_checks.py`: PASS. This includes 60,000 complex-moment samples per case, 7,000 adaptive Wishart trials, interpolation/recovery, and conditioning-spectrum diagnostics. Logs: `/private/tmp/nla-235-exact.log`, `/private/tmp/nla-235-numerical.log`; JSON in `/private/tmp/nla-review-235-run/results/`.
- Independently authored code, importing no submitted code, tested 12,000 cross-factor adaptive/interleaved trials with 3 factors, dimension 8, and 2 queries per factor. Residual means were 36.0003, 35.9691, 35.9899 versus 36; variances 72.2749, 72.0496, 71.1065 versus 72. Cross-factor correlations and means binned by known total trace met the specified checks. Sixteen shifted-log-chi-square variance quadratures at df 2,3,9,36 and shifts 0,0.1,10,1000 met the analytic lower bound. Evidence: `/private/tmp/nla-independent-235-237.py` and `/private/tmp/nla-235-adversarial.json`.
- Read-only visual inspection of every manuscript and canonical PDF page found no clipping, missing symbols, overlap, unresolved references, or scope inflation. Rendered review evidence is in `/private/tmp/nla-review-pdfs/`.

## Limits

Finite algebraic tests, quadrature, moments, correlations, and Monte Carlo do not establish the universal theorems or posterior independence; those conclusions rely on the written arguments audited above. This review does not certify exhaustive novelty or later-literature absence. Numerical code is explicitly a small-instance demonstration with underflow/rank-threshold/interpolation conditioning limitations. No Lean verification was claimed or performed. This audit supports recording **Partially resolved**, never **Solved**, for the existing RA-11 target. Root review handles shared registry/catalog/CI integration.
