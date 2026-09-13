# Verification boundary

## Exact checks

`derive_algebra.py` uses polynomial and rational-function arithmetic over the
rationals. It derives F, verifies all candidate active identities and the fifth-
pivot identity, factors the discriminant, checks the reference P5 coefficients,
and proves one root in (4,5) by an integer Descartes transformation plus endpoint
signs. It does not enumerate other active patterns.

`verify_local.py` uses 512-bit dyadic intervals with integer endpoints and
outward rounding. It checks a contraction map for (F,F_z), feasibility of the
candidate, positivity of the pivots and 77 inactive slacks, a full-rank active
Jacobian minor, positive multipliers, and negative reduced curvature. The report
proves why those checks imply a strict local maximum on the normalized fixed-
diagonal-path feasible set. Exact active equalities come from the symbolic
check, never from a small numerical or interval residual.

`rational_witness.py` makes no assumption that the root centers are exact. It
reads 25 integer numerators, recomputes every Schur complement using Fraction,
and verifies all 100 strict comparisons, nonsingularity, normalization and the
stated strict lower bound. This check is independent of SymPy and the interval
kernel.

`global_model.py` specifies all diagonal-path CP constraints in LU variables.
The report proves the formulation and explains how permutations cover all
pivot paths. Its exact test on the rational witness checks the implementation
of the LU/Schur identities; a single witness test is not a universal proof.

`verify_layer_hull.py` proves a result about a **relaxation only**: a rational
mixture attains 81/16, and retained linear inequalities give the matching upper
bound. A nonzero two-by-two minor proves that one of its layers is not rank one.
This is not a counterexample or a value proved attainable for g5.

## Trust and reproducibility

The verification relies on the correctness of Python integer and Fraction
arithmetic, the small interval kernel, SymPy's exact symbolic arithmetic for the
algebraic reconstruction, and the mathematical arguments in the report. It is
not a Lean, Coq, Isabelle, or other proof-assistant formalization. Randomized
containment tests for the interval kernel are supplementary software tests,
not a substitute for the proof of outward enclosure.

All inputs needed by the exact verifiers are included. Full floating-point
exploratory histories and the source paper itself are not needed to run them.
Successful local or rational verification never changes `global_solution` to
true. The missing universal upper bound remains explicitly unproved.
