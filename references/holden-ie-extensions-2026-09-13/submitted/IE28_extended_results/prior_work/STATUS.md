# Status and provenance

## What was actually recovered

The recovery session found an empty `/mnt/data` workspace. The prior conversation retained mathematical descriptions, executable code snippets, and some numerical outputs. There was no recoverable original ZIP, PDF, or completed arbitrary-stage proof.

This archive reconstructs the central inverse-collocation formula, polynomial parameterization, spectral-coefficient equations, three-node endpoint computations, and selected exploratory scripts. It is a reconstruction of recoverable work, not a byte-for-byte recovery of absent files.

## Work completed during recovery

The previously unfinished three-stage argument has been completed in `writeup.pdf`. The proof uses

\[
p_{r,\theta}(t)=t(t+r)(\theta t+r),\quad 0\leq\theta\leq1,
\]

and chooses the unique positive `r(theta)` satisfying the determinant constraint. A universal positive trace identity at `theta=0` and a universal negative trace identity at `theta=1` force a trace zero. One eigenvalue is already one throughout the family. In dimension three, these facts determine the whole characteristic polynomial.

This establishes the desired diagonal for every distinct positive real node triple, with strict ordering and `ci/3 < di < ci`. The proof does not rely on sampling. Universal symbolic identities and finite exact regression examples are distinguished in the report.

All files in `results/` were generated anew. Decimal candidates, including the high-stage entries, have no interval certification.

## What is not established

There is no proof here that for every `s >= 4` and every admissible set of nodes there are positive `alpha_j` solving all the reduced coefficient equations. There is no proof that all positive solutions must belong to the negative-root polynomial ansatz. There is no general counterexample, uniqueness theorem, complete count of positive diagonals, or certified exhaustive homotopy calculation.

Consequently the original all-stage problem has not been fully solved by this work. This limitation is an identified missing argument, not a conclusion inferred merely from the problem's historical status.

## Scope of computational assurance

`check_symbolic.py` verifies the two universal endpoint trace identities by exact rational simplification. It also verifies the divided-difference formula and spectral completion identity. Structural identities additionally receive exact rational-example tests, while their universal proofs are provided in the text.

`run_examples.py` is reproducibility and regression testing. Small floating-point residuals are not exact certificates. The mathematical existence theorem for `s=3` is supplied by the analytical proof, not by those residuals.

The selected files in `experiments/` preserve exploratory approaches. Their search failures must not be interpreted as counterexamples, and their recovered root counts must not be interpreted as exact counts.

## Attribution boundary

The problem statement and historical context are attributed in `REFERENCES.md` and the writeup. The three-stage argument is presented with all details for review. No claim is made that this proof is the first such proof in the literature, or that it has been independently refereed.
