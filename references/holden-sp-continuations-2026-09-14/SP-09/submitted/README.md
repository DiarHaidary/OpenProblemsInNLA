# SP-09: First-order invariance under independent spectral splitting

**Status: PARTIAL. This archive does not prove or disprove general SP-09.**

Read `SP09_first_order_splitting.pdf` for the new result and its proof. The editable source is `manuscript/SP09_first_order_splitting.tex`. The complete preceding proof pack is retained under `prior_round2/`.

## What is established in this round

Starting from any fixed finite repetition of the certified three-point pair, all repeated eigenvalues may be split independently in fixed complex directions. The right derivative of the squared orbit distance is exactly a four-Hermitian-orbit optimization, with rational coefficients in Q(i sqrt(3)). A classical Horn block-averaging theorem makes this coefficient invariant under finite amplification.

For each fixed base repetition r and amplification k, the squared amplification gain is nonnegative and at most C_(r,k) t^(3/2) for sufficiently small nonnegative t. The constants and smallness radius are existential and may depend on dimensions and directions. This is not an exact equality at nonzero t and is not uniform in k.

The new exact identities include a rank-three active-face derivative, a rank-five gauge tangent, a single nongauge flat direction, first-order coefficients (153-45s)/364, (225-135s)/364, and 0, and positive second-order Schur curvature 1/52, where s^2=-3.

The six-dimensional first-order coefficient also has a closed polygon formula. A worked example has coefficient 603/364. Its numerical illustration constructs actual upper-bound witnesses rather than estimating a lower bound.

## Reproduce the checks

From the extracted archive root, using Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python -O verify_all.py
```

This verifies the SHA-256 manifest, runs all eight retained prior exact programs, and runs both new exact-check programs. All finite arithmetic in the new exact checker uses integers and `fractions.Fraction`; NumPy is an array container, not a floating-point proof engine.

Optional numerical illustrations and the saved-search audit require SciPy:

```bash
python -m pip install -r requirements-experiments.txt
python -O verify_all.py --include-numerics
```

To save fresh logs without modifying the packaged records:

```bash
python -O verify_all.py --include-numerics --report-dir ../sp09_fresh_verification
```

The optional search can be rerun separately with `python experiments/search_candidate34.py`. Its results are numerical feasible upper bounds, never certified base lower bounds.

## File guide

- `SP09_first_order_splitting.pdf`: 11-page mathematical manuscript.
- `certificate/first_order_geometry.py`: exact recomputation of the new finite identities.
- `certificate/first_order_witness.json`: fixed, human-readable rational witness.
- `certificate/test_first_order_geometry.py`: eight corrupted-witness tests and one changed-model test.
- `experiments/first_order_witness_demo.py`: constructive six-dimensional upper-bound illustration.
- `experiments/verify_candidate34.py`: audit of one retained n=7, k=2 numerical comparison.
- `verification/`: saved exact, numerical, and archive-check records.
- `prior_round2/`: the complete previous two rounds, including their source, fixed data, and exact verifiers.
- `STATUS.md`: precise scope and unresolved general inequality.
- `SOURCES.md`: source attribution and the exact external Horn input.

## Verification boundary

The programs check finite algebra, stored data, and selected numerical constructions. The analytic local-slice, Taylor-remainder, Schur-complement, and Horn arguments are written proofs in the manuscript; they have not been formalized in a proof assistant. Passing the checkers is not an independent verification of every analytic argument. No independent human peer review or comprehensive novelty determination is claimed. No repository files were changed.
