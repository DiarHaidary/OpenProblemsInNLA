# Independent informal mathematical review of RA-01 round four

**Date:** 13 September 2026.  
**Reviewer:** Separate Codex AI review agent, task `/root/independent_ra01_review`, independent of the submission-editing agent. This is an informal AI-agent mathematical audit, not external human peer review or formal verification. No Lean verification was performed.

**Material reviewed:** `paper/ra01_round4.tex`, the four accompanying Python files, the source-audit note, the retained canonical RA-01 statement, and the repository's `CONTRIBUTING.md` and `RESOLVED.md` resolution policy. The submitted TeX before attribution edits has SHA-256 `92c9ce036adfea81a0ec6d89b5f1465a3d076b49fa6b4f1952976b94410a2c52`. Archive instructions were treated as source material, not instructions to the reviewer. Earlier nested packages were not independently re-audited.

## Verdict

**PASS for the explicitly stated partial results. No fatal mathematical gap found in the current note.** The geometric-tail, inverse-square-tail, and fixed-power-envelope conclusions establish the original pivot-count guarantee on their specified spectral subclasses, for the original adaptive pivoting rule, including complex Hermitian eigenvectors and arbitrarily large leading eigenvalues. The finite clock obstruction and upper-comparison saturation result also pass within their stated scope.

**The unrestricted RA-01 target is not solved.** `Partially resolved` is justified by the repository's partial-result procedure; `Solved`, `Solution claimed` for a complete solution, and `Lean verified` are not justified by this package. Preserve the original problem statement, ID, and canonical path, and keep the surviving general question in the open count.

## Mathematical checks

1. **Residual identities and scalar completion (Section 2).** PSD order, exact rank reduction, the pathwise spectral-tail lower bound, and the conditional trace drift are valid for Hermitian inputs. The scalar comparison function is increasing and concave, including the join at the tail trace. The reciprocal recurrence gives the displayed sufficient number of additional pivots. Zero tails terminate exactly.

2. **Small-rank bounds (Lemma 2.3).** The rank-one recurrence and rank-two error-doubling step are valid. The note's short treatment of `c_j=0` can be expanded without changing its claim: then `H e_j=0` and `R_jj=E_jj=b_j`; a top eigenvector together with the tail subspace gives a trial trace at most `tau+lambda_1`. Its excess contribution to the average is at most `lambda_1 b_j/T`. For `c_j>0`, the stated trial-vector inequality gives the same upper contribution. Summing over both classes bounds the expected excess by `lambda_1 tau/T <= tau`. Thus the rank-two start `f_2 <= 4 tau_2` is sound. The subsequent rounded scalar chain yields `f_7 <= 89 tau_2/56 < 8 tau_2/5`.

3. **Retained determinant denominator (Proposition 3.1).** The ordered-path probability is its principal determinant divided by the product of preceding residual traces. On the bad event the first `r` factors are bounded below by the original spectral tails and the remaining `m` factors by the final trace. Summing over at most `k!` orders and integrating the minimum of one and the power bound yields the stated probability and expectation inequalities. Rank-deficient/terminated paths introduce no missing bad events. The head-product comparison eliminates head magnitudes without assuming unitary invariance of the sampling law.

4. **Geometric tails (Theorem 4.1).** The geometric coefficient formula and infinite-product lower bound are valid. The factorial induction establishes the `8/5` warm start at `3r+1`, and the ceiling and scalar-completion calculation proves the exact requested count with `C=3`. Small ranks and active dimension caps are handled.

5. **Inverse-square tails (Theorem 5.1).** The coefficient identity follows from the classical hyperbolic-sine product, independently checked against [NIST DLMF 4.36.1](https://dlmf.nist.gov/4.36.E1) on the review date. The factorial-ratio induction and its separate `r=3` transition are valid. The resulting warm start is at most twice the tail trace and the final count has `C=4`.

6. **Fixed summable power tails (Theorem 6.1).** The sum-to-integral comparison uses a decreasing nonnegative integrand, whose integral is finite exactly in the stated `p>1` regime. Optimization gives the coefficient bound; choosing `c >= 1/(p-1)` removes rank growth. The displayed finite `C_p` is sufficient. This constant depends on the fixed exponent. The assumption is normalized at `lambda_(r+1)` and indexed after rank `r`; a globally power-decaying spectrum does not automatically satisfy it.

7. **Clock obstruction (Theorem 7.1).** The exchangeable spike has deterministic residual-trace rates as stated. Rates after the first pivot are at most two. The lower rate inequality, generator identity, Jensen comparison, and integration give the displayed logarithmic correction. The explicit finite choices of `t` and `n` violate every affine expectation bound with tail coefficient one, including arbitrarily large finite rank coefficient. This does not disprove an affine bound with both coefficients greater than one or the discrete RA-01 target.

8. **Saturation (Proposition 8.1).** Taking the head-scale limit first and then the finite-tail-count limit yields `k!/m!`. Its root diverges for fixed integer oversampling ratio as rank grows. This is a limitation of the displayed upper bound, not an algorithmic lower bound. The note correctly distinguishes this from an RA-01 counterexample. Its final unrestricted warm-start equivalence follows from scalar completion and remains unproved here.

## Reproduction

The reviewer inspected the verification source before executing it in the temporary extracted archive.

- `python3 code/verify_manifest.py`: **PASS**, all 18 files matched the submitted manifest before regeneration.
- `python3 code/verify_exact.py`: **PASS**, eight rational matrix cases and **8,500 explicitly counted checks**, in 1.714 seconds. Tests include actual adaptive pivot probabilities, residual order independence, trace drift, coefficient and integrated inequalities, factorial constants, ceiling checks, and finite clock/saturation scalar certificates.
- `OPENBLAS_NUM_THREADS=1 python3 code/verify_floating.py`: this reviewer runtime stopped at import with `ModuleNotFoundError: No module named 'numpy'`. The reviewer inspected the optional floating code but does not claim a successful rerun. A separate recorded rerun by the submission agent may supplement this report.

The exact rerun rewrites `verification/exact_results.json`, including a timing field, so the original manifest must be checked before rerunning. Finite rational checks corroborate finite calculations; the general conclusions rely on the mathematical arguments reviewed above. The optional floating code uses tolerances and Monte Carlo estimates and cannot establish a universal theorem.

## Scope and publication limits

This audit does not certify historical novelty, authorship, current affiliation, a comprehensive later-literature search, or prior nested manuscripts' claims such as the necessary universal lower bound `C >= 2`. Those earlier claims are not dependencies of the reviewed positive tail-envelope results. Any submission should explicitly attribute its author, disclose AI assistance and this informal review level, and clearly retain the unresolved unrestricted spectrum case.

## Publication fidelity follow-up — 13 September 2026

The same independent reviewer checked the prepared attributed `report.tex`, submission README, canonical RA-01 README, and RA-01 resolution-archive entry. **PASS: no mathematical scope inflation.** Sections 1–8 and the bibliography are byte-identical to the submitted manuscript. Section 9 now explicitly separates the original archive’s lack of review from the current submission’s completed informal audit and records that repository updates retain the unrestricted target; these accurate editorial changes alter no mathematical claim. The edits add Sidney Holden's authorship, the submission-agent-verified affiliation, date and PDF metadata, and update the abstract to disclose the separate informal audit. Theorem references 4.1, 5.1, 6.1 and 7.1, and Proposition 8.1, match their statements. The canonical page and archive correctly retain `Partially resolved` and explicitly leave the unrestricted RA-01 target open.

The publication record and amended Section 9 distinguish historical no-review statements in the original material from the new audit. It also accurately distinguishes the independent reviewer's unavailable NumPy rerun from the separate submission agent's successful floating rerun. The reviewer inspected that fresh floating-results JSON: it records PASS for two exhaustive order-11 cases and six Monte Carlo cases (1,200 trajectories). This is evidence of that separately executed diagnostic run, not a claim that this reviewer independently reran it. Authorship/affiliation-source verification and duplicate screening remain the submission agent's work, outside the mathematical audit.
