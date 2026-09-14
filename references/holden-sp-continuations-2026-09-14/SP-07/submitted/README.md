# SP-07 — Completion barriers and a two-line variational model

**Status: partial research continuation, not a full solution.** The unrestricted
sharp constant is not determined. This archive does not improve the prior finite
lower bound or the literature upper bound. The number near **1.0373054** is a
certified value of a **formal stationary-model quotient**, not a new SP-07 bound.

The mathematical report is `REPORT.pdf`; editable LaTeX is in `REPORT.tex`.

## Results proved in this continuation

For an odd regular polygon of selected spectral values, Theorem 2.2 gives the
exact minimum anticommutator norm over every Hermitian-unitary completion of a
prescribed circulant overlap, allowing an arbitrary complementary matrix.
Theorem 3.2 removes the circulant assumption from the resulting constant-one
obstruction by a norm-preserving cyclic orbit dilation. The completion dimension
is unrestricted. Attainment in this relaxation uses a nonnormal complementary
matrix and is not presented as a normal-matrix counterexample.

For one explicit sequence of compressed-optimal overlaps, the selected compressed
quotient tends to pi/2, whereas its best completed selected quotient tends to
zero. These statements concern the specified Hall numerator, not every other
possible Hall witness of a completed pair.

The stationary two-line operator model has an exact phase minimization described
by a unique integral equation. Height balancing at a fixed normalized sum is
strictly convex. The rational parameter pair in `certificates/model_parameters.json`
has formal quotient strictly between **1.0373054176426** and **1.0373054176428**.
The actual countable-spectrum matching is computed separately: its ratio is below
one, approximately **0.703762744557** at these parameters. A finite Hall deficit
cannot be replaced by a bijection between two bilateral infinite ladders.

## Run the checks

Python 3.10 or newer is recommended. The new exact checks use only the standard
library; third-party site packages may be disabled:

```bash
python -S verify_polygon.py
python -S verify_model.py
python -S verify_all.py
```

The default combined entry point runs both arithmetic audits and the ten exact
regression/rejection tests, including a second test run with Python optimization
enabled. Acceptance does not rely on removable `assert` statements.

Optional numerical diagnostics, a separate symbolic reconstruction, and the
inherited checks are available with:

```bash
python -m pip install -r requirements-observed.txt
python verify_all.py --numerical --prior
```

The `--prior` option safely extracts the retained round-4 archive into a temporary
directory, then runs its rank-one exact certificate and tests. It also extracts
the nested round-3 archive and reruns the 193-dimensional certificate by both exact
positivity methods. This is the slower part of the verification. No optimizer is
needed to check that inherited finite lower bound.

The optional model exploration can be rerun independently:

```bash
python research/stationary_fit.py --optimize
```

Its three local optimization runs and the bulk fit are numerical diagnostics,
not global parameter-optimality or finite-transfer certificates.

## The inherited global bound

The prior rational normal pair still proves

    C_normal > 20000000 / 19281027 = 1.03728914440086...

Its matching distance is exactly 2 and its perturbation norm is strictly less
than 19281027/10000000. Both positivity methods passed again in this continuation.
The cited literature upper bound remains C_normal < 2.9038872828. The report
attributes that upper endpoint to the checked Tang preprint rather than claiming
an independent derivation.

## Files

- `REPORT.pdf`, `REPORT.tex`: complete new proofs, distinctions between the
  constants, verification scope, and remaining gap.
- `verify_all.py`, `verify_polygon.py`, `verify_model.py`, `src/`, `tests/`:
  runnable arithmetic audits and diagnostics.
- `certificates/`: the chosen rational model parameters and requested strict
  interval, recomputed rather than trusted by the checker.
- `research/`: proof-development notes, the stationary diagnostic, and an
  unchanged inherited floating-point search candidate used for the bulk fit.
- `results/`: actual execution records, including the inherited finite certificate.
- `prior/`: the unchanged round-4 ZIP, with earlier continuations nested inside it.
- `sources/PROVENANCE.md`, `STATUS.json`, `MANIFEST.sha256`: attribution, status,
  and file-integrity information.

The inherited search candidate is not the rational 193-dimensional certificate;
they are kept distinct in the report and code. The norm-completion minimizers in
Sections 2–4 are not silently assumed normal. The stationary infinite construction
is not silently substituted for a finite matching problem.

No external referee report, proof-assistant formalization, or historical-priority
claim is supplied. No repository files were modified. The missing theorem is a
sharp, rank-uniform upper bound for arbitrary diagonal data, with matching finite
sharpness evidence.
