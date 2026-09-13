# Recovery and provenance

The earlier attempt ended without a completed answer. The transcript preserved
substantial formulas, code and intermediate results, but the working directories
did not survive subsequent execution-environment resets. This package was
**reconstructed from the recorded work and rerun**, not copied from a surviving
old archive.

The reconstructed and executed checks are enumerated in `results/run_all.json`.
They include symbolic identities and polynomial identification, exact interval
root and local-optimality hypotheses, the strict rational witness, and the
LU/Schur identity test. The layerwise convex-hull relaxation was also rebuilt;
its numerical support was reconstructed exactly and is checked by a separate
standard-library rational verifier.

Earlier transcript entries describe multistart floating-point optimization,
nonlinear real-arithmetic solver attempts, and branching experiments. Their
complete original raw logs were not recovered. They are not represented as
newly rerun experiments, and no global conclusion is based on them. In
particular, no missing solver result is presumed to have been UNSAT.

The present global SMT-LIB query is generated from the exact LU formulation.
It is supplied as a specification of the remaining counterexample problem,
**not as a solved decision problem or a global certificate**.

The package records what the reconstructed computations establish. It does not
claim a particular elapsed research duration, restoration of unavailable files,
or completion of the requested full solution.
