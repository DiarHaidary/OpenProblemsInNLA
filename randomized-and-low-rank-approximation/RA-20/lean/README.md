# RA-20 Lean proof — Linux verification candidate

The complete twelve-export proof **refutes the original joint critical-count
conjecture**: the generic count at the allowed parameters `n=s=3` is three,
whereas the conjecture predicts four. Two independent final mathematical
referees approved the frozen proof, and the [coordinator accepted both
reports](verification/final-review-acceptance.json) on 13 September 2026.
**Canonical status remains Solved.** Independent candidate packaging review,
actual non-root Ubuntu Comparator/default-kernel/control verification,
independent operational acceptance and canonical publication are still pending.

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

## Statements, reviews and retained evidence

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
This documentation was subsequently prepared by `/root/ra20_final_referee1`.
That document-author role adds no independent mathematical or packaging
approval. A different reviewer must inspect this concrete installation before
a candidate commit and Linux run. No candidate Git revision or Linux run is
asserted at this stage.

The exact earlier [statement-stage README](verification/pre-candidate-README.md)
is archived with SHA-256
`7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50`.
It, [SourceCorrespondence](SourceCorrespondence.md), PROOF_MAP and frozen source
phase notices retain their dated descriptions. This README and the accepted
gates supply the current status without rewriting those historical records.
The [candidate installation record](verification/linux-candidate-2026-09-13/HANDOFF.md)
and its verifier preserve the complete prior inventory through that one
archived README; historical manifests bind their original version.

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
their actual method; this candidate-document task ran no new Lean build.

After independent packaging review and a clean committed candidate, run the
authoritative commands **from the repository root on non-root Ubuntu**, with
the [Linux prerequisites and isolation](../../../tools/lean/HARNESS.md) ready:

```
tools/lean/bootstrap.sh /tmp/nla-ra20-check
tools/lean/selftest.sh /tmp/nla-ra20-check
tools/lean/verify.sh \
  randomized-and-low-rank-approximation/RA-20/lean \
  /tmp/nla-ra20-check
```

These commands are **pending**, not a report of execution. They must use the
actual pinned exporter/default kernel and [Lean Comparator](https://github.com/leanprover/comparator),
real isolation and the complete rejection/control suite. Independent
operational review and reviewed canonical Markdown/TeX/PDF/index changes must
follow before any `Lean verified` status or upstream publication claim.

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
