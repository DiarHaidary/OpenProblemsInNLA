# KE-04 independent statement review 2

**Verdict: APPROVE the exact statement boundary below. No mathematical change
is requested.** This approves the meanings and scope of the definitions and
contracts before proof implementation. It is not a proof approval or a claim
that KE-04 is Lean verified.

Reviewer: AI agent `/root/mf16_final_referee`, 13 September 2026. I had no KE-04
statement, design or proof contribution. I first read the original and current
canonical statements, the complete original and current Markdown proof, the
complete current TeX proof, Definitions, all 24 Challenge signatures,
NUMERICAL_TARGETS and SourceCorrespondence. I formed and recorded my own
mathematical judgment before reading the first independent review. The first
review was read only after my fresh type and definition checks passed. It supplies
no substitute for my independent approval.

## Mathematical findings

The complete canonical target is preserved: every natural `n,p`, every actual
real symmetric `A`, a full-column-rank `V`, every largest full iteration `s`, every
`1 ≤ k < j ≤ s`, independently chosen orthonormal bases at `k,j`, and every
`1 ≤ i ≤ (k-1)p`. Both spectral inequalities are strict. The full-prefix version
is a stronger theorem from the source manuscript, and the direction of its
separate implication to the canonical formulation is correct. The final target
does not assume occupancy, a spectral gap, endpoint separation, simple spectrum,
quadratic nonannihilation or a compatible Lanczos recurrence.

`Vec n` uses genuine real L2 Euclidean space. `act` is the library's actual matrix
action, and the block Krylov columns are exactly `A^r V` for `r < ell`; their
span, coefficient map, finite dimension and linear independence have their usual
meanings. All ambient spaces and subspaces are finite-dimensional, so `finrank`
does not silently substitute zero for an infinite dimension. A basis is precisely
an orthonormal frame with the correct span. Its existence and arbitrary-basis
invariance remain theorem conclusions, which prevents vacuity from an empty
custom basis interface.

The increasing spectrum is a reversal of Mathlib's actual decreasing self-adjoint
spectrum. I checked the pinned `eigenvalues`, matching `eigenvectorBasis`, their
antitone order and eigenvector equation, and the characteristic-root multiset
identity. `OrthonormalBasis.reindex` evaluates the inverse equivalence, and
`Fin.revPerm` is an involution, so both reversals agree. The contract uses a
multiset of characteristic roots, not a set, and therefore preserves algebraic
multiplicity. The auxiliary equality of whole ordered spectra is required for
arbitrary equal-span orthonormal frames.

The substantive quadratic argument is faithfully stated. `compressedQuadratic`
is `Q q(QᵀAQ) Qᵀ`, with `q(t)=(t-a)(t-b)`, so it lifts the subspace polynomial by
zero on the orthogonal complement. Applying `q` to the ambient zero-extended
first compression would add an extraneous `ab(I-P)`; that is not the definition
here. The earlier and later quadratic **forms**, not their squared actions, are
equated on `K_(k-1)`. Symmetry makes each form equal to
`‖Ax‖²-(a+b)⟪x,Ax⟫+ab‖x‖²`. Only the later action is identified with `q(A)x`,
because it contains `x,Ax,A²x`; that identity correctly does not need symmetry.

The source contradiction is complete at the level of obligations: a gap makes
the later quadratic PSD; a window of `p+1` indexed eigenvectors gives a
nonpositive earlier form on a subspace of that dimension; actual dimension and
nesting force a nonzero intersection with `K_(k-1)`; equal forms and the PSD kernel
criterion give a zero later action; and the monic degree-two leading coefficient,
together with full block rank through `k+1`, forbids annihilation. Each existence,
transport and nonannihilation step is a conclusion to prove, not hidden input data.

## Every contract

All names have prefix `NLA.KE04.`. I checked each source signature; a fresh Lean
inspector also compared its actual elaborated type with a separately elaborated,
proof-free proposition generated from that exact reviewed signature.

| Contract | Independent assessment |
| --- | --- |
| `real_matrix_semantics` | Correct transpose symmetry, coordinate matrix action and orthonormal-column equivalence over the real field. |
| `krylov_range_semantics` | Actual coefficient range and expansion, with the right `ell*p` upper dimension. |
| `krylov_nesting_and_shift` | Empty prefix, nesting and one-power propagation are consequences of the actual powers. |
| `fullBlockDimension_iff_independent` | Correct finite-family rank equivalence and identification of starting rank at iteration one. |
| `fullBlockDimension_prefix` | Correct restriction to every earlier prefix, including coefficient injectivity as a conclusion. |
| `lastFullBlockIteration_exists` | Positive width is necessary; full starting rank supplies iteration one and finite ambient dimension bounds all full iterations. |
| `krylovBasis_exists` | Correct orthonormal basis existence at exactly the full dimension. |
| `frameProjection_semantics` | Hermitian idempotence, exact fixed space and orthogonal residual characterize the genuine projector. |
| `compression_semantics` | Correct compression and representation of the projected action on the subspace. |
| `orderedSpectrum_semantics` | Increasing genuine spectrum, matching eigenvectors, root multiplicities and valid natural indexing. |
| `compression_basis_independent` | Correct orthogonal similarity, characteristic polynomial equality and full ordered spectrum equality. |
| `interval_index_validity` | Both endpoints are in range; `k≥2` and `p>0` follow from the original index constraints. |
| `quadratic_semantics` | Genuine monic degree two, actual polynomial evaluation and correct expanded matrix expression. |
| `spectral_gap_quadratic_psd` | Correct spectral sign implication for weakly ordered endpoints, including equality. |
| `spectral_window_subspace` | `p+1` indexed orthonormal eigenvectors give this dimension even with repeated eigenvalues; sign is a conclusion. |
| `krylov_intersection_nonzero` | Correct nonzero intersection from the codimension `p` calculation; no vector is assumed. |
| `psd_zero_form_iff_kernel` | Correct for singular as well as nonsingular PSD matrices. |
| `compressedQuadratic_semantics` | Genuine congruence transports forms and PSD; no unnecessary symmetry or frame assumption. |
| `quadratic_forms_agree` | Correct equality of forms on the previous prefix, using symmetry and common first action. |
| `later_quadratic_identity` | Correct containment of both powers through `A²x`, without an unnecessary symmetry premise. |
| `fullRank_quadratic_nonannihilation` | Nonzero leading coefficient survives a monic quadratic inside the full-rank powers through degree `k`. |
| `strictIntervalOccupancy` | Complete stronger full-prefix theorem with original dimensions, bases and strict index bounds. |
| `fullPrefix_implies_canonical` | Correct reduction to the original largest-iteration convention. |
| `blockLanczosConjecture` | Complete canonical target with no extra mathematical premise. |

## Degenerate cases and nonvacuity

For `p=0`, all full dimensions are zero and there is no largest full iteration;
the existence lemma correctly requires `p>0`. The full-prefix target still
includes `p=0`, but then its index range is empty. It is also empty at `k=1`.
When `n=0`, a positive-width full-column-rank block is impossible. These extensions
do not narrow the original positive-dimensional target.

At the upper boundary `i=(k-1)p`, the upper zero-based endpoint is `kp-1`; at the
lower boundary it is still valid. Neither endpoint can use the total helper's
out-of-range zero value. At `k=2` the nonzero vector is in the starting block and
the proof needs powers through two; at `k=s-1,j=s` it needs exactly full rank at
`k+1=s`, not beyond `s`. If `a=b`, the same PSD/annihilation argument applies to
`(t-a)²`, so equality of endpoints is contradicted rather than excluded by a
hypothesis. Repeated eigenvalues within the allowed multiplicity remain included.

For a direct nonvacuity check, take the symmetric three-vertex path matrix
`A=[[0,1,0],[1,0,1],[0,1,0]]` and `V=e₁`. Its first three Krylov columns are
`e₁,e₂,e₁+e₃`, which are independent. Thus `s=3`, and `k=2,j=3,i=1` is admissible.
The earlier spectrum is `{-1,1}` and the later spectrum is `{-√2,0,√2}`, giving
actual strict occupancy. Block diagonal copies give arbitrary positive widths
and repeated Ritz values. This is a mathematical reviewer sanity check, not a
Lean theorem or evidence replacing the universal proof.

## Exact boundary and source identities

| Input | SHA-256 |
| --- | --- |
| `STATEMENT-HANDOFF.md` | `f46ec1cb54a9eed22dd7fc2cf640531be64b2ec86d48251d09075a64e94fa8a9` |
| `DRAFT-INVENTORY.json` | `e82c391cc2d8d3ad1ee12e4f19266e2495e469e4b39272d31697a2e4a873a9fa` |
| `NLA/KE04/Definitions.lean` | `ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4` |
| `Challenge.lean` | `a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e` |
| `NUMERICAL_TARGETS.md` | `ad963526a371cdfee8eaaf179674d5cabd2a1d5a9ae5b123c96ac2f2b4271c47` |
| `SourceCorrespondence.md` | `399f28847f52a6c5ff309a25b9501c0c6d4bd5a76892de2f5adaa9c25fe80a00` |

Before my writes, I verified the exact 1,468-file existing project membership:
the original 168-file author boundary, first review, all its evidence and its
outer inventory. `prior-boundary.json` records every one. Subsequent integrity
checks retain that exact historical membership and require every old byte to
match; they do not incorrectly require an earlier whole-tree inventory to include
my later additions.

My batched read-only provenance audit independently retrieved all 17 original
Git files at their specified commit/path identities and all 20 Git-backed API
reference files. The 13 remaining Tau Ceti snapshots were checked against their
blobs and seven independently reconstructed Git trees, including the commit's
actual root tree. Thus all 33 selected references are bound. Original and current
theorem/proof blocks match exactly: 2,622 bytes, SHA-256
`3ba1bd9a62a00aaf787758af6312e4787ca8d6db02b4487e8b956ce0553977a7`.
The canonical status at the reviewed base `5830ed4fb06da0659414a3deb2a40ad327aca052`
is Solved and its permanent registry path is unchanged. This audit does not claim
a new live literature, fork or PR search; the author's bounded eligibility
evidence remains separately retained.

## Actual independent Lean evidence

My single fresh attempt is
`reviews/statement-referee-2-evidence/attempt-o6p9csbt/result.json`.
Definitions, the definition-only inspector, Challenge and the type inspector
all compiled successfully from private immutable source copies. The output
prefix began empty. The definition inspector imports only Definitions, the
specific built `LeanCert.Tactic.Verification` module and a Lean traversal utility;
it does not import Challenge.

The run executed 27 actual `#assert_trust kernel` commands and 27 axiom reports.
Every actual definition and each of the 33 declarations in its project
type/body closure is safe, nonpartial, has a body and has no transitive axioms
beyond `propext`, `Classical.choice` and `Quot.sound`. All dependencies were
traversed from the actual definitions, including six generated helpers.
The retained log contains their actual direct dependencies and fully explicit
definition values. The real matrix, span, rank, finite linear combination,
spectral theorem, reverse-index and polynomial dependencies are present.

The type inspector separately elaborates all 24 reviewed signatures as
`Prop`-valued definitions with no proof holes, then checks definitional equality
with every actual Challenge theorem type. Those proposition definitions have
only foundational axioms, and no actual target type calls another admitted
Challenge theorem. The full actual types are retained with `pp.all`. This is a
mechanical preservation check supplementing source-first mathematical review,
not an independent semantic certificate. Challenge emits exactly 24 expected
admission warnings. Its theorem bodies are never used as proofs or passed off
as trusted exports.

The host is macOS 14.6.1 arm64. Lean reports 4.33.1, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; the binary SHA-256 is
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.
All ten clean source pins were checked before and after; nine existing dependency
object directories were read directly, while Cli is source-only tooling here.
Mathlib is `0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert is
`621a43d7cf21f87872392a01e874f2f1dbddc926`. No Lake invocation, dependency copy,
download, rebuild or cache mutation occurred. All four own private objects were
hash-recorded and removed. All raw commands and outputs are retained; this
reviewer's fresh execution and provenance audit had no failures. Historical
author and first-reviewer failures remain untouched and are not counted as my
successful evidence.

## Tau Ceti scope, reuse and attribution

I applied the pinned NLA adapter and read Tau Ceti's common protocol and all ten
rubric angles. The relevant scope is this single permanent NLA target; Tau Ceti
roadmap admission, compatibility policy, namespace rules and service endorsement
are not imported. Existing actual Mathlib APIs cover coefficient maps, dimensions,
orthonormal bases, self-adjoint spectra and PSD kernels. I independently searched
and inspected those APIs. The semantic export bundles make this problem's audit
boundary explicit; they do not justify duplicating generic library proofs later.

The exact algebraic argument needs no numerical boxes or interval computation.
LeanCert's concrete use here is its explicit kernel trust assertion, whose pinned
implementation I read: it collects transitive axioms, rejects sorry/custom/native
axioms in kernel mode and succeeds silently. The Schiffer and Forsythe references
were inspected for Challenge/proof separation and target configuration. They are
not imported as KE-04 mathematical proofs. No implementation or licensing claim
is inferred from the unlicensed Schiffer example; the retained Forsythe license
and source identity remain intact.

Original mathematics remains attributed to Matthew J. Colbrook, Department of
Applied Mathematics and Theoretical Physics, University of Cambridge, including
the disclosed ChatGPT draft origin and earlier Codex informal review. Prospective
formalization is credited to George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA, with substantial AI assistance. No George email is added; exact historical
source metadata for its original author is preserved.

## Reproduction and remaining gates

`reviews/statement-referee-2-evidence/verify_inventory.py` checks the complete
hash-bound evidence and preserved prior memberships. Its default mode checks
only the sealed membership and permits later phase additions; `--strict` also
requires that its inventory still describes the entire current project. The
outer `EVIDENCE-MANIFEST.json` excludes exactly itself. The runner is retained
for reproduction, but another run would create new evidence and must not be
presented as covered by this historical seal.

This supplies the second independent statement approval, subject to the
coordinator accepting both exact reports and explicitly opening the proof phase.
No frozen source, prior review, canonical page, status, metadata, Git state or
dependency cache was modified. No solution proof, publication YAML, Comparator
execution, default-kernel export replay, non-root Linux sandbox or publication
approval is claimed. Those remain later gates for the completed formalization.
