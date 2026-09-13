# KE-04 independent statement review 1

**Verdict: APPROVE the exact statement package identified below.** This is a
statement-fidelity and definition-trust approval, not a proof approval or a claim
that KE-04 has been Lean verified. All 24 Challenge bodies remain intentional
admissions. A second independent statement approval and the coordinator's
acceptance are still required before proof implementation.

- Date: 13 September 2026.
- Reviewer: AI agent `/root/ra20_final_referee2`, acting as KE-04 statement referee 1.
- Independence: I did not author or steer the KE-04 statements. The author is
  `/root/ie05_statement_referee1`; the coordinator supplied design steering.
  Neither author's assertions nor the prior informal review counted as an
  independent statement approval. I reused a diagnostic traversal pattern from
  my earlier RA-20 review, with new KE-04 inputs, executions and results.
- Scope: original target and complete source proof; all 27 concrete definitions
  and 24 actual elaborated contracts; exact domains, quantifiers, multiplicities,
  existence and semantic bridges; pinned library meanings; retained evidence
  integrity, attribution and reproducibility.
- Changes: no original input, statement, proof, metadata, canonical status,
  registry, Git object, branch or remote was modified. Reviewer writes are this
  report and `reviews/statement-referee-1-evidence/`; only newly created private
  object prefixes were deleted after hashing.

## Exact reviewed inputs

The original package contained exactly 168 files: 167 entries in its complete
draft inventory plus that inventory itself. Before creating this review's
directory I checked every byte identity, both supplied handoff identities, and
exact membership. I repeated all 168 checks after the independent compilation
and provenance audits. `baseline.json` retains the complete initial inventory.

| Input | SHA-256 |
| --- | --- |
| `STATEMENT-HANDOFF.md` | `f46ec1cb54a9eed22dd7fc2cf640531be64b2ec86d48251d09075a64e94fa8a9` |
| `DRAFT-INVENTORY.json` | `e82c391cc2d8d3ad1ee12e4f19266e2495e469e4b39272d31697a2e4a873a9fa` |
| `NLA/KE04/Definitions.lean` | `ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4` |
| `Challenge.lean` | `a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e` |
| `NUMERICAL_TARGETS.md` | `ad963526a371cdfee8eaaf179674d5cabd2a1d5a9ae5b123c96ac2f2b4271c47` |
| `SourceCorrespondence.md` | `399f28847f52a6c5ff309a25b9501c0c6d4bd5a76892de2f5adaa9c25fe80a00` |
| `README.md` | `a842060b717a02f2cbc7f204b0773ee847f724d2ed0b4ceebd98a087a3b66cf6` |
| `comparator.json` | `c0c7086cb81abe8f422762d0db2cc55419828f08ba80d33f9157cb3f396a8b8e` |
| `lakefile.toml` | `1e860d6ff5d2754de834dcb8d458f3d95e4da3ad43a7b5ecbd48e91ed2f18363` |
| `lake-manifest.json` | `6590a604a552411f07cd4806d378bf6c8ed3f2cf3b957b2b41b0e7669dcf29c6` |
| `lean-toolchain` | `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71` |

The canonical source and review policy are bound to Git commit
`5830ed4fb06da0659414a3deb2a40ad327aca052`. I independently ran `git rev-parse`
and `git show` for all 17 original source records, including the original target
at `b4123194697bdf6f8f82518c1dd7d6c40a30c2e0` and initial submitted proof at
`fe025e14d2639cbae59f98cacf4023d83addcb89`. Their Git blobs, full bytes and
SHA-256 values match the retained copies. The complete selected theorem/proof
block remains 2622 bytes with SHA-256
`3ba1bd9a62a00aaf787758af6312e4787ca8d6db02b4487e8b956ce0553977a7`.
I read both full Markdown manuscripts, the full source TeX, the current and
original canonical statements, and the retained detailed informal review.

## Mathematical fidelity

The target is the strict interval-occupancy assertion for every real symmetric
matrix, full-column-rank starting block, allowed iteration pair and allowed
one-based index, with spectra ordered with multiplicity and independently
chosen orthonormal Krylov bases. The original maximal-full-index formulation is
present in `BlockLanczosConjecture`. The source proof's stronger arbitrary-full-
prefix formulation is present in `FullPrefixBlockLanczosClaim`, with an explicit
implication contract back to the canonical formulation. Neither final target
assumes interval occupancy, a spectral gap, or quadratic nonannihilation.

I inspected the actual elaborated values and types, including fully explicit
outputs, rather than accepting their names or the source-correspondence table.
Readable copies of the same outputs are retained as `actual-definition-values.txt`
and `actual-contract-types.txt`. The main definitions have precisely the stated
universal quantifiers; there are no added rationality, boundedness, positivity,
invertibility, simple-spectrum, endpoint-separation or basis-compatibility
requirements.

`Vec n` is genuine real Euclidean space, and the matrix action is the imported
`Matrix.toEuclideanLin`. The Krylov space is the span of all actual columns
indexed by `Fin ell × Fin p`, with powers zero through `ell-1`; it is not an
unconstrained family of subspaces. Its finite-dimensional ambient space and
submodules rule out the infinite-rank-to-zero convention of `Module.finrank`.
I inspected the precise finite-dimensional and finrank definitions in additional
pinned source captures. Full block dimension and starting full rank have no
spectral content hidden in their definitions.

The spectral choice is sound as a statement boundary. In pinned Mathlib,
`LinearMap.IsSymmetric.eigenvalues` is antitone, with genuine matching
`eigenvectorBasis`, eigenvector equations, and characteristic-root multiset
theorems. The draft reverses the eigenvalue index by `Fin.rev`. Library
`OrthonormalBasis.reindex` uses the inverse equivalence; since `Fin.revPerm` is
an involution, the draft's eigenbasis has exactly the same reversed indexing.
This is not the potentially misleading arbitrary-index matrix eigenvalue
enumeration. The roots equation in the contract is multiset equality, retaining
all algebraic multiplicities. I also checked the actual Hermitian-to-Euclidean-
self-adjoint bridge and real transpose interpretation in the pinned sources.

An orthonormal basis matrix means exactly `QᵀQ=I` and the correct column space.
Existence is a required conclusion, not an assumed witness type that might be
empty. Arbitrary equal-span choices must be proved orthogonally similar and have
equal full ordered spectral functions. Quantifying just the two relevant bases
is equivalent to allowing independent choices at all iterations for this
pairwise spectral property.

The quadratic is the actual monic degree-two polynomial `(X-a)(X-b)`. The ambient
lift is `Q q(Qᵀ A Q) Qᵀ`, which represents the compressed subspace quadratic
extended by zero. It does not accidentally evaluate the polynomial on the
ambient zero extension of the first compression. Equality of earlier and later
**forms** uses symmetry and their common first action on `K_(k-1)`. Only the
later squared action is identified with `A²x`, using `k+1 ≤ j`. This distinction
preserves the substantive second step of the source proof.

## All 24 contracts

Every declaration below has namespace prefix `NLA.KE04.`. Each was inspected in
source and in the independent compiler's actual type output.

| Contract | Independent statement finding |
| --- | --- |
| `real_matrix_semantics` | Correct real symmetry, coordinate matrix action and orthonormal-column equivalence, including empty dimensions. |
| `krylov_range_semantics` | Exact finite coefficient range and expansion of all block powers; dimension upper bound has the correct `ell*p`. |
| `krylov_nesting_and_shift` | Empty prefix, nesting and one-power action inclusion follow from those actual powers; no invariance assumption. |
| `fullBlockDimension_iff_independent` | Full rank is exactly independence of all indexed columns, and the width-one-prefix statement correctly identifies starting full rank. |
| `fullBlockDimension_prefix` | Earlier dimensions and coefficient injectivity must be derived from one full prefix, with every `ell ≤ s` covered. |
| `lastFullBlockIteration_exists` | The necessary positive-width premise is explicit; full starting rank gives a nonempty set of positive full indices. |
| `krylovBasis_exists` | Genuine orthonormal bases of size `ell*p` must be constructed from full dimension. |
| `frameProjection_semantics` | Hermitian idempotence, exact fixed space and orthogonal residual characterize the actual projector. |
| `compression_semantics` | Correct real matrix compression and ambient representation of the projected action on its subspace. |
| `orderedSpectrum_semantics` | Increasing order, matching actual eigenvectors, characteristic-root multiplicities and valid total indexing are all conclusions. |
| `compression_basis_independent` | Orthogonal similarity, characteristic polynomial equality and equality of ordered lists cover arbitrary equal-span frames. |
| `interval_index_validity` | Both source endpoints are in range; `k ≥ 2` and positive width are derived, not extra target assumptions. |
| `quadratic_semantics` | Correct monicity, degree two, actual polynomial evaluation and expanded matrix identity. |
| `spectral_gap_quadratic_psd` | The only gap assumption is local to this auxiliary contradiction lemma; it allows coincident endpoints. |
| `spectral_window_subspace` | A consecutive window of `p+1` indexed eigenvectors yields that dimension even with repeated eigenvalues; nonpositive form is a conclusion. |
| `krylov_intersection_nonzero` | Actual dimension and inclusion premises force the nonzero intersection; no vector is assumed. |
| `psd_zero_form_iff_kernel` | Correct zero-form/kernel equivalence for singular as well as nonsingular PSD matrices. |
| `compressedQuadratic_semantics` | Correct quadratic-form and PSD transport through congruence, without unnecessary orthonormality or symmetry assumptions. |
| `quadratic_forms_agree` | Uses symmetry for forms on the previous Krylov space; does not assert the generally false earlier squared-action identity. |
| `later_quadratic_identity` | The later subspace contains the vector and its first two images; symmetry is correctly unnecessary for this action identity. |
| `fullRank_quadratic_nonannihilation` | Full dimension through `k+1`, a nonzero previous-prefix vector and monic degree two supply the highest-coefficient contradiction. |
| `strictIntervalOccupancy` | Complete arbitrary-full-prefix target; all original dimensions, matrices, bases, indices and strict inequalities are present. |
| `fullPrefix_implies_canonical` | Correct direction of the bridge to the original maximal-index statement. |
| `blockLanczosConjecture` | Complete canonical target, with no additional mathematical premise. |

The obligations assemble the complete original proof: spectral absence gives a
later PSD quadratic; a `p+1` window intersects the previous Krylov space
nontrivially; equal forms give a zero PSD form and hence an actual kernel
equation; the later action gives `q(A)x=0`; full block rank through `k+1`
contradicts that equation by the highest nonzero block coefficient. I found no
missing existence or semantic bridge requiring a stronger final hypothesis.
Whether a future Lean implementation proves each step remains a separate gate.

## Boundary and vacuity checks

For `p>0`, every full index satisfies `s*p ≤ n`; the full starting block gives
index one. Thus the largest full index exists. For `p=0`, all dimensions are
zero and there is no largest index. The existence theorem correctly excludes
that case; the stronger target still includes it with an empty admissible
index range. The same range is empty for `k=1`, and a positive-width full-rank
block cannot exist when `n=0`. These are honest degenerate cases, not the reason
the substantive target holds.

At `i=1` and `i=(k-1)p`, the zero-based endpoints are respectively `i-1` and
`i+p-1`, both strictly below `k*p`. The total indexing default of zero cannot
enter an admissible interval. At `k=2`, the coefficient expansion has only its
starting block and needs powers through two. At the last pair `k=s-1,j=s`, the
argument uses full dimension at `k+1=s`, not at `s+1`. Repeated eigenvalues are
retained, and coincident endpoints are excluded by the contradiction rather
than assumed absent.

As a separate mathematical nonvacuity check, `A=diag(-1,0,1)` with starting
column `(1,1,1)ᵀ` has three independent block-power columns. It has `s=3` and
an admissible pair `k=2,j=3,i=1`; the earlier compression has eigenvalues
`±sqrt(2/3)` and the later spectrum includes zero. Direct sums of this example
give positive block widths and repeated Ritz values. This is a reviewer sanity
check, not a Lean theorem or a proposed finite test substituting for the
universal proof.

## Independent execution and trust

The accepted fresh inspection is `attempt-nglj5yvu`. It compiled Definitions,
Challenge, a definition-only inspector and a contract inspector using Lean
4.33.1, binary SHA-256
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.
The toolchain reports commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
Mathlib is pinned to `0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert to
`621a43d7cf21f87872392a01e874f2f1dbddc926`; all ten manifest source revisions and
clean Git statuses were independently checked before and after.

The output prefix began empty. The only reused objects were the nine existing
read-only dependency directories plus the toolchain library. Cli is a tenth
source pin with no object directory used here. No Lake command, dependency
download, cache copy or dependency rebuild occurred. This is a macOS source
elaboration using preexisting dependency objects, not a fresh build of all
Mathlib sources or an external default-kernel/Linux run.

All four modules exited zero. Definitions emitted no diagnostics. Challenge
emitted exactly 24 expected admission warnings. Both inspectors emitted no
warnings or errors. The definition inspector imports
`LeanCert.Tactic.Verification`, explicitly selects `leancert.trust = "kernel"`,
and executes **27 actual `#assert_trust kernel` commands plus 27 axiom prints**.
Every printed definition depends only on `propext`, `Classical.choice`, and
`Quot.sound`. I read the actual LeanCert command implementation: it collects
transitive axioms and rejects sorry, custom and native-compiler axioms; success
is silent, so no invented success marker is required.

The actual definition closure has **33 declarations**, including six generated
helpers. Each was checked for a body, unsafe/partial status and transitive axiom
allowance. Its actual dependencies include 19 separately checked material
library constants covering Euclidean action, rank, spans, coefficient maps,
genuine self-adjoint spectra, reversed basis indexing and polynomials. The
contract inspector confirmed all 24 theorem declarations are admitted and that
their actual types do not depend on another admitted Challenge contract.
The trust audit does not turn those admissions into proofs.

There are 408 recorded child-command receipts across elaboration/provenance
attempts and additional source captures, with original stdout/stderr retained.
Three private compilation attempts produced ten objects in total; all ten were
hashed and only their own fresh prefixes removed. The first failed inspector,
the intermediate successful inspection and the final successful readable/fully
explicit inspection all remain in the evidence. No failed attempt is counted
as an accepted final run.

## Evidence integrity, reuse and attribution

I independently bound all 33 retained API/reference text snapshots to their
actual pinned Git files or the retained Tau Ceti archive; three additional
Mathlib captures cover the precise symmetry and finite-dimension bridges.
The Tau Ceti archive's seven Git trees were reconstructed independently and
matched the commit's actual root tree. Its API response outer SHA echoes the
requested commit and is not substituted for that root-tree check. Five source
searches were rerun; parallel `rg` output order was compared as a complete line
multiset while retaining both exact raw outputs. Existing spectral, orthonormal
basis, finite linear-combination, dimension and PSD APIs provide the intended
building blocks. The empty Krylov/Lanczos name search is bounded evidence, not
a claim that no equivalent abstract lemma exists.

I read the pinned Schiffer and Forsythe structural examples and the repository's
review adapter together with all ten Tau Ceti rubric angles. Their relevant
fidelity, scope, reuse, generality, API, naming, placement, documentation,
attribution and proof-quality concerns were applied within this statement
phase. Tau Ceti service execution, roadmap admission and endorsement are not
claimed. The 24 semantic bundles are this problem's explicit audit boundary;
they are not a proposal to duplicate generic Mathlib proofs. The source argument
is exact finite-dimensional algebra, so no artificial interval mesh or numerical
certificate is necessary. LeanCert has an actual definition-trust role now;
future theorem trust checks remain required.

The author candidly records the overwritten historical elaboration JSON. I
checked the offending and corrected validator sources and the surviving logs.
The old final JSON, exact old object records and old dependency postflight are
lost; I do not infer or reconstruct them. The fresh author attempt
`attempt-r5fn2nl_` has intact source/log bindings, four module results, ten pinned
dependency records and removed-object hashes. My independent executions do not
rely on the author-only PASS markers. All original failed captures and nested
manifests are preserved. My own tooling failures and their corrections are
documented in `DIAGNOSTICS.md`, with raw diagnostics and executed source copies.

Original mathematical credit remains Matthew J. Colbrook, Department of
Applied Mathematics and Theoretical Physics, University of Cambridge. The
ChatGPT draft origin and prior independent Codex informal review remain
disclosed. Prospective formalization credit is George Stepaniants, Department
of Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA, with substantial AI assistance. No contact email is
added for George. Exact original source bytes retain the original author's
public metadata; this is not a claim that the entire historical corpus contains
no email addresses. Archived third-party sources retain their licenses and
bylines; Schiffer is a structural reference, not an imported implementation.

## Reproduction and limits

`RESULT.json` identifies accepted attempt and provenance result hashes and the
complete diagnostic counts. `EVIDENCE-MANIFEST.json` seals this report, every
original input (including every nested manifest), and every reviewer evidence
file. Its only omitted file is that exact outer manifest itself. The read-only
entry point, run from this statement package before later phase additions, is:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 reviews/statement-referee-1-evidence/verify_inventory.py
```

The independent elaboration runner can create a new attempt if required, but
that is a new execution outside this sealed inventory. Do not rerun mutating
audit/runner scripts inside a sealed historical review and present the old seal
as covering the new outputs.

The configured 24 Comparator target names and foundational allowance match
Challenge. `Solution` is explicitly reserved and absent; default Lake target is
Challenge. No solution proof, publication YAML, Comparator execution, exporter,
external default-kernel replay, Linux sandbox/control result or status promotion
is asserted. A future complete proof must satisfy all those applicable gates
and must not import Challenge. This review supplies one independent approval of
the exact statements only.
