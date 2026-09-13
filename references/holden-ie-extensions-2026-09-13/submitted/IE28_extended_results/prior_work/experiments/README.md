# Reconstructed exploratory scripts

These are selected scripts reconstructed from code preserved in the interrupted conversation. Formatting, comments, output locations, and a few defensive checks were updated. They are not byte-identical original files. The main mathematical and numerical API is `../src/ie28.py`.

`solve.py` is the original-style SciPy search over logarithms of the diagonal ratios. It fits the characteristic coefficients of the scaled inverse and the logarithmic determinant. It also extracts an eigenpolynomial from a computed nullspace.

`explore3.py` reconstructs the sextic elimination experiment for three nodes. The acceptance tolerances and real-root classification are heuristic. The displayed number of accepted candidates is not a certified root count. This is not the proof of the three-stage theorem.

`homotopy.py` reconstructs the complex predictor-corrector experiment with permutation start solutions. It has no certified path tracking, projective endgame, singular-root handling, or completeness guarantee. Distinct start paths can merge numerically. Its function name `all_solutions` is retained from the exploratory code, but does not describe a certified complete enumeration.

Run from the archive root:

```sh
python experiments/solve.py
python experiments/explore3.py
python experiments/homotopy.py
```

The delivered `results/exploratory_checks.txt` and `results/homotopy_example.json` were generated during recovery. They are explicitly separate from the proof and from exact symbolic checks. Legacy boundary scans and unsuccessful broad searches were not promoted into the final proof or a claim of general nonexistence.
