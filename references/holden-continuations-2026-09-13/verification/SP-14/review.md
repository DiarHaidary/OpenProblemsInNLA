# Independent informal review of SP-14, round seven

Date: 2026-09-14 UTC (2026-09-13 in the submission's local date).
Reviewer: a separate Codex AI agent, task `/root/review_sp14`, independently delegated by the submitting agent. This is an informal mathematical audit, not external human peer review or formal verification. No Lean verification was performed.

**Verdict: PASS for the stated partial scope; NOT a complete resolution of SP-14.** The original canonical target requires full-sequence weak convergence for every continuous symbol with neither one-sided annular extension. The manuscript proves a canonical subsequence in a specified Jordan-range class and supporting general reductions. Section 7 expressly retains the full-sequence gap. Under CONTRIBUTING.md and RESOLVED.md, SP-14 must remain **Partially resolved**, with its permanent target and ID unchanged.

## Reviewed inputs and provenance

- Submitted archive `sp14_round7_research.zip`: SHA-256 `0de8ff20ea8ea09a9a693bf0984ac71cfbd5f77e3e6b99b8a49448948a3c093e`.
- Original `manuscript/sp14_round7.tex`: SHA-256 `c5b63644743c5ab3d4be0b6c4353323edd6be33bab34dcaf5e2b7df01f3481a4`.
- Original `manuscript/sp14_round7.pdf`: SHA-256 `3acabd550775170b34fa12a5a06c8a121f80f01979089ad647cb4351256860fb`.

I read the canonical SP-14 README, CONTRIBUTING.md, the resolution status policy, the manuscript's arguments, and the relevant check implementation. Archive prose was treated as evidence to evaluate, not as instructions. Computation ran in a separate temporary copy. Authorship/affiliation additions do not alter the reviewed mathematical argument; the hashes above bind this review to the supplied original.

## Analytic scrutiny

1. **Theorem 2.5 (inverse-corner extension test): passed.** The exact bordering identity controls the first inverse row by the sum of subsequent corners, and a uniform inverse bound makes exponential corner decay imply an exponentially decaying nonzero limit row. Passing the row equation to the limit uses square summability and gives the reflected, unconjugated Toeplitz equation with the stated orientation. Lemma 2.4 correctly handles the potential discontinuity of the Riesz projection: multiplying the negative tail by an analytic function yields exponentially decaying nonnegative coefficients, and an H2 radial growth bound excludes poles on the unit circle. For the converse, radial diagonal similarity, constant logarithmic mean of the zero-index core, and the cofactor identity give the strict root-limsup bound. The two-boundary parametrix in Appendix A supplies finite-section stability; the scalar kernel argument is needed and is supplied, so index zero alone is not incorrectly used as invertibility.

2. **Theorem 3.1 and Corollary 3.3 (unit-index determinant and least-singular-value limsups): passed.** The zero-index core is z^{-1}(a-w), with the correct cofactor orientation. Its bulk determinant limit plus the inverse-corner root limsup yields a pointwise limsup, even if infinitely many determinants vanish. Lemma 3.2's finite comparison follows from block inversion and its test vector, including zero corners. Proposition 3.5 retains a determinant of a boundary block at larger winding; it does not claim that entrywise nonextension controls this determinant. The singular-value splitting and cutoff-log argument are valid for fixed winding magnitude.

3. **Lemmas 4.1–4.3 and Theorem 4.4 / Corollary 4.5 (canonical subsequence): passed.** The Schur-basis coupling has exactly the claimed squared transport cost. Truncated logarithmic kernels give local L1 convergence of potentials and an almost-everywhere upper bound. At the single unit-index anchor, the pointwise limsup selects a sequence; the subharmonic maximum principle then propagates equality over that one component. Zero-index stability supplies equality in the other components. This avoids assuming that independent pointwise limsups synchronize over multiple nonzero-index components. Complementary potential equality determines the measure under the stated area-zero or rational-density hypothesis.

4. **Walsh hypothesis independently checked.** The cited primary source, J. L. Walsh, *Approximation by polynomials in the complex domain* (1935), §4, printed p.9 (PDF page 12), states uniform approximation of a continuous function on a Jordan curve enclosing the origin by polynomials in z and 1/z. Translating an interior point to the origin yields rational density on any Jordan curve. The statement imposes neither rectifiability nor zero planar area, so the manuscript's positive-area Jordan extension is supported. Source: https://www.numdam.org/item/MSM_1935__73__1_0.pdf . I checked the source directly, not merely the submitted citation ledger.

5. **Theorem 5.1 and Corollary 5.2 (extension obstruction and subsequential dichotomy): passed.** The radial logarithmic-mean difference is p log r with the correct sign. Since radial similarity preserves every finite eigenvalue multiset, comparison with both symbols produces a nonnegative potential deficit everywhere almost surely and a uniform positive deficit on an interior disk. Integrating the logarithmic kernel gives the stated second-moment identity and factor 2/pi, so every cluster measure has a positive energy deficit when extension exists in the winding direction. Combining this with the Jordan subsequence theorem establishes exactly the subsequential dichotomy, not full convergence.

6. **Examples and limits:** the plateau Fourier coefficients and finite certificate are consistent with direct integration; the residue-class corner zeros explain why an all-order lower bound would be false. The smooth arbitrary-phase construction has summable derivatives and degree-one Jordan range under its stated smallness bounds. Historical claims about earlier rounds were not independently established here and are not needed for the new core results.

No substantive gap was found in these bounded results. This review does not certify historical novelty or exhaust the later literature.

## Reproduction and independent checks

The original manifest was verified successfully (`source-manifest.log`). In a temporary copy I reran `python code/validate.py` with Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, and mpmath 1.3.0. **246/246 supplied checks passed** (`rerun.log`, `rerun-validation.json`). I did not rerun the six nested historical packages; their shipped counts are not claimed as independently rerun here.

I also wrote `independent_checks.py`, importing no submitted module. **200/200 additional finite checks passed** (`independent-checks.json`): complex general-matrix cofactor and row-bordering identities, singular-value comparison bounds, and independent Fourier quadrature of the Schur coupling and its energy cost. These finite checks supplement the analytic review; they do not prove an infinite or universal limit.

To repeat after installing the versions above:

```sh
python code/validate.py
python /path/to/verification/independent_checks.py
```

The first command runs from an extracted package root and regenerates its results; use a disposable copy to preserve the source manifest. The second script is standalone. No modified mathematical source was needed for the checks.

## Recommended canonical summary

Sidney Holden's independently informally audited seventh note proves an inverse-corner criterion for one-sided annular extension and a canonical weakly convergent subsequence for continuous Jordan-range symbols with winding +1 and no inner extension, or winding -1 and no outer extension. The Jordan curve may have positive area. Extension in the winding direction instead forces a positive limiting lower energy deficit. The universal full-sequence convergence conjecture remains unresolved, including the exclusion of noncanonical cluster subsequences under nonextension. Retain **Partially resolved** and do not present this as a full solution.
