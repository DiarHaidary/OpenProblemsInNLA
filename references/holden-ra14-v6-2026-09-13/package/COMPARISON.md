# What changes from v5 to v6

| Item | v5 | v6 |
|---|---|---|
| Unrestricted all-parameter lower bound | `Omega((k/s) log(1+n*s/k))`, plus `k` | Unchanged; not rebranded as a stronger theorem |
| Unrestricted all-parameter upper bound | `O(min(n,(k/s) log(e*n/k)))` | Unchanged; its construction is reorganized and its certificates reproduced |
| Critical rank-one unrestricted case | Gap between `n log log n/log n` and `n` | Same gap |
| Deterministic-width full-block model | No finite-parameter matching theorem in v5 | Defined explicitly and characterized as `Theta(U)` |
| Arbitrary outputs in the restricted model | Not the new result of v5 | Covered by an exact conditional-rotation comparison |
| Shifted singular-Wishart posterior | Not present | Exact formula on the domain `J > h I`, including the empty transcript convention |
| That shifted family's rank-one difficulty | Not asserted | An averaged `O(F)` algorithm shows it cannot supply the missing linear transition lower bound |
| Global completion claim | PARTIAL | PARTIAL |

The restricted lower bound uses a different hard spectrum from the shifted ensemble. There is no conflict between its worst-case `Theta(U)` rate and the fact that the shifted ensemble is easy at rate `F`.

The new full-block upper bound has a larger explicit constant, 24000 rather than 12000, because both Gaussian stages are computed inside one physical fixed-width prefix. This is an accounting adjustment for the restricted model, not a worsening of the existing unrestricted upper bound.

The v5 PDF and ZIP in `prior/` are unchanged. Their proofs remain unreviewed research arguments, and their original model and dimension qualifiers remain attached to them. Nothing here turns an earlier restricted or dimension-dependent claim into a globally quantified result without a new proof.
