# IE-28 — Recovered work and a three-stage existence proof

**This archive is a partial resolution, not a full all-stage solution.**

The original hyperlink leads to IE-28, *Positive diagonal preconditioning with a nilpotent stiff limit*. The previous attempt did not leave recoverable files or a completed general proof. This package reconstructs the available work from the conversation, completes the three-stage endpoint argument, and includes newly rerun checks.

## Main result

For every `0 < c1 < c2 < c3`, the three-node collocation matrix admits a positive diagonal `D` such that

\[
(I_3-D^{-1}A)^3=0.
\]

The construction also ensures `d1 < d2 < d3` and `ci/3 < di < ci`. An explicit two-stage construction is included. General existence for arbitrary stage counts **s >= 4 is not established in this package**.

Read **writeup.pdf** for the complete arguments, limitations, and references. **writeup.tex** is the editable mathematical source. The proof is not represented as peer-reviewed, and no claim of literature priority is made.

## Reproduce the checks

Use Python 3.11 or later for the pinned dependency set. The core code uses `mpmath` and `sympy`; the exploratory scripts additionally use NumPy and SciPy. Tested versions are recorded in `results/environment.json` and pinned in `requirements.txt`.

```sh
python -m pip install -r requirements.txt
python scripts/check_symbolic.py
python scripts/run_examples.py
```

The numerical script overwrites its JSON and text reports in `results/`. To omit the 66-triple regression grid, run `python scripts/run_examples.py --skip-grid`.

A minimal use of the constructive solver, run from the archive root:

```python
import sys
sys.path.insert(0, "src")
import mpmath as mp
from ie28 import solve_three, diagnostics

mp.mp.dps = 120
c = ["0.1", "0.5", "1"]  # Decimal strings avoid binary-float input rounding.
answer = solve_three(c, dps=80)
print([mp.nstr(d, 50) for d in answer.diagonal])
print("theta =", mp.nstr(answer.theta, 50))
print("radius =", mp.nstr(answer.radius, 50))
print(diagnostics(c, answer.diagonal))
```

The exact mathematical diagonal is defined by the roots in the theorem. Every finite decimal returned by the code is an approximation. For clustered nodes, set diagnostic working precision well above the requested solver precision.

## Contents

- `writeup.pdf`, `writeup.tex`: self-contained two-/three-stage proofs, general reductions, algorithms, and limitations.
- `src/ie28.py`: constructive two-/three-stage solvers, high-precision diagnostics, and a clearly marked experimental higher-stage refinement routine.
- `scripts/check_symbolic.py`: exact identity checks and rational-example regression checks.
- `scripts/run_examples.py`: two two-stage examples, seven three-stage examples, six higher-stage candidates, 66 rational node triples, input validation, and an independent refinement cross-check.
- `results/`: newly generated reports and environment information.
- `experiments/`: selected reconstructed exploratory code, separated from the proved construction.
- `STATUS.md`: recovery provenance and the precise missing general step.
- `REFERENCES.md`: the problem URL and primary-paper references.
- `MANIFEST.sha256`: hashes of the delivered files, excluding the manifest itself.

The symbolic checks passed. The numerical checks passed. The higher-stage entries are **uncertified numerical candidates**, not exact existence certificates, and none of the finite numerical tests proves a universal assertion.

To rebuild the PDF with a LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error writeup.tex
pdflatex -interaction=nonstopmode -halt-on-error writeup.tex
```

The result files were recreated during recovery; none is claimed to be an original saved binary from the interrupted session.
