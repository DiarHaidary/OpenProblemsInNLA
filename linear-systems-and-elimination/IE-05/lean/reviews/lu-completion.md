# IE-05: completed generic scaled-LU trajectory helper

**Complete:** `NLA.IE05._proved.scaledLU_trajectory` has exactly the frozen
eighth Challenge contract, with no extra hypothesis. This is scoped author
validation, not a complete IE-05 proof, independent final review, or actual
Linux Comparator verification.

Formalization credit: **George Stepaniants**, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. The `formal_review_standards` AI agent authored this module and the earlier
statement draft/Pivot helper; it is not an independent final referee. The
original conjecture retains John Peca-Medlin's attribution and the submitted
counterexample retains Stepaniants's existing mathematical credit. No contact
email is included.

The exact accepted proof gate and two statement approvals preceded this task.
The separate ownership receipt is
`verification/lu-development/gate-and-ownership.json`. All 733 frozen project
inputs and 27 original source/policy Git blobs remain unchanged. Before and
after this work, the complete 150-file GEPP seal and 847-file QR/Scaling seal
were rehashed. None of their bytes was edited. Root retains the separate integer
certificate, QR identification, and real-growth tasks.

## Exact mathematics and implementation

For every natural dimension, real unit-lower `L`, upper-triangular `T` with
positive diagonal, positive column scales `d`, and lower multipliers bounded in
absolute value by one, the theorem proves all three reviewed conclusions:

1. `noSwapPath n` is an actual `FirstAvailablePath` for
   `scaledColumns (L * T) d`.
2. The actual ascending tie scan `firstPath` equals that path.
3. For **every** `k ≤ n`, the actual recursive trajectory is
   `scaledColumns (tailProduct L T k) d`.

No determinant, admissible-path, desired-trajectory, or nonzero-pivot result is
assumed. The proof establishes those pivot facts from the factor hypotheses.
`tailProduct_terminal` separately proves the terminal product is literally the
zero matrix, including dimension zero; the full trajectory theorem includes
that terminal stage.

The nine material declarations in `NLA.IE05._proved` are:

| Declaration | Purpose |
| --- | --- |
| `tailProduct_zero` | The actual initial trailing sum is the full matrix product. |
| `tailProduct_terminal` | No active coordinate remains at stage `n`. |
| `tailProduct_pivot_row` | The pivot row is the upper factor's row. |
| `tailProduct_pivot_column` | The pivot column is the lower multiplier times the upper pivot. |
| `tailProduct_split` | Split off exactly one term of the finite trailing-factor sum. |
| `scaled_tail_schur` | The genuine row-swap/Schur definition cancels exactly that term. |
| `scaled_tail_firstAvailable` | Positive pivot, multiplier bound, and least-row tie specification. |
| `scaled_noSwap_trajectory` | Induction on actual recursive states, for every `k ≤ n`. |
| `scaledLU_trajectory` | Exact frozen three-conjunct contract using the proved scan uniqueness. |

Only the pivot column's positive square root must be nonzero for the generic
cancellation. No numerical square root, interval subdivision, finite matrix
entry enumeration, or determinant calculation occurs in this helper. The
column scaling is retained in every exact state. Ties are allowed: the current
diagonal row is already the smallest active row, and the genuine Pivot helper
identifies this valid path with the frozen scan. Actual `Finset` sum lemmas and
`Real.sqrt` positivity are used, not substitute definitions.

## Observed validation

The final immutable run is
`verification/lu-development/attempt-x4p3dxwm`. Four fresh direct-source commands
for Definitions, the sealed Pivot module, LUTrajectory, and the inspector all
returned zero in **20.601 seconds** on macOS 14.6.1 arm64 with Lean 4.33.1.
The private prefix began empty; no prior project objects were used. Nine
existing dependency object directories and all ten clean source pins were read
from the shared MI-22 cache. Cli is source-only and is not imported. No Lake
build, network download, dependency-cache copy, or shared-cache write occurred.
All generated private objects were hashed, then removed.

The exact exported type is definitionally equal to an admission-free Prop
constructed mechanically from the frozen Challenge header. `Challenge.lean`
is not imported by this proof or inspector. The actual type/body traversal
checks **42** safe, nonpartial project declarations and **29** retained material
dependencies, including the actual scan, row swap, Schur update, scaling, finite
trailing sum, square root, triangularity, and all three path definitions. Its
nine root declarations include the terminal-zero helper even though that
auxiliary theorem is not needed in the main theorem's proof term.

There are **23** successful explicit LeanCert `#assert_trust kernel` invocations
and **23** exact standard-three axiom reports across the fresh modules: five
Pivot, nine LU, and nine inspector checks. All transitive axiom closures are
subsets of `propext`, `Classical.choice`, and `Quot.sound`. No written or retained
proof admission, custom axiom, unsafe/partial project declaration, native
execution trust, or diagnostic-reference dependency is used. LeanCert's role is
kernel-trust auditing of exact universal algebra; there is no artificial
numerical certificate. Mathematical modules have no warnings. Five
inspector-only unused-binder warnings preserve the frozen hypothesis names in
the expected Prop; they are not proof holes.

All three development attempts are retained. The first exposed a missing pair
of parentheses around a sum body and an unsimplified true conjunction in a
Schur conditional. The corrected mathematical source passed the second run;
the third fresh run added the successful type/dependency inspection. The first
run's error-recovery `sorryAx` diagnostics remain visible and are not treated as
proof success. The delivered source is identical in the second and third runs.

The final audit verifies every frozen input, original Git blob, source/log hash,
ten pins, prior complete seal, actual declaration check, and private-prefix
cleanup. Actual Linux Comparator and independent full-proof review remain later
gates. No canonical status, ID, catalog, Git history, metadata verification
claim, or publication was changed.

## Exact delivered identities

- LUTrajectory source: `96d71b7a46ec692f9e84e6450adacfa71b9c79ef69ff17222e44173f3e6abcbb`
- Inspector: `376d5329b1721614133b70e73c364d7788ea12b0a2de2d6722afd9c7d3b3d691`

Use `verification/lu-development/verify_seal.py` for a read-only integrity check.
A new source elaboration should run `compile.py Inspect` in a separate project
copy so that the present sealed evidence remains unchanged. Exact commands,
source snapshots, toolchain identity, dependency paths, timing, and object
hashes are retained in the successful run.
