# IE-16 Lean statement boundary

This is a **statement-stage** Lean package for IE-16. It records the exact
finite-set complex-polynomial target and the nine-point degree-four
counterexample described by Sidney Holden. The formalization author is
George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA.

`NLA/IE16/Definitions.lean` contains the proof-independent definitions of
finite maxima, the infimum `M`, the subset maximum, the full original
universal assertion, and the exact witness. `Challenge.lean` contains fifteen
deliberate placeholders covering the finite certificate, the attainment
bridges for the full and subset infima, positivity of the subset maximum, and
the implication for the full universal target. `NUMERICAL_TARGETS.md` gives
the source map, exact numerical contracts, and planned proof route.

The three attainment bridges requested during review are explicit Challenge
exports: `full_minimum_isLeast`,
`every_five_point_subset_minimum_isLeast`, and `subset_max_positive`. The
pre-bridge 12-export boundary is preserved under
`verification/prior-statement-boundary-20260913/` for audit.

The complete informal proof and exact arithmetic certificate remain
attributed to Sidney Holden. The stronger amplification theorem is outside
the Lean scope because the finite witness already refutes the original
universal statement. No proof implementation, proof approval, Linux run, or
Comparator result is claimed at this stage.

The package is pinned to Lean 4.33.1, Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`, and LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`. It was typechecked directly
against existing pinned dependency artifacts without copying `.lake` into
this package.
