# IE-05: completed GEPP helper author validation

The first five frozen contracts are completely proved in `NLA/IE05/Pivot.lean`
and `NLA/IE05/GEPP.lean`. This is a bounded implementation handoff, not a
complete IE-05 proof, independent final mathematical review, formal verification
status promotion, or authoritative Linux Comparator result.

Formalization credit: **George Stepaniants**, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. The implementation was written by the `formal_review_standards` AI agent,
which also authored the reviewed statement package. The coordinator suggested
the supported-vector injectivity proof route. Neither contributor is an
independent final referee for these proofs. The original IE-05 conjecture is
attributed to John Peca-Medlin; the submitted counterexample retains George
Stepaniants's existing mathematical credit. No contact email is included.

## Fixed boundary and exports

The accepted proof gate is
`verification/proof-start.json` (SHA256
`2a8e4b4029a6ba005856c9ec56178cc7fefc8b8b16e945df27599ce471c95726`).
Both independent statement approvals preceded implementation. All **733**
statement-freeze files and **27** original source/policy Git blobs remain
byte-identical to the recorded boundary at
`5830ed4fb06da0659414a3deb2a40ad327aca052`.

Each of the following theorem types was compared by Lean definitional equality
with a mechanically extracted, Prop-valued version of its exact frozen
Challenge header. No proof is supplied by those diagnostic definitions; neither
proof module imports `Challenge.lean`.

| Frozen contract | Completed theorem in `NLA.IE05` |
| --- | --- |
| `entryMax_semantics` | `entryMax_semantics_proved` |
| `schurStep_bound` | `schurStep_bound_proved` |
| `gepp_growth_bound` | `gepp_growth_bound_proved` |
| `firstPath_semantics` | `firstPath_semantics_proved` |
| `orthogonalGrowthSet_bounded` | `orthogonalGrowthSet_bounded_proved` |

The first statement proves attainment of the actual entrywise maximum for every
positive dimension. The one-step bound concerns the actual row-swapped Schur
complement, including its zero-padded inactive entries. The growth theorem
quantifies over **every admissible path**, with no determinant assumption added:
`0 < entryMax A`, `1 ≤ growth A path`, and the genuine bound `2^(n-1)` all follow.
The first-path theorem requires exactly the reviewed `A.det ≠ 0` and holds for
all dimensions, including zero, all natural-number stages, and every exact tie.
The final result proves nonemptiness and boundedness of the actual orthogonal
growth set, which will justify use of the real supremum in the later conclusion.

## Actual proof route and reusable interfaces

`Pivot.lean` proves that the frozen fold implements Mathlib's first-occurring
`List.argmax` for an active-row score. Genuine maximum and list-index lemmas
establish both maximal magnitude and the least current row among ties. The
following suffixed interfaces are retained exactly for later LU integration:

- `firstPivotIndex_spec_proved`: active selection, maximum, and least tied row,
  even when the whole active column vanishes.
- `firstPivotIndex_eq_of_firstAvailable_proved`: any row satisfying the frozen
  independent first-available specification equals the scan result.
- `firstPivotIndex_firstAvailable_proved`: an actual nonzero active column makes
  the scan admissible.
- `trajectory_firstPath_eq_proved`: equality of the two actual recursive state
  definitions for every natural-number stage.
- `firstPath_eq_of_firstAvailable_proved`: an already valid first-available path
  equals `firstPath`, without an unnecessary determinant premise.

`GEPP.lean` derives entry bounds and attainment from the frozen `Finset.sup`
over `NNReal`. A partial-pivot multiplier has absolute value at most one, so the
triangle inequality bounds the next active maximum by twice the previous one.
Induction and the actual finite maximum of all stages prove the all-path growth
bound.

Nonsingularity is maintained through `ActiveInjective S k`: vectors supported
on indices at least `k`, whose actual matrix-vector product vanishes in those
active rows, must vanish. The initial property follows from the genuine
nonzero-determinant/matrix-unit/injective-mulVec bridge. A zero active column
contradicts the supported coordinate vector. Row swapping preserves the
property. To transfer it through a Schur step, the proof extends a prospective
new kernel vector by the pivot coordinate `-(B *ᵥ x) k / B k k`, proves all
active equations, and applies the preceding invariant. Thus the zero-padded
full matrix is never incorrectly assumed nonsingular. The identity matrix and
its proved valid path supply an actual member of the orthogonal growth set.

No numerical intervals, eigendecompositions, shrinking determinants, or
exhaustive pivot-path enumeration are needed. This module pair uses LeanCert
for explicit kernel-trust auditing of exact algebra, not for an artificial
interval certificate.

## Observed checks and limits

The selected immutable successful check is
`verification/gepp-development/attempt-rwc8pqg6/result.json`, selected explicitly
by `final-run.json`. Fresh direct-source elaboration of Definitions, Pivot,
GEPP, and the admission-free inspector completed with four exit codes zero in
**20.743 seconds** on macOS 14.6.1 arm64, Lean 4.33.1. No old project objects were
used. The ten exact pinned dependencies were read from the existing MI-22 cache;
no Lake build, download, cache copy, or shared-cache mutation occurred. Cli has
source but no compiled artifact directory, and is not imported by this check.
All generated objects in the private prefix were hashed and removed.

The successful run contains **21** explicit `#assert_trust kernel` invocations
and **21** exact standard-three axiom reports: five in Pivot, eleven in GEPP,
and five in the inspector. The actual type/body traversal visits **70** safe,
nonpartial project declarations and checks **42** retained semantic/library
dependencies. Every transitive axiom closure is a subset of `propext`,
`Classical.choice`, and `Quot.sound`. There is no `sorryAx`, compiler/native
execution axiom, custom axiom, or reference-proof dependency. The mathematical
modules have no warnings. Six inspector-only unused-binder warnings arise from
retaining the exact frozen binder names in Prop-valued expected types; they are
not proof holes.

All failed development attempts remain intact. An inspector initially expected
the named theorem `Real.norm_eq_abs` to survive in the proof term; the actual
norm/absolute-value reduction is definitional, so that unsupported dependency
claim was removed from the diagnostic only. The full successful check was then
rerun. A raw-text source scanner was corrected to ignore a comment containing
“partial-pivot.” Both corrections and their original scripts are retained.

After the successful run, a brief attempt to add redundant nested-namespace
wrappers encountered a doc-comment/namespace syntax error. The coordinator
requested preserving the established suffixed interfaces, so both exact
mathematical files and the inspector were restored byte-for-byte to the
successful run. The discarded experiment, source snapshots, and diagnostic
remain retained; `latest.json` honestly records that last experiment, while
`final-run.json` identifies the successful run bound to the delivered bytes.
No redundant mathematical rerun was claimed after restoration.

`audit_result.py` independently rechecks the selected attempt's hashes, every
frozen source and original Git blob, dependency pins, exact-type results,
actual proof closure, retained attempt identities, and private-prefix cleanup.
The handoff's outer manifest includes all scoped evidence and nested manifests;
only its exact own path is excluded from its own listing. Future integration,
two independent full-proof referees, and actual Linux Comparator/default-kernel
verification remain coordinator-controlled later gates.

## Delivered mathematical hashes

- Pivot: `89a404945ce5fc2c04d06dd971f7a155d7ef1a48c3c331082bdea9df89dc6f69`
- GEPP: `f9cfa58bd03aa49748bfde358147197bf73b165701cb67b58e1af2ec926c8b98`
- Inspector: `7ebe5d8839736904ab897c305345cebd6382587c6ee29f135addc15a7e355df3`

For a new source check, run `compile.py Inspect` in a separate copy of this
project; keep this sealed evidence directory unchanged. Reproduction uses the
explicit toolchain, dependency paths, commands, and hashes recorded in the raw
result. `verify_seal.py` performs a read-only check of the delivered seal.
