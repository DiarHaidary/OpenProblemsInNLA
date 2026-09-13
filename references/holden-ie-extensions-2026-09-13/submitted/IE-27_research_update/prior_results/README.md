# IE-27 — recovered research and certified finite-stage results

**Status: partial mathematical results, not a complete solution of IE-27.**

The interrupted run did not leave recoverable files in the current workspace.
This archive reconstructs the available proof arguments and code excerpts, then
regenerates and independently checks the certificate data. It does **not**
represent a recovered, completed proof for every stage number.

## What is established

The manuscript proves the exact reduction from the symmetric positive-definite
spatial matrix pencil to the stage matrices, an all-stage positive-pivot result
for the specified Radau factorization, and a sufficient common-energy criterion.
It includes a closed-form two-stage spectral bound and an explicit three-stage
proof in the field Q(sqrt(6)).

There are **64 freshly verified energy certificates**, covering every integer
stage count **2 through 64, and also 80**. For each included stage, the certificate
proves the disk enclosure for **every positive shift**, hence for all symmetric
positive-definite spatial matrices and every positive time step. These are not
checks on a finite grid of shifts. Stages 65–79 are not included.

The all-stage disk inequality has **not** been proved in this work. In particular,
no theorem establishes the required energy certificate for every admissible q.
The manuscript identifies that precise missing step rather than extrapolating
from the finite set.

## Start here

`report.pdf` is the mathematical write-up. Its complete LaTeX source is
`report.tex`, with generated tables in `tables/`.

`results/verified.json` and `results/certificates.csv` list the checked claims and
strict rational-arithmetic margins. `results/exact_q3.json` is the independent
three-stage algebraic check. `RECOVERY.md` records provenance and limitations.

## Recheck the proofs

Python 3.10 or newer is required. Verification uses only the standard library;
NumPy and SciPy are **not** needed for these commands.

```sh
python code/run_checks.py
```

This runs the tests, the independent Q(sqrt(6)) proof, and all 64 certificate
checks. New results go into `recheck/`, leaving the bundled baseline results
unchanged. A failed check exits with a nonzero status.

Individual checks:

```sh
python code/exact_q3.py
python code/test_verify.py
python code/verify.py certificates/q080.json
python code/verify.py certificates/*.json --json-output recheck/verified.json
```

The wildcard example is intended for shells that expand `*`; `run_checks.py`
works without shell wildcard expansion.

## Generate additional candidates

Generation is optional and uses NumPy and SciPy. Install the versions recorded
in `requirements-generation.txt`, then run, for example:

```sh
python code/generate.py 65 --output new_candidates
python code/verify.py new_candidates/q065.json
```

This is a usage example, not a claim that stage 65 has been checked in the archive.
The optimizer is an untrusted proposal mechanism. It may fail, and every proposed
certificate must pass the integer-interval checker. Solver convergence is not a
proof; solver failure is not a counterexample.

## Rebuild the report

With a LaTeX distribution containing the standard packages named in `report.tex`:

```sh
python code/build_tables.py
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

`MANIFEST.sha256` contains hashes of the delivered files. The source bibliography
is in the report and `references/sources.md`. No third-party paper PDFs or font
files are bundled. The GitHub plugin was not used.
