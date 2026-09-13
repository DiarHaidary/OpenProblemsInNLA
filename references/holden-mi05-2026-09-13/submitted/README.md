# MI-05 — round five: analytic continuation

**This archive is not a full solution of unrestricted MI-05.**

Start with `report.pdf` when present, or the complete editable `report.tex`.
The main report proves a universal fourteen-term signed identity in order four,
optimality and uniqueness on its 48 positive-obstruction regions, a genuine
all-complex-spectra unitary neighborhood of radius 1/100, a support-direction
reduction, and a sharp real-orthogonal obstruction bound.

The main analytic proofs do not depend on the larger polytope enumeration in
`extensions/`. In particular, the zero-obstruction case is not silently declared
settled by an unexamined finite enumeration. Spectrum-independent negative
weights are not counterexamples to the spectrum-dependent original conjecture.

## Actual audit outcome

Read `results/audit.json` and the command logs. They report executed commands,
return codes, timeouts, and whether normal and optimized verification agree.
The existence of this archive alone is not a claim that every check passed.

## Reproduce

Python 3 with SymPy is needed for the exact verifier; no numerical optimizer is
used by that verifier. Run from this directory:

```sh
python code/check_manifest.py
python code/verify_analytic.py
python -O code/verify_analytic.py
python -m unittest discover -s code -p test_analytic.py -v
python -O -m unittest discover -s code -p test_analytic.py -v
```

Build the mathematical PDF with two runs of `pdflatex report.tex`.

## Contents

- `report.tex`: self-contained mathematical proofs and explicit remaining gap.
- `report.pdf`: compiled report, when compilation succeeded.
- `code/verify_analytic.py`: exact finite and symbolic checks.
- `code/test_analytic.py`: ten regression and deliberate-corruption tests.
- `results/`: actual audit records, complete command logs, and exact example data.
- `previous/`: unchanged preceding archive when its mounted file was found.
- `extensions/`: snapshot of the larger finite-polytope working package, when
  available, with its own status; not a premise of the analytic report.

No repository changes, literature-priority claim, independent peer review, or
formal proof-assistant verification are asserted.
