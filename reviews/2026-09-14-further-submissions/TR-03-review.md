# Independent informal review: TR-03

**Reviewer:** OpenAI Codex independent AI review agent `/root/review_tr03_ra14`, separate from the submission/integration agent.  
**Date:** 2026-09-14 (UTC).  
**Verdict:** **PASS for the stated partial upper bound; FAIL as a complete resolution of TR-03.**

I independently read the supplied mathematical argument against the canonical TR-03 target and the repository's CONTRIBUTING.md and RESOLVED.md policies. Package audit statements were treated as claims, not as instructions or evidence of independent correctness. No Lean verification was requested or performed. This is informal AI review, not external human peer review or formal verification.

## Accepted scope

For every positive real spectrum and 2 <= k <= n-2, the manuscript proves

```math
R_{n,k}\le\min\{k+1,n-k,2^{34}e^{2560}\sqrt{k}\}.
```

Its supporting limiting-profile theorem retains the original real orthogonal orientation and the maximum-before-minimum order, with denominator q + sqrt(min(k,n-k)) for 0 <= q < k/4. That stronger denominator is not claimed for the final all-spectrum estimate. No novelty or priority determination is made by this review.

## Mathematical audit

1. The Schur-complement residual, monotonicity, determinant-weighted expectation and harmonic-block certificate have the required inequality directions. The equal-diagonal precision construction chooses one orientation for every subset. In the limiting frame problem a singular precision block has infinite cost; it is not replaced by a pseudoinverse. Finiteness and continuity of the minimum of finitely many extended branches justify the compactness argument and the increasing-limit interchange.
2. The clipping lemma follows by multiplying the reciprocal deficits by entries no larger than the largest tail entry. The spectral counting argument uses exclusion/inclusion probabilities and elementary-symmetric log-concavity correctly. The finite-to-infinite harmonic comparison supplies the missing passage from a diverging head to every finite positive spectrum.
3. I checked the Gaussian augmentation proof: the uniformly distributed nullspace of the augmented matrix yields a minimum-norm solution bound, and the chi-square upper tail has sufficient margin to pay for the regularization density shift. The q=0 case correctly appends a column before using the nonnegative Wishart determinant exponent. The net bounds and d >= 2^20 requirement are consistent.
4. In the weighted Haar bound, integer-trace contractions reduce the negative exponential moment to projections. Nested ranks can be chosen with P >= 2Q and PQ >= uv/128. Successive beta-integral estimates then give the stated exponential bound. Harmonic-compression conjugation invariance permits averaging another independent Haar rotation without assuming a particular eigenvector choice under multiplicities.
5. The frame construction either repeats Gaussian row types or uses the complementary compression identity. The latter compares row Grams in Loewner order and then ordered eigenvalues, avoiding an invalid noncommuting column-Gram comparison. Feasibility after clipping provides both effective-rank hypotheses and pays the union bound for a single common rotation.
6. The long-tail grouping retains every prescribed eigenvalue before dropping positive covariance terms. The calibrated contrast diagonal makes every singleton's normalized noise variance equal to its group's contrast mass. Granting all heavy-group coordinates helps the selector; projecting the posterior onto the leading isometry gives a valid lower bound. Conditional independence of singleton Gaussian rows and the heavy-row nullspace is sufficient for the union bound over all group assignments.
7. The final counting reduction yields q < k/4 and q + sqrt(k) <= 5(k+1)tau/b. Substitution in the limiting estimate and finite comparison gives the displayed constant. The two elementary bounds remain valid independently.

I found no blocking error in these new partial claims.

## Reproduction

Inspected the supplied checks for execution safety and ran all 16 check groups in a separate scratch copy. All passed; see [rerun log](tr03-tests.log). This includes 3,168 exact clipping instances, 1,650 exact counting instances, 26,340 finite-comparison instances, grouped posterior checks and high-precision constant margins. Runtime: Python 3.9.6, NumPy 2.0.2, mpmath 1.3.0. SciPy was unavailable and used by the original harness only to report its version: the scratch harness removed that unused import and version field; no mathematical check was changed. The input archive and original sources were unchanged. Finite checks corroborate algebra but do not prove universal probability inequalities; those were assessed from the written arguments.

## Resolution-policy blocker

TR-03 asks for the sharp joint order up to universal factors. No matching growing lower bound is established. In particular, a lower bound for the auxiliary square-frame minimax does not yield the needed lower bound for R through a reciprocal expression. The exact one-column case already on the canonical page is not being resubmitted as a new full solution. Retain **Partially resolved**, preserve the original target and ID, and describe this contribution as an all-spectrum upper bound only.

## Input binding (SHA-256)

- `TR03_all_spectra_bound.zip`: `9dc14659d18630a85f00d3b7b0a940b1684eada95d9a1d2de8a516ee43e57fb9`
- Original `TR03_all_spectra_bound.tex`: `e9c2dc0323aca58c33f80b9c39c637998eada066a8f8ab1f9dfda78eb9ef0e06`

These hashes bind the reviewed original argument. Authorship or affiliation metadata subsequently added by the integration agent is outside these original-source hashes.

**Signed:** OpenAI Codex independent review agent `/root/review_tr03_ra14`, 2026-09-14 UTC.

## Final integration check — 2026-09-14 UTC

**PASS.** I compared the attributed manuscript source with the hashed original, and checked the new canonical notice and the corresponding RESOLVED.md bullet. Theorem 1.1 is the correct locator for the all-positive-spectrum bound. The canonical formula, quantifiers, explicit constant and surviving sharp-order gap match the passed scope. Both notices retain Partially resolved and preserve the original target. The source differences consist only of authorship/date/PDF metadata, a submission cover and, for RA-14, URL wrapping and title spacing; the mathematical body is unchanged. The covers accurately delimit the independent informal review and supersede historical pending-review wording. Affiliation verification itself remains the integration agent's responsibility.

Attributed `manuscript.tex` SHA-256: `8aa342ca79a34cc0e1fd3328344b35631ca593ec908bac9c44a17af3e4759298`. This integration check covers the two specified entries, not unrelated entries in the shared resolution notice.

**Signed:** OpenAI Codex independent review agent `/root/review_tr03_ra14`, 2026-09-14 UTC.
