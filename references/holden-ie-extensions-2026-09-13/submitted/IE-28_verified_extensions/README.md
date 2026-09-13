# IE-28: recovered proofs and continued investigation

## Status: NOT A FULL SOLUTION

This archive does **not** establish the universal assertion in IE-28 and does
**not** provide a counterexample to that assertion. No file in this archive
should be cited as a complete solution of IE-28.

The target is the problem at:
https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/linear-systems-and-elimination/IE-28/README.md

The recovered report supplies proofs for arbitrary admissible two- and
three-node sets, an all-stage local existence result near a common positive
node, and an exact four-node example. The continued investigation includes
additional numerical searches and an exact eleven-stage obstruction to one
particular negative-root construction. That obstruction is **not** an
obstruction to positive diagonals in the original problem.

## Contents

- `recovered_work/`: the previous report, LaTeX source, exact certificates,
  numerical code, captured problem statement, and original claim-status file.
- `continued_work/`: preserved continuation scripts and outputs, including
  the eleven-stage obstruction. These are research records, not an additional
  general existence proof.
- `additional_checks/`: preserved four- and five-stage search scripts/output.
- `STRUCTURAL_REDUCTION.md`: a self-contained reduction to a diagonal plus
  skew-symmetric Cauchy matrix, and an exact counterexample showing why
  several broader matrix-class arguments do not suffice.
- `verify_structural_reduction.py`: exact rational-arithmetic checks for the
  reduction and for the new, auxiliary counterexample.
- `verification/`: replay logs and machine-readable execution status.
- `MANIFEST.sha256`: checksums for the packaged files.

## What remains to be proved

For every number of stages and every ordered set of distinct positive nodes,
one must either prove that a single fixed positive diagonal makes the stiff
iteration matrix nilpotent, or exhibit an admissible node set and rigorously
exclude every positive diagonal for that set. Neither task is completed here.

Numerically successful examples, a local continuation theorem, a failed
parametrization, or a counterexample for a broader class of matrices cannot
replace this missing global argument.

## Reproduction

Use the requirements and reproduction instructions in `recovered_work/` for
that report. The additional exact check needs Python 3 and SymPy:

    python verify_structural_reduction.py

The original report is preserved unchanged, so its own status limitations
continue to apply. The top-level status in this file governs the archive as a
whole. The eleven-stage obstruction and auxiliary matrix counterexample must
not be confused with counterexamples to IE-28.
