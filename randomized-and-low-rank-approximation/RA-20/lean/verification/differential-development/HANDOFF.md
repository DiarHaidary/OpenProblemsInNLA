# RA-20 differential helper completion

Contracts **5, 6 and 8** are proved in `NLA/RA20/Differential.lean`, SHA-256
`8e24af9b30b668fd1c6bfc3799fe6d8771e4a6e96124087752a02f7b4d913ec7`.
The exact exports, all in `NLA.RA20`, are:

- `full_frobenius_differential_proved`;
- `hollow_distance_semantics_proved`;
- `component_hessians_proved`.

The coordinating proof-start gate preceded every implementation attempt. Its hash
is `9fe55d622e50390cb3ed439989b9393455fa48eb50d42d84fb33c20fd8c883f3`;
the role record is `a81af5049b95b824f36043bf78619a68ee14579923a11a1f4a97dad8004a09cf`.
All 68 frozen project inputs and 16 original source snapshots and Git blob
identities remain exact. The frozen statements, definitions, canonical entry,
metadata and Git were not changed.

## Mathematical content

A finite sum of squared affine complex linear functionals has an explicitly
proved Fréchet derivative. The gradient is itself a function valued in actual
continuous linear maps; differentiating this function proves the genuine second
Fréchet derivative. Both calculations reach Mathlib's derivative rules in the
actual proof terms. Specializing to the two matrix coordinate projections gives
contract 5 for every natural `n`, including zero, and every `U`, `X`, `Z`.
The proof locally equips matrices with the ordinary finite product norm needed
by the calculus API. This does not alter the frozen derivative type: the
elaborated contract comparison passes exactly.

Expansion over the nine entries of a complex symmetric 3-by-3 matrix proves
contract 6. Diagonal terms remain, and each off-diagonal square is counted twice.
No complex conjugation or Hermitian objective is substituted.

Each of the three actual component charts is expressed through continuous
linear entry maps. The general second derivative yields the bilinear Hessian
`4 * ∑ j, h j * v j`. Testing against each coordinate vector proves that its
radical is zero. Contract 8 assumes no symmetry of `U` and holds for every chart,
base point and pair of directions. The proof does not define a derivative to be
this formula or use a premise asserting differentiability or nonsingularity.

The helper depends on frozen `Definitions.lean`, Mathlib calculus and finite
algebra only; it imports neither `Smooth.lean` nor `Algebra.lean`. The finite
quadratic lemma avoids repeating the derivative calculation for the charts.
This is exact symbolic calculus; no interval or numerical certificate is added.

## Validation and retained attempts

The helper was compiled directly from source using Lean 4.33.1 in one initially
empty private prefix. The exact ten-package MI-22 dependencies were read-only;
all pinned revisions and clean source statuses were checked before and after.
No Lake build, dependency copy, cache download or shared-cache modification was
performed. The final helper compile took approximately 5.8 seconds locally.

Four successful commands compiled frozen Definitions, the final helper, a
namespace-only diagnostic copy of frozen Challenge, and the diagnostic inspector.
All three actual elaborated theorem types match the frozen reference types.
The inspector traversed the actual types and bodies of 45 safe project
 declarations, rejecting admissions, unsafe or partial project declarations and
nonstandard transitive axioms. Sixteen actual mathematical dependencies were
required and retained. Three source and six diagnostic LeanCert `#assert_trust
kernel` assertions and matching axiom reports passed. Their only foundational
axioms are `propext`, `Classical.choice` and `Quot.sound`; no native-compiler
axiom is accepted. The diagnostic admitted reference is absent from actual
proof dependencies.

Every source attempt, runner snapshot and raw log is preserved. Three initial
implementation attempts failed on Lean calculus/instance/projection or finite
simplification interfaces; their corrections are present in the final helper.
The first inspector attempt wrongly required the reflexive `matrixEntry_apply`
lemma to survive elaboration. Lean reduced that equality definitionally; the
corrected inspector requires the actual `ContinuousLinearMap.proj` dependency.
No implementation changed for that diagnostic correction. The final helper's
two remaining warnings are nonblocking style suggestions to replace `letI`
with `let`. Reference admission warnings are intentionally diagnostic.

`validation.json` binds the counts, source hashes, gate, prior nested inventories
and honest platform scope. `owned-prefix-cleanup.json` records every generated
object and hash before removal of this author's completed private prefix. All
logs and source evidence are retained. `EVIDENCE-MANIFEST.json` binds the complete
helper evidence and its frozen input closure, excluding only that exact manifest
from its own inventory; `verify_seal.py` rechecks the seal without a rebuild.

## Roles and remaining work

Implementation and these helper diagnostics: `/root/mf16_final_referee`.
This role is an RA-20 proof contributor, hence ineligible as an independent final
mathematical referee for the completed RA-20 project. This handoff is not an
additional independent mathematical approval.

Formalization author: George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. No personal email is included. Original negative-resolution mathematics:
the repository's Codex automated maintainer audit. Original conjecture:
Kubjas, Sodomaco and Tsigaridas.

Full RA-20 integration, its other nine contracts, two independent final
mathematical reviews, authoritative Linux replay, Lean4 Comparator and controls,
operational review and publication remain pending. This evidence records local
macOS work only and makes no Linux or Comparator claim.
