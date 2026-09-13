# Changes from the recovered partial package

The supplied `prior/IE20_recovered.zip` is byte-for-byte identical to the
archive supplied in the conversation. The new main manuscript does not
replace or retrospectively change its status.

## Mathematical additions

The scalar result changes from a sharp asymptotic order to an exact
integer threshold obtained from the nine operations affecting x1.
A new joint dimension/conditioning witness strengthens the additive lower
bound to log2(nK)-5 for n>=2.

The exact first-step envelope M(K) and its finite-precision transfer give
explicit additive constants for coarse tolerances. A new prefix-wise
matvec estimate replaces the earlier conservative quadratic dimension
factor in the local error budget by a linear factor.

The general upper argument now uses H=min(K,64/epsilon^2), rather than K
alone, to bound step lengths under the all-failure hypothesis. Its proof
horizon is the minimum of n, an explicit Chebyshev horizon, and an
explicit universal backward-error horizon. The polynomial arguments
include a transfer to the rounded recurrence; they do not simply import
an exact-arithmetic convergence theorem.

Together these results give P=log2(nK)+O_epsilon(1), uniformly in n>=2
and K for each fixed tolerance. They also give a sharp order uniformly
on 1<=K<=2 and preserve the other stated sharp regions.

## Preserved limitations

The growing-dimension hard family's exponent threshold remains
non-uniform. The general upper and lower bounds still do not match for
all triples. The regime K=n^2, epsilon=n^(-2) remains explicitly unresolved
by these arguments.

## Reproducibility changes

The old executor is reused without changes. Old `verify.py` and
`test_envelope.py` are copied as `verify_legacy.py` and `test_legacy.py`;
the latter's import is adjusted for the renamed verifier. New files add
exact bound evaluation, polynomial construction, rational joint-breakdown
schedules, and further checks. The reports were regenerated rather than
copied from prior outputs.

The new PDF was compiled in three LaTeX passes, rendered, and visually
inspected. Its exact checks are evidence about the recorded finite
instances, not machine verification of the analytic arguments.
