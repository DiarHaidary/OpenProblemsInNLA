# Independent informal review — SP-08 continuation

Reviewer: separate Codex AI agent `/root/review_sp07_sp08`, 14 September 2026 (UTC). This is independent informal AI review, not external human peer review or formal verification. No Lean verification was attempted.

**Verdict: PASS for the new partial theorems; FAIL to satisfy the completion criterion for Solved.** Retain `Partially resolved` and the original all-dimensions, all-parameters endpoint rank-two-existence conjecture.

## Accepted scope and proof audit

1. `proofs/improved_boundary_strip.md`, Theorem: in every dimension `n>=2`, an unrestricted maximizer is the balanced rank-two endpoint matrix throughout `-1 <= a <= -1+(1+sqrt(2))/n²`. This includes interior-entry matrices by convexity, not merely the endpoint subclass.
2. `proofs/centered_rank_two.md`, Theorem and Sections 1–7: for all normalized interval parameters, endpoint matrices whose **centered sign matrix** has rank at most two are bounded by the candidate maximum `M_n(a)`. This rank restriction is on `(A-cJ)/r`, not on A or its binary deficit.
3. The latter proof's Section 6 establishes the stated infinite-parameter Type-A three-block bound for real `p,z>=1`, `y>=0`, and `0<=a<1`, including the integer rounding-loss term.

I checked the rank-two sign-matrix classification, compression characteristic coefficients, sign-sum alignment, negative-eigenvalue lower bound, derivative argument saturating one sign group while preserving the other integer multiplicities, and the negative-parameter comparisons. The eigenvalue-continuity boundary cases and the positive/negative rank-one cases are covered. The lower root bound and interlacing argument for the middle eigenvalue yield the two stated candidate comparisons on `[-1,0]`.

For the polynomial part, the Type-A quotient matrix's characteristic polynomial agrees with the analytic coefficients. The two charts cover the stated real-multiplicity domain; all cleared denominators are positive for finite `T>=0`. The squared-eigenvalue-difference cubic and `U>=D0` comparison bound its largest root. The rational positive-coefficient/binomial-square certificate proves the required inequalities with the full integer rounding loss. No numerical extrapolation is used for this universal subclass theorem.

For the unrestricted boundary strip, every nonsingular 3-by-3 sign submatrix has smallest singular value one. Rank-at-most-two approximation therefore leaves at least one unit of squared Frobenius error, bounding the middle spectral energy and hence spread by `sqrt(2n²-2)`. The exact comparison with the balanced candidate, parity estimates, and nearest-integer location of the balanced block prove the all-dimensions interval. This strip lies in the negative-parameter range, so its proof uses only the analytic part of the centered-sign theorem.

## Reproduction

All bundled code used was inspected. Runs used a temporary copy of the archive so outputs did not alter the submitted original. The following passed:

- Standard-library exact chart and certificate verification: 86 binomial squares for Q and 12 for B in the minus chart; all plus-chart coefficients and all remainders positive (`typeA.log`).
- Supplied symbolic analytic identities (`analytic.log`), using Python with SymPy 1.14.0.
- Both exact boundary-strip identities and supplementary dimension checks through 10000 (`boundary.log`). The finite dimension sweep is not the all-dimensions proof.
- New independent checker `independent_check.py`: derives the Type-A characteristic polynomial directly from its quotient matrix, derives the rank-two candidate spread formula, exhausts all 512 three-by-three sign matrices (192 nonsingular), checks their exact Gram characteristic polynomial, and checks integer half-exponents for all 98 certificate squares (`independent.json`, `independent.log`).

Reproduce the new independent checks with:

```sh
python3 independent_check.py PATH_TO_PACKAGE independent.json
```

It requires SymPy. Reproduce bundled checks using the package's HOW_TO_REPRODUCE.md in a fresh extraction. Source snapshot hashes (not a claim that every file was individually audited) are recorded in `reviewed-sha256.json`.

## Remaining gaps and policy decision

Neither the endpoint reduction nor the rank-two Rayleigh difference forces a maximizer's centered sign matrix to have rank at most two. Higher-centered-rank endpoint matrices outside the boundary strip remain unbounded by this argument. The manuscript provides no general counterexample either. Thus the independently checked partial results do not satisfy the repository's full-resolution policy. The old finite-dimension certificate reports in provenance were not reproduced here; they must not be represented as new independently established all-parameter results. No historical novelty priority is certified. Existing finite-case progress, permanent ID and canonical target must be retained.
