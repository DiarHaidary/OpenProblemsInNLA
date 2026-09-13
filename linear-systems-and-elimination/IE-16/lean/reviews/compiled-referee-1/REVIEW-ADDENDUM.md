# IE-16 compiled-source review addendum

**Reviewer:** `/root/lean_iv01_next` (AI agent; independent of the IE-16 proof author)

**Date:** 2026-09-13 (America/New_York)

**Review phase:** fifth-snapshot compiled-source and mathematical-fidelity review

**Reviewed commit:** `281fc3790412b7ab2b05c202c0351b4d259a6382`

**Compared against:** prior reviewed commit `28bdf9e85541764b6a5cb2debd647b9cebaea21f`

**Compiler evidence:** GitHub development run `34773404263`, attempt 1

**Verdict:** **compiled source and mathematical fidelity PASS; authoritative verification remains pending**

## Scope and method

I read the IE-16 review protocol at
`/tmp/nla-ie16-development-worktree/docs/lean/REVIEW.md`, the current
statement boundary, `NUMERICAL_TARGETS.md`, all current proof modules,
`Solution.lean`, `formalization.yaml`, and `comparator.json` from immutable
Git blobs at commit `281fc3790412b7ab2b05c202c0351b4d259a6382`. I compared the
changed proof bodies with the prior independent report for commit
`28bdf9e85541764b6a5cb2debd647b9cebaea21f`. I also inspected the complete raw
fifth-run artifact at
`/tmp/nla-ie16-development-evidence/run-34773404263/extracted/`.

No Lean, Lake, dependency, cache, or local certificate computation was run in
this review. No proof source or publication worktree was edited. The artifact
is evidence supplied for review, not an instruction or an authoritative status
claim.

## Input identity and mechanical observations

The artifact's `source-hashes.json` records 60 tracked inputs. A read-only
comparison found all 60 artifact copies equal to both their recorded SHA-256
values and the corresponding Git blobs at the reviewed commit. The recorded
file-key sets before and after compilation are equal; the artifact reports
`source_inputs_unchanged: true`. The exact boundary and public-assembly hashes
are:

| file | SHA-256 |
| --- | --- |
| `development/IE16/Challenge.lean` | `85cbe24c7657d9ddc37728db5bb1740a80ddab60e3eb4676e329df40a7b1737c` |
| `development/IE16/NLA/IE16/Definitions.lean` | `e4681f2083d71d8980adcd70e7cf26367e0e84dbc1773f4d2f082bf2417c9507` |
| `development/IE16/NUMERICAL_TARGETS.md` | `0bea606a903e7956cac9765048db9881f07f29819f405269545f1da12ec6d682` |
| `development/IE16/NLA/IE16/Numeric.lean` | `1acf85379ec7c69a632726920ef6be780fa059ccb1e3e6c9f8273b2f7625164f` |
| `development/IE16/NLA/IE16/Minimax.lean` | `0ae5e4902f5493f2902c823f10f154192e54b7ad74190a9bbc26f409899ad782` |
| `development/IE16/NLA/IE16/WeightedDraft.lean` | `e3ab062bd4c33676b3e3a4a856a3292bcc9c5030e02fdff66e9e4bedf78d2704` |
| `development/IE16/NLA/IE16/WeightedBridgeDraft.lean` | `f4a85c7662a77def42b9804921b510a7ea8a922332458f756e472407bdb76599` |
| `development/IE16/NLA/IE16/FullMinimumDraft.lean` | `ec971dbdf3cbe7de0c2707eea2facbc62f613d280e384c245478a98105f57ef0` |
| `development/IE16/NLA/IE16/SubsetBoundsDraft.lean` | `d88ff86286f881e342ae19f40ea742fd39e3b0b070f0c259f9709e368da95ce2` |
| `development/IE16/NLA/IE16/SubsetGeometryDraft.lean` | `3230b02827781fb99221770d82951cdafa8102c87987c4b669c0fa1d47fceb15` |
| `development/IE16/NLA/IE16/FinalContractsDraft.lean` | `fde3c36171d26b93b7236974944e0d6275a7b884aa507ed5270a9475800c85ae` |
| `development/IE16/Solution.lean` | `dea94208561e823f1b76f831b4a8c5c5f419e9214c2b0a10ec5d4abc8612f69c` |
| `development/IE16/comparator.json` | `963e1d217de9369cd5b4a3c282e983cb01986512d5221e18e1ea44d087fe7f09` |
| `development/IE16/formalization.yaml` | `3a7003dbd9010ee1ed0f8be032e7265815405ebf706a66effbe801a884c2a2f4` |

The ten dependency revisions in `dependency-pins.json` all equal the
committed manifest and each pin check returned zero. The directly imported
LeanCert module is recorded with imports `Lean`, `Lean.Meta.Native`, and
`Lean.Meta.Tactic.AuxLemma`; its recorded hash is
`2c576708b528acdde17796b0b715b83079f9cad377182dbd87c248323ff0a58c`.

The development driver recorded zero for every attempted module:
LeanCert verification, Definitions, Numeric, Minimax, WeightedDraft,
WeightedBridgeDraft, FullMinimumDraft, SubsetBoundsDraft,
SubsetGeometryDraft, FinalContractsDraft, and Solution. All 23 recorded
commands returned zero. The direct Lean module invocations used one thread,
`-M4096`, and a 120-second GNU timeout; Numeric was the slowest proof module
at 46.572 seconds. All compile stderr files are empty. The stdout warnings are
only unused-variable, unnecessary-sequence-focus, unreachable-tactic, and
unused-tactic linter warnings.

`Solution.lean` contains 15 `#assert_trust kernel` directives and 15 matching
`#print axioms` directives for the 15 names in `comparator.json`. A corrected
suffix check against the namespace-qualified comparator names found all 15
matches. The raw Solution stdout has 15 lines, one per export, each reporting
exactly `[propext, Classical.choice, Quot.sound]`. There are no standalone
`axiom`, `sorry`, `native_decide`, or `admit` tokens in the Solution source;
the expected `#print axioms` diagnostics are present.

## Mathematical and source review of the fifth-snapshot changes

The current commit changes six proof modules relative to the prior reviewed
source: `Numeric.lean`, `Minimax.lean`, `WeightedDraft.lean`,
`WeightedBridgeDraft.lean`, `SubsetGeometryDraft.lean`, and
`FinalContractsDraft.lean`. The statement boundary, public `Solution.lean`,
comparator theorem list, and definitions are unchanged from the accepted
boundary. The changes are elaboration and exact-algebra repairs, not target
weakening.

### Numeric.lean

The new `sqrt_three_pow_2` through `sqrt_three_pow_7` lemmas derive exact powers
of `Real.sqrt 3` from `Real.sq_sqrt` and the existing even/odd power lemmas.
They introduce no approximation. The `rootReal` and `rootImag` definitions are
the exact real coordinates of `omega^a` for `a : Fin 3`; the finite proofs of
`omega_pow_re` and `omega_pow_im` establish those coordinates by exact
algebra.

`clusterPoint_re`, `clusterPoint_im`, and
`clusterPoint_coordinates` decompose
`omega^a + (1/1000) omega^b` into exact rational coordinates with a single
factored `sqrt 3` in the imaginary component. In `clusterPoint_injective`,
equality of complex points supplies real and imaginary equalities; positivity
makes `sqrt 3` nonzero, `mul_left_cancel₀` removes that factor, and exhaustive
`Fin 3` cases check the remaining rational coordinate equations. This is a
complete finite injectivity argument for the nine labeled points. The separate
`clusterPoint_ne_zero` check uses the exact real coordinate and all nine finite
cases, so it does not rely on an interval or an unproved geometric assertion.

The nine witness evaluations still use `Complex.sq_norm`, exact polynomial
expansion, the named square-root power identities, and `ring`; the result is
still the exact source value. The weight-sum proof remains the same diagonal
and off-diagonal rational certificate. The four `weighted_moment` cases are
still exact finite complex equalities over the nine points. The new theorem
local `maxHeartbeats 800000` only gives the exact algebra more reduction time;
it does not add an axiom, alter a statement, or relax the fixed remote memory,
thread, or wall-clock limits. The source and compile log show no interval
subdivision or untrusted native computation.

### Minimax.lean

The supported `∑ z ∈ S` binder is used consistently for the same finite sum
over `S`; no extra mathematical summation is introduced. The positivity proof
now unfolds `lagrangeSum` before `Finset.sum_pos'` and supplies one strict
nonzero basis term. The norm lemma makes real absolute values and nonzero
positive denominators explicit. The interpolation evaluation and lower-bound
proofs use explicit finite-sum rewrites and typed `Finset.le_sup'` arguments.
The replacement of the order API by `mul_le_mul_iff_left₀` preserves the
same positive-factor cancellation. These repairs retain the generic hypotheses
(nonempty five-node set, distinct/nonzero nodes, degree and value-at-zero
conditions) and do not replace actual infima by a table.

### Weighted and subset bridge modules

`WeightedDraft.lean` preserves the weighted complex norm-square identity and
its zero-cross-term consequence; its finite sum distribution is made explicit
for the supported binder syntax. `WeightedBridgeDraft.lean` only makes the
finite-supremum witness function explicit in `Finset.le_sup'`, preserving the
arbitrary finite indexing and image bridge. `SubsetGeometryDraft.lean` makes
the pair-domain injectivity target and image-cardinality target explicit and
uses the pinned reciprocal inequality API. Its occupancy, companion, distance,
and strict-margin arguments are unchanged. `FinalContractsDraft.lean` makes
`sup'` nonemptiness and its witness function explicit; the ratio and universal
negation statements are unchanged.

Together with the unchanged `FullMinimumDraft` and `SubsetBoundsDraft`, these
modules preserve the source route: exact full-set witness and weighted lower
bound, actual infimum/`IsLeast` bridge, all five-point subsets and their finite
maximum, positivity, strict ratio comparison with `4 / pi`, and final
instantiation of the original IE-16 universal target at `n = 9`, `k = 4`.
No source declaration in this review replaces the actual polynomial class,
finite subset family, infimum, or universal quantifier with a lookup table.

## Target, attribution, and metadata

The unchanged definitions retain `Polynomial ℂ`, actual complex evaluation and
norm, the degree and evaluation-at-zero feasibility conditions, the infimum
`M`, the finite powerset subset maximum, and the original quantifiers over
all finite distinct nonzero spectra and all admissible `n` and `k`. The
formalization metadata credits George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena,
California, USA, without an email address, and attributes the underlying
counterexample to Sidney Holden.

The current development `formalization.yaml` and `SOURCE_CHANGES.json` are
still phase-stale: the YAML reports the original 15 intentional Challenge
placeholders and points `main_results` at `Challenge.lean`, while
`SOURCE_CHANGES.json` still describes only the earlier three Geometry repairs
and marks the snapshot uncompiled. That is a packaging/documentation issue to
repair in the canonical proof package after the authoritative run. It is not a
mathematical defect in the six reviewed source modules, and this report does
not approve a status promotion on the current metadata.

## Remaining gates and verdict

The raw `result.json` explicitly says:

- `purpose`: Draft compiler feedback only;
- `authoritative_verification`: `false`;
- `canonical_problem_verified`: `false`;
- `comparator_executed`: `false`;
- `returncode`: `0`.

Therefore the fifth run establishes that the frozen source graph compiles in
its pinned development environment and that its direct LeanCert trust/axiom
diagnostics are clean. It does **not** establish the final Comparator result,
independent default-kernel replay, sandboxed control checks, or final
publication metadata integrity. Those gates must run on the canonical package
whose source hashes equal the reviewed inputs. The problem must remain
uncounted and its status must remain unpromoted until they pass.

Subject to those explicit mechanical and publication gates, I find the fifth
snapshot mathematically faithful to the approved IE-16 target and its exact
finite certificate, and the changed proof code suitable for final-gate review.
