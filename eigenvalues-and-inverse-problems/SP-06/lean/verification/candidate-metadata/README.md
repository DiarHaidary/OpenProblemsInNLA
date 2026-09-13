# SP-06 Lean proof candidate

This package implements the complete negative resolution of the original
SP-06 finite Toeplitz spectrum implication. All twenty exported theorems
pass local Lean elaboration and LeanCert kernel trust checks. Two independent
final reviews have approved the complete proof; authoritative Linux Comparator
verification remains pending;
the canonical problem has not been promoted to Lean verified.

Read `NUMERICAL_TARGETS.md`, `NLA/SP06/Definitions.lean` and `Challenge.lean`
in that order. `SOURCE_MAP.md` records immutable canonical sources. All
definitions use ordinary finite Laurent evaluation, Mathlib's actual unit
circle and its actual complex matrix spectrum. Existence of the entire real
Jordan curve is proved in `NLA/SP06/Curve.lean`. The twenty deliberate
Challenge placeholders live in a separate environment and are never imported
by `Solution.lean`.

The proof uses exact rational arithmetic and one scalar root equation.
A uniform algebraic separation bound gives a continuous radius without curve
subdivision or an implicit-function calculation. LeanCert kernel trust and
real Linux default-kernel, permitted-axiom and Comparator checks are separate
gates. Local results are recorded in `verification/local-2026-09-13/CHECKS.json`.

The reviewed Schiffer and Forsythe examples guide statement/proof separation
and kernel-trust checking. Their structure is a reference, not an imported
mathematical assumption. The package pins LeanCert and its dependency closure
in `lake-manifest.json`. Both pre-proof statement approvals and their unchanged
boundary hashes are retained under `reviews/`. The exact algebra and finite
spectrum calculation are in `NLA/SP06/Numeric.lean`; the original universal
implication is explicitly negated in `NLA/SP06/Proof.lean`.

For a local complete proof check using an existing pinned dependency cache:

```
SP06_DEP_ROOT=/path/to/existing/.lake/packages \
  python3 verification/compile_development.py Solution
```

The command checks dependency source revisions, invokes Lean directly and
writes all new objects and logs to a fresh temporary directory. It never runs
Lake or modifies shared dependency artifacts. The existing objects are not
rebuilt from source by this local check. Each problem has its own pinned Lake
project; this command reuses dependency objects and keeps all new proof objects
private. To reproduce the earlier statement-only check, use
`verification/statement-typecheck.py` instead; its twenty warnings are expected.

Original mathematical proof: Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge. Formalization:
George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA. Substantial
AI assistance is disclosed; no email is added for George Stepaniants.

To check package hashes and metadata from a full repository checkout, run
`python3 verification/verify_package.py` with the shared metadata requirements
installed. This integrity check is separate from mathematical verification.
