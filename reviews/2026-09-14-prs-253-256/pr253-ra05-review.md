# Independent review of PR #253: RA-05 full classification

Reviewed PR head `43183e8254d121aa4b365fdd34643cc4c91d8503` against published base `deb549fa9ddd6b119e6c59016f268237e645dfa2`, on 14 September 2026. Reviewer: separate Codex audit agent. Source checkout: `/private/tmp/nla-audit-253`. This review did not rely on the submitted PASS report, did not modify the source checkout, and did not perform GitHub mutations.

**Verdict: no actionable mathematical or presentation blocker found. The submitted two-part argument supports marking the original RA-05 target Solved under the repository's informal independent-review policy. It does not support a Lean-verified label.** This conclusion is an informal AI-assisted mathematical audit, not external human peer review, a proof-assistant certificate, or a priority determination. Integration, permanent-ID validation and CI remain the coordinator's responsibilities.

## Exact scope and relation to earlier contributions

Read both complete new proof sources (667 and 1,058 lines), the canonical README and original question, the submitted proof/dependency notes and checkers, and the prior PR #247 independent review. The new result concerns every fixed real `p>2`, every integer `k>=1`, every `0<epsilon<1/2`, all finite input row counts and ambient dimensions, and unrestricted input rank. Upper bounds have nonnegative weights supported on original rows and simultaneously preserve all fitted subspaces of dimension at most `k`. Constants may depend only on the fixed exponent.

The rate is `k^(p/2)/epsilon^2` for non-even `p`, and

`min(k^(p/2)/epsilon^2, k^((p+1)/2)/epsilon + k^(p/2-1)/epsilon^2)`

for even `p>=4`, up to the explicitly stated logarithmic factors. The non-even lower logarithmic loss is `log(2k/epsilon)^(5p/2+3)`; the full upper loss is at most exponent `p+5`; the improved even upper branch uses exponent five. The even lower bound has no logarithmic loss.

This is more than the previously accepted high-accuracy even-power result. Part II proves the missing intermediate-accuracy estimate for every even power, using a new uniform polynomial Gaussian argument, and Part I supplies all non-even powers. There is no interpolation in the exponent. All original question text, permanent path/ID and preceding quartic, all-exponent lower-bound and high-accuracy contributions remain present. The dated notice expressly supersedes historical remaining-gap statements. The subsidiary additive proposal is also disproved for each fixed `p>2`, with a strictly positive polynomial exponent gap.

## Part I: non-even lower bound

- **Stable core.** Independently checked the Gaussian increment comparison, radial lower tail, moment normalization and simultaneous positive-probability event. The absolute-power kernel need not be positive semidefinite: its symmetric spectral truncation suffices. Restricted invertibility selects actual columns with squared least singular value at least `3/64`, while retaining bounded row sums and `Theta_p(r^(p/2))` selected rows.
- **Fourier coefficient.** The cosine remainder integral is absolutely convergent, has a strict alternating sign by two integrations, and scales to the absolute non-even power. The Walsh character kills every subtracted polynomial. With the cube dimension a multiple of four and its middle degree exceeding `p`, both trigonometric exponents are even; the integral has no sign cancellation. Recomputed the interval bound around `pi/4`, the resulting eigenvalue estimate, binomial multiplicity and original-column selection. The dependence on the distance to an even exponent is allowed in the fixed-`p` constants.
- **Simultaneous support conversion.** Product normals are legal hyperplane queries after choosing `rh<=k+1` and padding. The entire error matrix is exactly `G Delta F^T`; its Frobenius lower bound uses both least singular values. Every omitted original tensor row contributes one to `||Delta||_F^2`, even for signed and input-dependent weights. The argument controls all groups together and does not improperly sum independent bad-query conclusions.
- **All parameter ranges.** Maximal admissible cube dimension gives `h=O(log(1/epsilon))` and `N>=c_p epsilon^-2 h^(-2p-3)`. The core pays the additional `h^(-p/2)` factor. When the tensor cannot fit, `k=O_p(log(2k/epsilon))`, so the separate unrestricted-rank block lower bound absorbs the missing rank power. The constant-accuracy case is separately covered. Thus no small-rank or extremely small-accuracy hypothesis is left in the theorem.
- **Small-rank construction.** Independently derived the two rank-`k` block projectors, residual formula, positive group-mass estimate, power-difference inequalities and final Cauchy--Schwarz/convexity support bound. The ambient dimension can grow with accuracy without changing query rank. Positivity is used precisely in this fallback and the constant-accuracy mass argument.

## Part II: full even-power classification

- **Uniform structured Gaussian estimate.** Checked the Gaussian squared-norm moment-generating-function bound and its singular/zero cases. Polarization gives a common constant-mesh norming set for vector-valued homogeneous polynomials in any finite-dimensional normed domain. Using the norm induced by the head rows on `k x k` matrices gives a deterministic set of size `exp(O_s(k^2))`, with no conditioning factor. Left variance bounds the fixed-query Frobenius mean; full vectorized covariance separately bounds its Gaussian top variance. A union bound produces `sigma+O_s(vk)`. The Gram-factor/isometry reduction covers arbitrary output dimensions and rank-deficient maps.
- **Geometry and all expansion terms.** Checked optimal-head existence and spanning, Lewis normalization, scalar sensitivity, Gaussian transfer to Euclidean residuals, both densities, singular feature ranges and zero tails. The tensor degrees and common scalar/vector outputs in the mixed factorization are correct; the odd case is not falsely treated as a rank-one query. Recomputed the Frobenius bounds and identities `j+c<=s-1`, `l+j+c<=2s-1`. Balanced cross terms, the one-cross anisotropic case and the recombined pure-tail class are all separately covered.
- **Protection costs.** Protecting a matrix-Hilbert output eigendirection costs one scalar equation. After imposing those equations and further coefficient restrictions, the output covariance has range in the unprotected space and is dominated by the compressed full covariance. Its top eigenvalue is bounded by trace divided by `q+1`. Left variance contraction remains valid independently. Substituting both scales into the structured estimate gives the claimed improved `k^(s+1/2)` term.
- **Partial coloring and induction.** The good increment sets are symmetric convex seminorm balls, and the finite intersection has sufficient Gaussian measure after choosing constants. Rothvoss's theorem permits both an arbitrary current fractional point and a coefficient subspace. Every protection family is charged within the codimension budget. Recomputing output eigendirections between partial steps is legitimate because only the step errors, not persistent output constraints, are accumulated.
- **Positivity and final size.** All inner-step bounds use the positive full measure at the start of the outer round. Frozen fractional entries remain in every invariant. Exact cardinality halves full-copy counts. Executed masses satisfy the geometric sums `sum eta<=2/m0` and `sum sqrt(eta)<=4/sqrt(m0)`, closing matrix induction and total relative error. Initial downward rounding is uniformly controlled. The baseline preliminary reduction removes logarithmic dependence on original row count/dimension, and positive weight composition preserves original indices. Zero optimum is treated in linear-form coordinates and then transferred to Euclidean residual maps, including zero-cost queries.
- **Lower bounds and matching.** Checked the fixed-rank auxiliary query geometry, polynomial derivative extraction, stable evaluation and support conversion for arbitrarily many auxiliary coordinates. Separately checked the variable-density core's probability estimates, the Haar-basis net argument with independence only between complete bases, entire-group orthogonality and density optimization. Combining its capped three-branch lower bound with the uncapped high-accuracy lower bound yields the precise even rate, including both breakpoint regimes.

## Primary dependencies checked independently

Opened and read the relevant original statements on 14 September 2026:

- [Lin--Mirrokni--Woodruff, arXiv:2608.26047v2, Theorem 1.2](https://arxiv.org/html/2608.26047v2): the imported upper bound uses original sampled/reweighted rows and applies to every rank-at-most-`k` subspace, with the displayed logarithmic exponent `p+5` and arbitrary input matrices. A fixed positive success probability supplies existence.
- [Marcus--Spielman--Srivastava, arXiv:1712.07766, Theorem 1.1](https://arxiv.org/html/1712.07766): the stated Spielman--Srivastava selected-column inequality uses stable rank, allows arbitrary column lengths and bounds the least singular value on the full selected coefficient space.
- [Rothvoss, arXiv:1404.0339, Lemma 9, printed page 8](https://arxiv.org/pdf/1404.0339): the hypotheses include a high-dimensional coefficient subspace, a symmetric convex body with enough Gaussian measure, and an arbitrary starting point in the open cube. Fixed choices give the constant-fraction saturation statement used in Part II; the lower threshold can absorb the Gaussian-measure requirement for the finitely many small coordinate counts.
- [Tropp, arXiv:1004.4389v7, Theorem 1.5](https://arxiv.org/html/1004.4389v7): the rectangular Gaussian bound has the maximum of the two matrix variances and the sum-of-dimensions prefactor. Restricted Gaussians are first expressed in an orthonormal coefficient basis, so independence is not assumed incorrectly.
- [Li--Wang--Woodruff, arXiv:1904.05543v3, Section 3.1](https://arxiv.org/html/1904.05543v3): Lemmas 3.1--3.3 and Corollary 3.4 support the explicitly credited antecedent for the middle Walsh spectrum. Part I supplies its own estimates and support reduction; it does not substitute the earlier bit-complexity lower bound for an original-row support bound.

The imported theorems are not re-proved by this review. No novelty or first-discovery priority was certified.

## Fresh reproduction and negative controls

All executable code was read before use. Ran only in disposable copies under `/private/tmp/nla-review-253-256/pr253-ra05`, using scientific Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and mpmath 1.3.0. The archived even ZIP was checked for traversal paths and symlinks before extraction.

- New submission manifest: all **26** file hashes matched.
- Cubic certificate: **17,575** exact integer/rational assertions passed. Its finite universal conclusion is `m>=204-548592 epsilon^2`, implying support at least 150 at accuracy `1/100` and all 204 rows at `1/1000`.
- Non-even diagnostic suite: **240** assertions passed, including all 75-decimal-digit Fourier-integral comparisons near even powers. The largest scaled numerical residual was `1.592e-15`. This suite was unavailable to the submitted reviewer but is freshly rerun here.
- Included all-even package: all **22** manifest hashes matched; **87,932** diagnostic assertions and **135** separate exact-certificate assertions passed. The largest scaled residual/PSD violation on this environment was `4.377e-14`, within its explicit tolerances. This environment-dependent residual differs slightly from the author's saved value without changing any assertion outcome.
- Independent additional checker: **1,552** assertions passed, including one full exact array comparison covering all **626,688** cubic tensor query/row pairs; an independently recomputed squared-cost sum; direct block projector/residual calculations at fixed ranks 1, 2 and 4 with auxiliary sizes 1, 3 and 17; non-even exponents as close as `2.0001` and `4.0001`; rational derivative extraction through degree 32; and the complete even lower-bound combination over a rational exponent grid. Three deliberately corrupted certificates (negative LDL pivot, altered core vector, incorrect support coefficient) were rejected. Maximum scaled residual was `3.141e-16`.

The scratch block checker initially encountered a tiny negative floating-point representation of an exact zero residual at a one-vector block. It was corrected to assert nonnegativity within `1e-14` before clamping that roundoff to zero; this was a diagnostic implementation issue, not a failed manuscript assertion.

Machine-readable fresh evidence:

- `pr253-ra05/exact-rerun.json`
- `pr253-ra05/non-even-rerun.json`
- `pr253-ra05/even-manifest-rerun.json`
- `pr253-ra05/even-rerun.json`
- `pr253-ra05/even-exact-rerun.json`
- `pr253-ra05/adversarial_review.py` and `adversarial-rerun.json`
- `pr253-ra05/reviewed-source-sha256.json`

The finite checks do not certify asymptotic existence, implement the partial-coloring oracle, prove the uniform Gaussian norming theorem, or formalize the imported results. In particular, the large assertion totals largely count repeated bookkeeping or array entries, not independent theorem proofs.

## Source preservation and PDF review

Both published mathematical bodies, from their first section onward, are byte-identical to their corresponding submitted TeX originals. The added publication covers and bylines do not change the proof bodies. SHA-256 values for the reviewed published sources are:

- `part-1.tex`: `6cc00d4e27c20529eb95a406313bb19fbaee5049bda2febca3d88ec5e3673712`
- `part-2.tex`: `911fe25ca20da6f3f3b05686d5d646f7aa0604a4488e3b368cdefeff73ef1175`
- combined `manuscript.pdf`: `d3d26a9e295f6eb80a57a8399469fb161a3bf4b86efb4741c464743bb09929ed`

Applied the PDF skill in read-only mode. Rasterized all **44 combined-manuscript pages and all 3 canonical problem pages** with Poppler at 1,600-pixel long-edge resolution and visually inspected every page. The new result, quantifiers, exponent formulas, attribution, historical-scope notices, original problem and mathematical symbols are legible. No clipped formulas, overlapping text, missing glyphs or actionable layout defect was found. No PDF was regenerated or edited.

The canonical prose about the optional numerical suite being unavailable accurately describes the earlier submitted audit; this fresh audit adds successful numerical reproduction and can be linked by the integration record. No mathematics or status correction is needed on this basis.

**Recommendation:** accept the RA-05 portion at the reviewed exact head, including the Solved transition, subject to the coordinator's full PR/integration checks. No actionable inline findings are proposed.
