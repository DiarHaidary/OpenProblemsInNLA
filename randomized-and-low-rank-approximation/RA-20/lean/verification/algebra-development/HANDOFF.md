# RA-20 algebra helper completion

Contracts **1 and 2** are complete in `NLA/RA20/Algebra.lean`, SHA-256
`67adf1643bd62089a62d857c404bdb5ee1bbbd192984ed5f1169b8c5ec71f5f1`.
The exports are `NLA.RA20.hollow_variety_semantics_proved` and
`NLA.RA20.reduced_coordinate_ring_proved`; both actual elaborated types match
the immutable Challenge types exactly.

The matrix proof expands the determinant to `2*a*b*c`. An actual rank bound
forces this determinant to vanish; conversely, each zero-factor case has an
explicit width-two matrix factorization. Symmetry and all three zero diagonal
entries identify every point of the original matrix variety with its hollow
coordinates. Degenerate matrices and intersections of components are included.

The polynomial substitution `hollowPullback` maps the nine original matrix
coordinates to their actual hollow entries. Its explicitly constructed section
proves surjectivity. The three distinct polynomial variables are prime and
pairwise relatively prime, so their product is squarefree and its principal
ideal is radical. Mathlib's actual Nullstellensatz then identifies the
vanishing ideal of the union of three coordinate planes with `(abc)`. Applying
the proved matrix-point correspondence gives
`definingIdeal_eq_comap_abcIdeal`. The first isomorphism theorem constructs the
actual reduced coordinate-ring equivalence, preserving every matrix coordinate.
No proposed equation is substituted into the frozen definition of the variety
or its vanishing ideal.

The named integration interface is:

- `reducedCoordinateEquiv : CoordinateRing 3 3 ≃ₐ[ℂ] ABCCoordinateRing`;
- `reducedCoordinateEquiv_mk_X (i j : Fin 3)`, the exact coordinate equality;
- `definingIdeal_eq_comap_abcIdeal`, the equality of ideals;
- `hollow_mem_variety_iff` and `matrix_eq_hollow_of_mem`, the point correspondence.

Four successful direct-source commands checked frozen Definitions, the final
helper, a namespace-only diagnostic copy of Challenge, and an actual dependency
inspector. The final helper compiled in about 8.7 seconds with no warnings.
The inspector checked 46 safe project declarations and 24 required mathematical
dependencies, traversing types and proof bodies. Six source and six diagnostic
LeanCert kernel assertions passed; the two source and six diagnostic printed
axiom lists contain exactly `propext`, `Classical.choice`, and `Quot.sound`.
The admitted diagnostic reference is excluded from actual proof dependencies.
No numerical interval certificate, native reduction or additional axiom is used.

Two initial failed helper elaborations are retained: one required explicit
orientations of symmetry rewrites; the other required three concrete vector and
quotient rewrites. No mathematical statement changed. All source snapshots,
commands, raw output and exit codes remain in this directory. The compile
driver uses one initially empty private prefix and the exact ten read-only
MI-22 package artifacts. All ten revisions and clean source statuses were
checked before and after. No Lake build, dependency download, dependency copy
or shared-cache write occurred. The private prefix remains available for the
separately authorized next module.

The proof-start gate and implementation roles preceded implementation. All 68
frozen project inputs and 16 original source snapshots and Git blobs are still
exact. `validation.json` records these checks and counts. The complete manifest
binds this helper, every local evidence file and the frozen statement/review
closure, including nested manifests; only its own exact path is excluded.

Implementation and these author diagnostics: `/root/formal_review_standards`.
This is not an independent final mathematical review. Full RA-20 integration,
two independent final reviews, authoritative Linux replay, Comparator controls
and publication remain pending. This handoff records local macOS work only.

Formalization author: George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. Original negative-resolution mathematics: the repository's Codex automated
maintainer audit. Original conjecture: Kubjas, Sodomaco and Tsigaridas.
