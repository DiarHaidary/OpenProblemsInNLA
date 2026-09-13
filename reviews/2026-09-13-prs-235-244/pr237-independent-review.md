# Independent audit: PR #237 (RA-01)

**Verdict: PASS for the stated partial results. No actionable mathematical or publication blocker found.** The universal RA-01 assertion remains open. This is an independent informal AI-agent audit, not external human peer review or formal verification.

Reviewed exact head `84782ad6087d142baa2fd4e751670d57cdfd59d1` against published base `b73cd1804e40e0d101294eedb156984f0d62b4a6`, in `/private/tmp/nla-audit-237`. Read the full 537-line attributed manuscript, original manuscript comparison, all four verification/engine files, canonical diff, provenance and review records. All 26 added/changed PDF pages were visually inspected: 12 attributed report, 12 retained original, and 2 canonical. No source-worktree edits or GitHub mutations were made; the source worktree remains clean.

## Claim coverage and proof assessment

The canonical target from `Context and notation` onward is byte-identical to base. Its original complex Hermitian PSD domain, adaptive diagonal-residual pivot law, expected relative trace error, all ranks/tolerances, dimension cap, references and old audit are preserved. Sections 1–8 and bibliography of the attributed TeX are unchanged from the original submitted manuscript. Only author/date metadata and disclosure prose change.

Theorem 4.1 establishes C=3 when `lambda_(r+j) <= lambda_(r+1) 2^(-(j-1))`; Theorem 5.1 establishes C=4 for the corresponding inverse-square tail; Theorem 6.1 establishes finite C_p for a fixed p>1. Head eigenvalues and complex eigenvectors remain unrestricted. These assumptions start after r and are normalized at the first tail eigenvalue, so global power-law decay does not automatically qualify. None gives one constant for every spectrum.

The proof details were independently checked as follows:

- PSD order and exact rank reduction give termination and both tail inequalities. The averaged trace drift is correct for complex Hermitian residuals. The scalar map is nondecreasing and concave at and across the join; its reciprocal recurrence gives the claimed completion count.
- The rank-one start and recurrence are valid. The rank-two doubling argument covers zero diagonal projection `c_j=0`: a leading eigenvector plus tail subspace has trial trace at most `tau+lambda_1`, whose probability-weighted excess is at most `lambda_1 b_j/T`. For positive c_j the displayed trial-space calculation gives the same bound after weighting. Summing yields the needed factor two. The rounded scalar chain and `89/56 < 8/5` check out.
- Ordered-path probability is a principal determinant divided by preceding traces. On the bad event, the first r denominators exceed original spectral tails, the remaining m exceed the final trace. Summation over at most k! orders and integration of `min(1,M v^-m)` give Proposition 3.1. Terminated paths produce no missing bad events. The head-product bound removes head magnitudes without invoking unitary invariance of the pivot law.
- The geometric coefficient product and uniform lower bound are valid. The factorial induction gives the `8/5` warm start at `3r+1`; its base and successive-ratio bounds and final ceiling calculation support C=3, including small ranks.
- The hyperbolic-sine product yields the inverse-square coefficients. The factorial induction, special r=3 transition, and warm-start completion support C=4. Active dimension caps and zero tails terminate exactly.
- For fixed p>1, the decreasing-integrand sum-to-integral comparison is valid, and coefficient optimization gives the displayed K_p. Choosing c at least `1/(p-1)` removes rank growth. The displayed finite C_p supplies both starting and completion pivots. Its dependence on p cannot be removed by choosing an input-dependent exponent.
- The spike Schur complement gives the deterministic holding rates. The rate-two post-first-pivot bound and rate lower bound imply the generator/Jensen inequality and logarithmic count correction. The finite t,n choices disprove only affine count bounds with unit tail-rate coefficient (or smaller), not bounds with both coefficients greater than one and not the discrete RA-01 target.
- The saturation limit takes head scale to infinity first, then tail count, yielding k!/m!. The diverging root is a limitation of this upper comparison, not an algorithmic error lower bound. The final unrestricted warm-start equivalence is valid and remains explicitly unproved.

## Primary-source verification

- [Chen–Epperly–Tropp–Webber, v6](https://arxiv.org/html/2207.06503v6): Algorithm 1 and Lemma 5.5 support the original pivot law and error-doubling ingredient.
- [Epperly, v1](https://arxiv.org/html/2608.20633v1): Corollary 1.3 and the conjecture after (1.5) support the retained unrestricted target and the extra rank-dependent term in known bounds.
- [Divan–Gilles, v1](https://arxiv.org/html/2609.06287v1): Theorem 3.1, Lemma 3.2 and Corollary 3.3 confirm the elementary-symmetric-polynomial method and decay assumptions on the full spectrum. The submission clearly states its additional tail-normalized scope and preserves attribution.
- [NIST DLMF 4.36.1](https://dlmf.nist.gov/4.36.E1): the sinh product has the normalization used in Theorem 5.1.
- [Official Sidney Holden profile](https://www.simonsfoundation.org/people/sidney-holden/) supports the CCB/Flatiron affiliation, without establishing authorship or endorsement.

## Reproduction and independent checks

After reading source, copied `submitted/` to `/private/tmp/nla-review-237-run` and ran with `/private/tmp/nla-batch-python/bin/python`:

- `code/verify_manifest.py`: PASS, 18 payload files match; the manifest itself is the 19th retained file.
- `code/verify_exact.py`: PASS, 8 matrix cases and 8,500 explicit exact checks. The rational engine exercises actual pivot probabilities, order independence, trace drift, spectral/path inequalities, coefficients, scalar constants, and finite clock/saturation certificates.
- `code/verify_floating.py`: PASS, 2 exhaustive order-11 cases and 1,200 Monte Carlo trajectories over six real/complex cases. Logs: `/private/tmp/nla-237-exact.log`, `/private/tmp/nla-237-floating.log`; JSON is in the scratch `verification/` directory.
- Independently authored Gaussian-rational arithmetic and exact complex RPCholesky enumeration imported no submitted code. New dense genuinely complex Hermitian cases had (n,r)=(5,1) and (8,2), with phase-rotated rational Householder eigenvectors and geometric tails. All paths merged exactly, probabilities normalized, trace identities held, and every realized strict-event threshold met the determinant probability bound. The two runs checked 105 and 1,242 transitions/event thresholds respectively and verified non-capped `3r+1` warm starts. Evidence: `/private/tmp/nla-independent-235-237.py`, `/private/tmp/nla-237-adversarial.json`.
- Visual inspection of all 26 pages found readable equations, labels, tables, references and disclosures, with no clipping or overlap. The renderer change adds only RA-01 to the existing PDF page-break set; the original target is intact on canonical page two. Root review handles renderer tests and shared integration.

## Limits

The finite rational and floating suites do not prove the analytic inequalities in all dimensions. Previous nested ZIP manuscripts and their separate claimed universal lower bound were not newly audited; the present accepted partial results do not depend on those claims. No complete-resolution, historical novelty, or Lean-verification claim is warranted. This review supports **Partially resolved**, preserving the unrestricted question and original permanent ID/path. Root review covers registry/catalog/CI and batch merge interactions.
