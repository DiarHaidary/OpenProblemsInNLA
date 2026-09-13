# Independent informal review of the RA-11 research package

- Review date: 2026-09-13.
- Reviewer: independent Codex AI agent, task `independent_ra11_review`, separate from the agent preparing the repository submission.
- Reviewed document: `manuscript/ra11_partial_results.tex` in the supplied `RA11_research_package.zip`.
- SHA-256 of the reviewed original TeX: `3ae2c62b99ef4eab0b1f81cce45218ce22ba452abf2afe74aed8409a0f0811d3`.
- Comparison target: the canonical RA-11 README, including arbitrary real PSD inputs, full-vector real product queries, unrestricted adaptation, and simultaneous constant-factor query complexity in all parameters.
- Evidence level: independent informal mathematical audit with reproducibility checks; no Lean verification, proof certificate, or external human peer review.

## Verdict

**PASS for the stated partial results; NOT a complete resolution of RA-11.** I found no material mathematical error in the claims audited below. The manuscript itself explicitly leaves the general upper/lower gap unresolved. The repository's resolution policy therefore permits **Partially resolved**, provided the canonical statement is preserved and the unresolved full parameter range is stated. It does not permit **Solved**, **Solution claimed**, or **Lean verified** on the strength of this package.

The tiny-error regime `0 < epsilon <= n^(-q)` does settle a substantive parameter range of the original arbitrary-PSD target: the displayed bounds imply `Q = Theta(n^q)` there with universal constants. The product-matrix promise theorem is a separate restricted subclass, not an assumption that may be imposed on the original question. The projection-conjecture counterexample also does not resolve RA-11's minimax question.

## Mathematical checks

Locators below use stable TeX labels and section names in the reviewed source.

1. **General bounds and restricted-product theorem** (`thm:main`, `thm:productmain`). The stated upper bounds and blocking lower bound follow from the later arguments, and the constants and endpoint regimes are consistent. Taking block size `b=q` supplies the tiny-error specialization. For the product upper bound, with `X=sqrt(k)/epsilon>2`, `5 ceil(8X)+5 <= 45X`, so the displayed final constant is valid. The nonmatching general bounds cannot be interpreted as a simultaneous characterization.

2. **Interpolation simulation** (`thm:interpolation`, Section 2). Evaluating the degree-at-most-q vector polynomial at `i` by q+1 real nodes is exact; applying the real map before interpolation is legitimate. The implementation uses finite arithmetic on real pairs. Large interpolation coefficients affect stability but not the stipulated exact-query model.

3. **Projection counterexample and conditioning** (`thm:counterexample`, `prop:conditioning`, Section 3). The disjoint-support coefficient vectors and the Vandermonde matrix establish dimension q+1. The real and imaginary parity vectors are orthogonal, both have squared norm `2^(q-1)`, and the sum of their squared inner products with any unit real product vector is one. This proves the deterministic projection lower bound. The Fourier-column orthogonality in the Gram calculation gives eigenvalues `(q+1) 2^(-q) binom(q,a)` and hence the claimed condition number. I independently checked [Conjecture 23 in arXiv:2502.08029v2, Section 6](https://arxiv.org/html/2502.08029v2#S6): its polynomial-size fixed-product-span formulation and probability threshold are the ones contradicted here. This finding concerns that stated conjecture; it does not contradict the conditioned theorems or claim a full trace-complexity solution.

4. **General upper bounds and low rank recovery** (`lem:real4`, `lem:complexmoment`, `prop:lowrank`, Sections 4–5). The real fourth-moment induction applies to arbitrary coefficient tensors. The complex swap expansion and partial-trace Frobenius bound are valid for PSD inputs. The estimator variances give the advertised Chebyshev probabilities. Ordinary-vector fibre decomposition costs at most `n^(q-1)` product queries. The nonzero-minor polynomial argument supplies almost-sure spanning under a rank promise, and the PSD Nyström identity then recovers the matrix.

5. **Parallel factor access and exact recovery** (`thm:parallel`, `cor:exactn`, Section 6). PSD guarantees strictly positive reference quadratic forms almost surely for a fixed nonzero promised input. Normalization gives `b_i^T g_i=1`; the specified shift makes every omitted-mode contraction one. Subtracting the known shifted part recovers every local product in a single shared round, including zero target products and singular factors. The reference direction plus n−1 basis-completion rounds accounts for exactly n calls. This reduction depends essentially on the product-matrix promise.

6. **Hutch++ and the product upper bound** (`lem:hutch`, `prop:productupper`, Section 7). The conditional mean is constant and the conditional variance is `2 ||R||_F^2/r`. The range approximation inequality, inverse-Wishart reciprocal expectation, and spectral-tail bound yield the displayed variance constant. Scaling preserves the sampled range, so pathwise scale-equivariance removes dependence on reference normalization in the product of normalized estimators. Independent factor randomness then gives the product variance and the stated success probability. The finite n=20 demonstration is correctly identified as a branch test, not an accuracy certificate for the conservative theoretical parameter choice.

7. **Adaptive Wishart posterior** (`lem:posterior`, Section 8). This is the central lower-bound issue. For a fixed queried span, conditioning on the observed Gram block and cross block leaves a square Gaussian residual of dimension d−t. Its squared Frobenius norm has law `chi-square((d−t)^2)`. For an adaptive next direction, conditional on the transcript that direction is fixed; orthogonal invariance permits rotating the current complement before exposing its next column. The one-column Schur calculation then leaves an independent square Wishart residual of one smaller order. A query to one factor, selected from the shared transcript, does not expose any other independent residual. Induction therefore handles adaptive interleaving across factors. Padding dependent-query transcripts only grants additional information and leaves an original estimator measurable. The known trace term is observable, nonnegative, and at most the realized total trace. I found no adaptivity/conditioning gap in this argument.

8. **Success-probability lower bound and blocking** (`lem:loggamma`, `lem:lc`, `prop:lower`, Section 8; Section 9). The shifted log-chi-square density has nonpositive second log derivative for the used degrees of freedom. Integration by parts and two Cauchy–Schwarz applications give the log-variance bound. The one-dimensional density proof yields the loose constant 8; convolution preserves log-concavity. On the stated good transcript event, at least half of the factor log variances have the required lower bound. Multiplicative success is an interval of log length at most `3 epsilon`, giving the probability bound rather than merely an RMSE claim. The chosen hard-support dimension, d/4 budget, integer small-d case, and universal 1/80000 constant all check out. The prior is independent of the algorithm's seed, avoiding a seed-dependent adversary. Blocking passes to a strictly stronger ordinary parallel oracle, so the lower-bound direction is correct. The zero-error subclass corollary uses only non-atomic residuals and remains valid when the residual has one degree of freedom.

## Reproduction and limits

Both supplied suites were rerun successfully on 2026-09-13:

- `tests/exact_checks.py`: all exact rational/Gaussian-rational assertions passed with SymPy 1.14.0; covers interpolation, projection calculations, factor recovery including singular/zero-contraction cases, low-rank reconstruction, and a log-density derivative identity.
- `tests/numerical_checks.py`: all diagnostic assertions passed using the supplied seed 20260913 and the bundled Python/NumPy runtime. These are finite floating-point diagnostics, not a proof of the posterior independence or universal claims.

Separate rerun JSON evidence was retained as `exact_checks.json` and `numerical_checks.json` alongside this review's local checking artifacts. Original package result files were restored from the uploaded archive after recording the reruns. No Lean work was performed.

This review does not establish exhaustive novelty/priority, an author's institutional affiliation, or absence of duplicate prior submissions; those are submission checks for the preparing agent. It audits the supplied mathematical argument and its correspondence to the exact repository target. Ordinary editorial changes to author attribution or review-status wording do not change this mathematical verdict; changes to mathematical claims require renewed review.
