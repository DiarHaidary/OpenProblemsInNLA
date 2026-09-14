# SP-09: local amplification invariance and quantitative rigidity

**Status: further partial resolution of SP-09. The universal assertion is not proved or disproved in this archive.**

The new manuscript is [SP09_local_invariance.pdf](SP09_local_invariance.pdf). Its editable LaTeX source is in `new_results/manuscript/`. The complete preceding proof pack is preserved under `prior/`.

## New theorems

Let

    a0 = (1, (4 + 5 i sqrt(3))/13, (-1 + 2 i sqrt(3))/13),
    A0 = diag(a0),  B0 = -A0,  gamma = 27/13.

There exists an open neighborhood of `(a0, -a0)` in `C^3 x C^3` such that independently perturbing all six complex eigenvalues within that neighborhood preserves unitary-orbit distance under every finite amplification. Every amplified minimizer is a tensor repetition of a scalar minimizer, up to changes of basis within spectral subspaces. The scalar minimizer is unique up to left/right diagonal phases. The neighborhood can be chosen so that orbit distance remains strictly below bottleneck eigenvalue matching.

**No numerical radius for this neighborhood is certified.** The theorem is an openness result, not a claim about a specified ball or arbitrary spectral parameters. Splitting all repeated eigenvalues independently in a larger matrix is not covered by the six-scalar-parameter neighborhood.

For the original reference pair, every unitary in dimension `3k` is within

    2,705,974 * sqrt(||A0_k + U A0_k U*||^2 - 27/13)

of a minimizing unitary in **normalized Hilbert–Schmidt norm**, uniformly in `k`. The norm in the residual is the operator norm. The constant is conservative; the theorem does not assert operator-norm closeness to a minimizer.

## The exact proof certificates

The openness proof uses a strictly positive trace sum-of-squares certificate from the prior pack and transports it after checking all compatibility conditions. The unique reference optimality density has positive eigenvalues `5/28` and `23/28` on the two-dimensional top singular space.

A selected 107-by-107 minor of the universal coefficient map is nonzero. With the stated denominator-clearing convention, its exact integer determinant is

    -2^1740 * 3^342 * 5^14 * 7 * 13^215 * 59.

The archive verifies this determinant both by fraction-free integer elimination and by modular arithmetic. The map has rank exactly 107 in 109 real trace coordinates. The mathematical proof identifies its two-dimensional left kernel and proves that the perturbed fixed term lies in its range. Strict Gram positivity then persists.

The quantitative constant is derived from four explicit projection relations, exact rational bounds, polar decomposition, and column-isometry alignment. Its verifier uses no numerical eigenvalue estimate.

## Verify from a clean extraction

Python 3.10 or later and NumPy are sufficient for the new exact checks. The supplied run used Python 3.13.5 and NumPy 2.3.5.

```bash
python -m pip install -r requirements.txt
python -O verify_all.py
```

The combined checker verifies the file hashes, the original certificate and equality classification, the new exact ranks and optimality density, the integer and modular minors, the explicit stability constant, and rejection of deliberately corrupted data. Optional logs can be written outside the archive:

```bash
python -O verify_all.py --report-dir /path/to/check_logs
```

The proof-critical checks use arbitrary-precision integers and fractions. NumPy holds the arrays. The modular vectorized operations have a documented bound preventing 64-bit overflow. `python -O` does not disable the logical checks.

## Additional exploration, separate from the proofs

The archive also retains 32 further fractional-block construction searches in base dimensions 4 and 6. Exact rational block multiplicities realize the recorded constructions at amplification factors no larger than 5. The two small raw positive comparisons already have k = 1 and assemble to base-dimensional witnesses, so neither shows an amplification improvement. After including those base witnesses, no candidate gap exceeds 1e-8. The saved unitary matrices and objective values have a numerical audit; these searches are not lower-bound proofs and do not establish universal invariance. Details, fixed-seed search code, data, and an audit script are in `new_results/experiments/`.

## Contents

`SP09_local_invariance.pdf` is the new 13-page manuscript. `new_results/certificate/` contains the exact checkers, fixed minor witnesses, and corruption tests. `new_results/verification/` contains recorded verification results. `prior/` contains the complete previous reference-example package, including its 14-page manuscript, fixed integer coefficient certificate, reconstruction source, and original numerical-search records. `STATUS.md` states the exact boundary of the conclusions. `SOURCES.md` records the public sources and prior-work dependency.

No numerical comparison of two optimized objective values is used as a lower-bound proof. No GitHub files were modified. Exact computer-assisted verification is not represented as proof-assistant formalization or independent peer review.
