# RA-05: unrestricted even-power continuation

**Status: further partial resolution of RA-05, not a full solution.**

Start with `manuscript.pdf` (21 pages), especially Theorem 1.1, Theorem 1.2,
Corollary 1.3, and Section 10. `manuscript.tex` is the complete LaTeX source.

## Results proved in this continuation

For every fixed integer s >= 2, every k >= 1, and 0 < epsilon < 1/2:

    S_(2s)(k,epsilon)
      <= C_s [k^((3s-1)/2)/epsilon + k^(s-1)/epsilon^2]
         log^5(2k/epsilon).

The input rank, ambient dimension, and original row count are unrestricted.
All returned weights are nonnegative and attached to original row indices.
The proof is an existence/size proof, not an efficient implementation.

A re-proved lower bound gives

    S_(2s)(k,epsilon) >= c_s k^(s-1)/epsilon^2.

Consequently these bounds match up to logarithms throughout

    epsilon <= k^(-(s+1)/2).

Examples: p=6 at epsilon=k^-3 has order k^8 up to logs; p=8 at
 epsilon=k^-3 has order k^9 up to logs. Constants depend only on fixed p.

## What is not claimed

The full problem includes every real p>2 and all accuracies. Intermediate
accuracy remains quantitatively unclassified for even p>=6; non-even powers
are not classified by this continuation. At p=6, epsilon=k^-1, the combined
available lower bound is k^(9/2), while the upper bound is k^5, ignoring logs.
No independent audit, human peer review, proof-assistant verification,
priority certification, or repository modification is claimed for the new work.

## Contents

- `manuscript.pdf`, `manuscript.tex`: statements and proofs, including every mixed monomial.
- `code/even_features.py`: symmetric-tensor and operator-query diagnostics.
- `code/verify.py`: finite verification suite; currently 8,453 assertions.
- `code/check_exact_certificate.py`: separate standard-library rational checker.
- `results/exact_even_power_certificate.json`: one full-rank input tested at p=4,6,8,10,12.
- `results/verification.json`: categories, tolerances/residuals, instance descriptions, environment and limits.
- `PROOF_AUDIT.md`, `STATUS.md`, `SOURCES.md`: dependency and scope boundaries.
- `prior_work/RA05_unrestricted_quartic_package.zip`: unchanged prior archive, including its nested predecessors.

## Reproduce

Use Python 3.10+ and NumPy. Install the Python dependency, then run:

```sh
python -m pip install -r requirements.txt
sh ./run_checks.sh
```

The script checks the delivered SHA-256 manifest first, then regenerates the
finite results and the exact certificate. It overwrites the recorded results
with the current run; tiny floating-point residuals can differ across numerical
libraries. Counts are bookkeeping assertions, not independent mathematical proofs.
The asymptotic partial-coloring and random-core oracles are not implemented.

To run only the exact integer/rational certificate checker, no third-party
Python dependency is needed:

```sh
python code/check_exact_certificate.py
```

To rebuild the mathematical manuscript, install a LaTeX distribution and run
`make pdf`. Rebuilt PDF bytes need not match the delivered hash because LaTeX
may include build timestamps. Do not confuse successful compilation or finite
checks with a formal proof certificate.
