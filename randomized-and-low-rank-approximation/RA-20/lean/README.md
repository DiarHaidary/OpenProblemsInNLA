# RA-20 Lean proof and accepted verification

The complete twelve-export proof **refutes the original joint critical-count
conjecture**: the genuine generic count at the allowed parameters `n=s=3` is
three, whereas its formula predicts four. Two independent final mathematical
reviews, independent candidate packaging and operational reviews, and the
[coordinator's accepted Linux verification](verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json)
support **Lean verified** status. Publication review and upstream integration
are separate from these accepted mathematical and Linux checks. This document
does not claim an upstream merge.

Formalization author: **George Stepaniants**, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA, with AI assistance. The original negative-resolution mathematics remains
attributed to the **Codex automated maintainer audit**. Kubjas, Sodomaco and
Tsigaridas retain credit for the original conjecture.

## Original target and exact scope

The immutable [canonical problem](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/randomized-and-low-rank-approximation/RA-20/README.md)
and [complete informal proof](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/randomized-and-low-rank-approximation/RA-20/solution.md)
are retained at source base `5830ed4fb06da0659414a3deb2a40ad327aca052`.
The target keeps all four formulas for every `n ≥ 3`, `1 ≤ s ≤ 4`, `s ≤ n`.
The counterexample negates this full universal assertion; it does not separately
settle the other parameter formulas or provide a corrected sequence.

[Definitions](NLA/RA20/Definitions.lean) uses actual complex symmetric matrices,
rank at most two and all prescribed diagonal zeros. Its reduced coordinate
ring is the quotient by **all** polynomials vanishing on that matrix variety.
Smoothness means the actual point prime belongs to Mathlib's algebraic smooth
locus; tangent directions annihilate the differential of every polynomial in
the entire vanishing ideal. Neither predicate is defined by the desired
three-coordinate answer, a chosen component, or the rank-two stratum.

The objective is `∑ i, ∑ j, (X i j - U i j)^2`, the complex bilinear full-entry
Frobenius distance, without conjugation. Actual complex Fréchet derivatives
and second derivatives are proved. Both off-diagonal entries contribute, and
data diagonals remain unrestricted. The count is `Cardinal.mk` of the actual
smooth critical-point subtype. Genericity permits an arbitrary exceptional
polynomial nonzero somewhere on the full symmetric data space; intersection
with the constructed generic open is proved, not presumed.

## All twelve exported declarations

Every name below has prefix `NLA.RA20.` and is exported by
[Solution](Solution.lean). [Comparator configuration](comparator.json) selects
all twelve, with no replaceable definition holes and only the standard three
foundational axioms. [The proof map](PROOF_MAP.md) gives the module-level route.

| Declaration | Proved mathematical content |
| --- | --- |
| `hollow_variety_semantics` | The actual determinant is `2abc`; the full matrix variety is exactly the hollow matrices with `abc=0`. |
| `reduced_coordinate_ring` | Coordinate-preserving equivalence of the original reduced matrix ring with `ℂ[a,b,c]/(abc)`. |
| `algebraic_smooth_locus` | The genuine algebraic smooth locus consists precisely of hollow points with exactly one zero coordinate. |
| `algebraic_tangent_space` | The entire-ideal tangent space has the symmetry, zero-diagonal and `bc Z01+ac Z02+ab Z12=0` equations, including singular points. |
| `full_frobenius_differential` | The actual complex derivative is `2∑ij(Xij-Uij)Zij` for every matrix order. |
| `hollow_distance_semantics` | Restricting the full metric retains arbitrary diagonal constants and doubled off-diagonal squares. |
| `generic_critical_locus` | For every symmetric datum with nonzero off-diagonal product, the full smooth critical set is the injective range of the three projections. |
| `component_hessians` | Actual second derivatives in all three component charts give `4∑hᵢvᵢ` with zero radical, even for nonsymmetric data. |
| `generic_data_intersection` | Every nonempty principal open in the full symmetric data space meets the displayed generic set. |
| `generic_count_three` | A genuine nonempty generic open has actual smooth critical-subtype cardinality three. |
| `generic_count_not_four` | No competing nonempty generic open can have actual count four. |
| `not_criticalCountConjecture` | The complete original four-formula universal conjecture is false at its allowed case `n=s=3`. |

The reduced-ring bridge uses squarefreeness, the actual Nullstellensatz, a
surjective polynomial substitution and its proved kernel. Smoothness uses
ordinary localizations, algebra retractions and a square-zero lifting
obstruction at component intersections. The `abcLocalChart` source comment's
“complete local ring” wording refers to the entire ordinary local ring here;
**no adic completion or completeness theorem is constructed**. The exported
Hessian theorem proves nondegeneracy. No separate scheme-theoretic
intersection-multiplicity theorem is claimed; the canonical target counts
distinct generic smooth critical points.

## Reviewed evidence

[Numerical and mathematical targets](NUMERICAL_TARGETS.md), the unchanged
[Challenge](Challenge.lean) and Definitions were fixed before implementation.
The [statement freeze](reviews/statement-freeze.json) binds 68 project inputs
and 16 original source/policy identities; the [proof-start gate](verification/proof-start.json)
accepted two independent statement reviews before proof work began.
Challenge's twelve deliberate reference admissions are not part of the proved
development and are never imported by Solution.

The [complete proof freeze](verification/proof-freeze.json), SHA-256
`f66dfe47527df937de8ed399606206bdaef55717cef8d68808f60834aece0c6f`,
binds 521 proof/evidence files and the same 16 originals. The
[author completion](reviews/proof-completion.md) records all twelve contracts.
The mathematical reviewers are fresh agents distinct from all proof authors:

| Reviewer | Actual local check and verdict |
| --- | --- |
| [Final referee 1](reviews/final-referee-1.md), `/root/ra20_final_referee1` | APPROVE; 13 fresh source commands, twelve exact types, 236 project declarations audited, 214 in the actual export closure and 39 material dependencies. |
| [Final referee 2](reviews/final-referee-2.md), `/root/ra20_final_referee2` | APPROVE; 13 fresh source commands, twelve exact types, 214 actual closure declarations and 28 separately selected material dependencies. |

Each final referee's successful logs contain 69 standard-three printed axiom
reports: 57 from the proof sources and twelve from its separate inspector.
Each passed 61 source and twelve additional LeanCert kernel assertions; four
source assertions do not print reports. Both recompiled eleven mathematical
source modules plus their separate reference and inspector in fresh private
prefixes, with ten exact dependencies reused read-only and no old target
objects. These are **local macOS checks**, not the authoritative Linux gate.
The author assembly likewise records thirteen successful commands and 69
reports; its initial failed Count attempt and all earlier development
diagnostics remain retained.

The accepted [final-review gate](verification/final-review-acceptance.json)
has SHA-256 `a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb`.
The [independent candidate packaging review](reviews/candidate-packaging-referee-2026-09-13.md)
preceded the committed candidate. After its independent mathematical review,
`/root/ra20_final_referee1` authored the candidate documents and later these
publication documents; that author role adds no
independent approval of its own packaging or publication.

## Actual Ubuntu verification - 13 September 2026

[Immutable proof revision](https://github.com/sgstepaniants/OpenProblemsInNLA/tree/43603b173beb294c2588d83f936a8a96246fd5f0/randomized-and-low-rank-approximation/RA-20/lean)
`43603b173beb294c2588d83f936a8a96246fd5f0` passed
[run 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047),
attempt 1, on non-root Ubuntu 24.04. All 17 workflow jobs succeeded, including
the RA-20 job and separate checker-controls job. The actual default Lean kernel
replayed the exported solution, and the real Comparator matched all twelve
frozen contracts with no definition exceptions. This catalog ran that Linux
workflow and reviewed its original artifacts; no local macOS Comparator
execution is claimed.

The actual source build passed **61 LeanCert kernel assertions** and printed
**57 axiom reports covering 45 distinct declaration names**. Every report
contains only `propext`, `Classical.choice`, and `Quot.sound`. The additional
twelve diagnostic prints in each earlier local review account for its 69
reports and are not part of the authoritative source run. Challenge's
deliberate reference admissions are isolated from Solution.

Both the standalone checker and RA-20 preproof controls passed: two sandbox
modes, four unsupported-option rejections, three raw default-kernel controls,
five Comparator fixtures and two forbidden-axiom controls. The invalid proof,
quotient mismatch, statement/kind/helper mismatch, `sorry` and native-execution
fixtures fail at their intended gates. In the nested-namespace check, bwrap
ran but UID-map setup was denied before the inner write; no executed inner
write syscall is claimed. The original control and isolation logs are retained.

The fresh project compiled the proof using all ten pinned dependencies and
**8,690 official matching Mathlib cache files**. This was not a from-source
rebuild of all Mathlib. The toolchain, dependency objects, trusted Challenge,
exporter, default kernel and checker infrastructure remain the disclosed trust
boundary. Exact algebra removes numerical interval computations.

The [independent operational report](reviews/linux-operational-referee-2026-09-13.md)
and [complete original runtime evidence](verification/linux-run-2026-09-13/runtime-verification.json)
bind all **1,092 candidate Git inputs**, every artifact and all source/line
axiom records. The operational seal has 1,589 entries. The coordinator rechecked
and accepted it in the [root acceptance](verification/root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json),
SHA-256 `a2c3a74eb858edb859d34d8bd2985dc54710e31816412d285c32a547e080e57e`;
its complete seal binds 1,604 files. These are accepted mechanical verification
results, not an additional independent mathematical approval.

The exact earlier [statement-stage README](verification/pre-candidate-README.md)
is archived with SHA-256
`7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50`.
It, [SourceCorrespondence](SourceCorrespondence.md), PROOF_MAP and frozen source
phase notices retain their dated descriptions. This README and the accepted
gates supply the current status without rewriting those historical records.
The [candidate installation record](verification/linux-candidate-2026-09-13/HANDOFF.md)
is a dated record. The exact checked candidate
[README](verification/publication-preparation-2026-09-13/archive/candidate-README.md)
and [metadata](verification/publication-preparation-2026-09-13/archive/candidate-formalization.yaml)
are now archived at their original SHA-256 values. The
[publication handoff and read-only verifier](verification/publication-preparation-2026-09-13/HANDOFF.md)
check every historical manifest with strict exact-path plus expected-hash
archive mappings, including both old README versions and the canonical page.
No proof, frozen statement, dependency pin or previous review/evidence file
was changed for publication. Older pending-phase notices are superseded by the
accepted gates and this current documentation.

## Pinned tools and reproduction

The toolchain is **Lean 4.33.1**, with Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`. All ten exact package revisions are
in [lake-manifest.json](lake-manifest.json). LeanCert's role here is actual
`#assert_trust kernel` auditing. Exact polynomial algebra, localization,
calculus and finite cardinality eliminate interval computations, numerical
root searches and artificial singleton certificates. No native execution
axiom or unproved literature premise supports the exports.

For an ordinary developer check, from this `lean/` directory with the pinned
dependencies prepared, explicitly select Solution:

```
lake build Solution
```

The historical Lake default still selects Challenge, so a bare `lake build`
is not the proof check. The retained fresh direct-source reviewer logs describe
their actual method; candidate-document and publication preparation ran no new Lean build.

To reproduce the accepted run, use a clean checkout of immutable revision
`43603b173beb294c2588d83f936a8a96246fd5f0`. Run the authoritative commands
**from the repository root on non-root Ubuntu**, with the
[Linux prerequisites and isolation](../../../tools/lean/HARNESS.md) ready:

```
tools/lean/bootstrap.sh /tmp/nla-ra20-check
tools/lean/selftest.sh /tmp/nla-ra20-check
tools/lean/verify.sh \
  randomized-and-low-rank-approximation/RA-20/lean \
  /tmp/nla-ra20-check
```

These are the repository commands whose actual Linux workflow result is
recorded above. They use the pinned exporter/default kernel and
[Lean Comparator](https://github.com/leanprover/comparator), real isolation and
the complete rejection/control suite. Publication of the canonical
Markdown/TeX/PDF, metadata and indexes is reviewed separately from the immutable
proof. Submission and upstream merging do not follow from kernel acceptance
alone; no upstream merge is claimed here.

[formalization.yaml](formalization.yaml) uses the pinned
[v0.4 metadata schema](../../../docs/lean/schema/README.md); schema validation
checks metadata consistency, not mathematical truth. The workflow follows
the repository's [Tau Ceti adaptation](../../../docs/lean/REVIEW.md), with
statement/proof organization examples from
[Schiffer](https://github.com/jaumededios/Schiffer/tree/2938e277969c329caf154e48a3d8823f3635c7f1)
and [Forsythe](https://github.com/sgstepaniants/Forsythe/tree/8d1b0c0545a77b40245e84705aa7d273e6c81e62/lean-proof).
No mathematical theorem from those projects is assumed. No external human
review, official Tau Ceti endorsement, source-author endorsement or priority
claim is added.
