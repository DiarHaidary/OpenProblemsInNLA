# Independent review: PR #247, RA-05 even-power continuation

Reviewed head `24212f477b26aad36a757e62998bd4974b24ac81` against base `752218e5417998b7f4d2aee9c447ca5d256fe530`, in `/private/tmp/nla-audit-247`. Review date: 2026-09-13. Reviewer: separate Codex audit agent, without relying on the submitted PASS report.

**Conclusion: no actionable mathematical or presentation finding identified for the stated further partial resolution.** The manuscript supports the all-accuracy upper bound and matching high-accuracy classification for every fixed even exponent `p=2s>=4`, with arbitrary input rank and ambient dimension and nonnegative weights on original rows. It does not resolve the original all-real-exponent/all-accuracy RA-05 target. This is informal AI-assisted mathematical review, not external human peer review or formal verification.

## Scope and target preservation

Read the complete 829-line submitted manuscript, its auxiliary source/dependency/status/audit documents, all four Python files and execution wrappers, the canonical README/TeX changes, and the RESOLVED addition. Compared the original and submitted manuscript sources: only authorship, affiliation, assistance wording and PDF-author metadata differ. No mathematics was altered during submission preparation.

The canonical additions retain status **Partially resolved**, give the correct condition `0<epsilon<1/2` and `epsilon<=k^(-(s+1)/2)`, retain the original question, and leave earlier quartic and all-exponent lower-bound credit intact. The supplied nested prior archive contains the stated rank-restricted comparison bound; I checked its corresponding theorem statement rather than treating that comparison as an input to the new proofs. PR #199 and PR #222 remain separately credited. No identifier/path is renamed in this diff. Repository-wide ID/catalog/CI checks belong to the coordinator's integration review.

The new bounds are

- `S_{2s}(k,epsilon) <= C_s (k^((3s-1)/2)/epsilon + k^(s-1)/epsilon^2) log^5(2k/epsilon)`;
- `S_{2s}(k,epsilon) >= c_s k^(s-1)/epsilon^2`.

The first upper term is dominated by the second precisely when `epsilon<=k^(-(s+1)/2)`. Constants depend only on fixed `s`. The separate `k^s/epsilon^2` baseline and illustrative `p=6` intermediate-accuracy gaps are reported consistently. No efficient implementation is claimed.

## Upper-proof audit

1. **Ambient/query model.** Compressing any ambient orthogonal projector to the row span gives a positive contraction of rank at most `k`; `a^T(I-P)a` is the original squared residual. Preserving all such contractions therefore covers the required queries. The optimum and head-spanning argument handle arbitrary rank above `k`; the separate zero-optimum branch handles ranks at most `k` and zero input.
2. **Normalization and sensitivity.** Verified the determinant-one minimization argument for Lewis isotropy, its moment inequalities, Gaussian transfer to vector-valued residuals, `H(P)<=C_s cost(P)`, and fixed distributions `omega` and `pi`. Every feature carries `sqrt(omega)`, and a density mass `mu_i` returns original-row weight `mu_i/pi_i`. Initial downward rounding loses at most the asserted uniform relative budget by the `C_s k^s` sensitivity bound.
3. **Features and every monomial.** Verified isotropy/trace on positive ranges, mixed covariance domination, leverage controls, and zero-tail handling. The six cases exhaust `(A+2X+r^2-R)^s`. For protected terms, the maps have a common vector output for odd `l`; the trace/nuclear bound correctly uses Hilbert--Schmidt norms and does not assert a false scalar rank-one query. The degree identities, map norms and rank bookkeeping give `(3s-1)/2`, including the worst protected monomial `a=s-1,b=1`.
4. **Gaussian bounds.** Coefficient-space projection contracts both rectangular variances. Right normalization by `(B+aI)^(-1/2)` controls both normalized variances, including restricted active subsets. Protecting `q` right directions is correctly charged `D_l*q` scalar equations; the protected space is fixed for an entire outer round. Balanced and one-cross terms use the appropriate distinct estimates. In particular, the anisotropic query bound uses a maintained trace invariant, while the recombined pure-tail class uses Lipschitz Gaussian increment comparison and the Frobenius bound `sqrt(k)`.
5. **Partial coloring and induction.** Radial spectral truncation uses covariance trace divided by the number of protected eigendirections. The arbitrary-center subspace coloring theorem applies at each fractional point. All good events are symmetric convex seminorm bounds, and their fixed finite intersection has enough Gaussian measure. The argument uses pre-round positive measures for all inner-step bounds and does not silently assume temporary fractional states obey new covariance invariants.
6. **Positivity, accumulation and output support.** Exact cardinality preserves total density mass, full positive copies halve in number, and strictly fractional entries are permanently frozen with positive weights. Frozen entries remain in all full-measure invariants. The executed masses double and obey the geometric prefix sums, closing covariance induction and the cumulative relative-error bound. At most `O(m_0 L)` entries survive before merging original indices, giving the fifth logarithmic power. The preliminary baseline reduction removes dependence on original row count/dimension from all logarithms. Positive weight composition preserves original indices.
7. **Low-rank branch.** Its radial-only linear-form argument and independent Gaussian averaging transfer to all Euclidean residual maps, including zero-cost queries. Undoing Lewis normalization is correctly done in the linear-form domain.

## Lower-proof audit

The Gaussian `2->2s` comparison, radial lower tail and spherical moment estimate give the random core's moment control. The off-diagonal smoothed-kernel estimate implies a positive-probability Frobenius event; spectral truncation leaves at least `3L/4` eigenvalues in `[1/2,3/2]`. The imported restricted-invertibility theorem then selects actual input columns with squared least singular value at least `3/64`.

The auxiliary-dimensional construction keeps query rank exactly `r`, independently of `N`. I derived its residual expression directly from its projector and checked the `0<=D<=2D_0` bound. Multiplying the cost error by `(1+t^2)^s` produces a degree-at-most-`2s` polynomial; interpolation at fixed real nodes gives the derivative bound without assuming nonnegative weights. The stable evaluation kernel controls all group-mean coordinates. The zero-subspace mass bound and Cauchy--Schwarz give `m>=c_s M/(r epsilon^2+1/N)`. Choosing `N=ceil((r epsilon^2)^(-1))` is valid even when that expression is below one, and produces the uncapped large-rank bound.

The separate small-rank block construction uses nonnegativity, forces positive mass in every group, and applies the two tilted subspaces simultaneously. Its residual formulas, power-difference estimates and convexity step yield an `Omega_s(k/epsilon^2)` bound, sufficient for the finitely many excluded ranks after adjusting the fixed-`s` constant. The signed extension is appropriately limited to sufficiently large ranks.

## Primary dependencies checked

Read the actual relevant theorem statements, not merely the manuscript's source list:

- [Lin--Mirrokni--Woodruff, arXiv:2608.26047v2, Theorem 1.2](https://arxiv.org/html/2608.26047v2): nonnegative sampled/rescaled original rows, all rank-at-most-`k` subspaces, size `C_p k^(p/2) epsilon^-2 log^(p+5)(C_p k/(epsilon delta))`. This supplies the preliminary reduction at a fixed failure probability.
- [Rothvoss, arXiv:1404.0339, Lemma 9, printed page 8](https://arxiv.org/pdf/1404.0339): both coefficient subspace and arbitrary fractional center are in the statement. I also inspected the cached raster of that exact page to confirm the `3/2` codimension coefficient and `epsilon/2` saturation fraction.
- [Tropp, arXiv:1004.4389v7, Theorem 1.5](https://arxiv.org/html/1004.4389v7): rectangular Gaussian series with the maximum of left and right variance and prefactor `d_1+d_2`.
- [Marcus--Spielman--Srivastava, arXiv:1712.07766, Theorem 1.1](https://arxiv.org/html/1712.07766): the stated Spielman--Srivastava stable-rank selection bound has no unit-column restriction.

These are imported results, not re-proved or formally certified by this review.

## Reproduction and adversarial checks

All submitted executable code was read before execution. Executed only from the disposable copy `/private/tmp/nla247-rerun`; no source checkout or GitHub state was mutated.

Commands:

```text
/private/tmp/nla-batch-python/bin/python /private/tmp/nla247-rerun/code/check_manifest.py
/private/tmp/nla-batch-python/bin/python /private/tmp/nla247-rerun/code/verify.py
/private/tmp/nla-batch-python/bin/python /private/tmp/nla247-rerun/code/check_exact_certificate.py
/private/tmp/nla-batch-python/bin/python /private/tmp/nla247-rerun/adversarial_review.py
```

Results:

- Final manifest: all 25 listed files matched before regeneration.
- Submitted suite: **8,453 assertions passed**, with category counts matching the submitted report. Largest scaled numerical residual was approximately `1.645e-14`.
- Exact certificate: the 12-row, input-rank-8, query-rank-2, six-retained-row example passed at `p=4,6,8,10,12`. Recreated certificate and exact-check JSON files were byte-identical to those submitted. Independently inspected the covariance/Jensen optimal-head proof.
- Additional scratch diagnostics: **3,490 assertions passed**, seed `98724471`; maximum scaled residual approximately `2.868e-12`. These include direct high-ambient-dimensional query/projector/residual calculations (`N` as large as 31), exact symbolic derivative and polynomial-degree identities for `s=2,...,12`, and singular-range/zero-head/zero-tail/all-zero-tail feature cases with projector ranks 0, 1 and `k`. The latter exercise the supplied feature library; the direct geometry and symbolic identities are independent constructions.
- Scratch extra checker and machine-readable result: `/private/tmp/nla247-rerun/adversarial_review.py` and `.json`.
- Source checkout remained clean after review.

The assertion counts are finite diagnostics, not counts of independent proofs. No finite check implements or certifies the partial-coloring oracle, asymptotic random-core thresholds or universal restricted-invertibility conclusion.

## PDF inspection

Read the PDF skill in read-only mode; did not rebuild or edit PDFs. Rasterized and visually inspected **all 21 manuscript pages and all 3 canonical problem pages** with Poppler at 1400-pixel long-edge resolution. Renderings are in `/private/tmp/nla247-raster`. Verified the displayed exponents, residual formulas, matrix norms, table entries, citations and retained original target; no clipping, missing mathematical glyphs, overlapping text or actionable layout defect was observed. Title/contents pagination and canonical status are coherent. Source-level review, rather than raster inspection alone, checked every proof formula.

## Limits and recommendation

Suitable to accept for the explicitly stated **further partial** scope, subject to the coordinator's independent integration/CI review. Do not promote RA-05 to fully solved on the strength of this PR. Novelty, priority and external human peer-review status were not certified. No Lean or other proof-assistant verification was performed. No actionable inline comments are proposed.
