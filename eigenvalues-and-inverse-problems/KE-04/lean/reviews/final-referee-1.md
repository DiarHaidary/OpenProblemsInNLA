# KE-04 independent final mathematical review 1

**Verdict: APPROVE the complete mathematical formalization at the corrected
proof freeze below.** This is an independent final mathematical approval with
fresh local source, statement and trust evidence. It is not an authoritative
Linux Comparator result or permission to describe the project as fully Lean
verified before the remaining repository gates pass.

Reviewer: AI agent `/root/ra09_final_referee1`, 13 September 2026. I did not
author, design, steer or fix any KE-04 statement or proof. I read the complete
original target, complete Colbrook Markdown and TeX proof, every definition,
all 24 contracts and every mathematical implementation module before reading
the earlier statement approvals. I reused diagnostic tooling from my own RA-09
review, with new KE-04 requirements and fresh executions. An author PASS report
or another referee's verdict did not supply my mathematical judgment.

My only substantive finding concerned a provenance convenience map in the
first proof freeze. It was reported before approval, corrected by the coordinator
without changing mathematics, and independently rechecked below. No unresolved
mathematical finding remains. My writes are this report and its own evidence
directory; no mathematical source, canonical problem, status, registry, Git state
or shared dependency cache was modified.

## Exact reviewed boundary

| Input | SHA-256 |
| --- | --- |
| Corrected `reviews/proof-freeze.json`, 3,503 inputs | `394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4` |
| Original compilation freeze, 3,493 inputs, preserved | `d45703f80e35612826060bc53d7a46da7c341234f2edd8cd6269e1ed72c53c16` |
| Accepted 1,598-input statement freeze | `85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e` |
| `NLA/KE04/Definitions.lean` | `ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4` |
| `Challenge.lean` | `a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e` |
| `NLA/KE04/Completion.lean` | `4014011a7c6435c362ce4cf304aed8d7a8ad2e32ffb03448fbf43223c59a3f97` |
| `NLA/KE04/Proof.lean` | `f3920f297fdd8de840e88cad46322ce69ddcfd106b6dec51dd92fc386ccc76da` |
| `PROOF-MAP.md` | `f3121530c52569206c248435e3eb41ff4b60da9a9a7a64d8c6999cc32bff11c5` |

Every byte of the original 3,493-file boundary and the 1,598-file statement
boundary was checked before and after my build. The corrected freeze retains
all those original bytes and adds ten provenance-correction artifacts. I checked
all 3,503 final entries, including every nested manifest. The independent outer
inventory binds that complete corrected boundary, the proof freeze itself,
this report and every file of this referee's evidence. Its sole self-exclusion
is its own exact path. Concurrent referee 2 additions and future packaging are
outside this approval.

The canonical current source base is
`5830ed4fb06da0659414a3deb2a40ad327aca052`. I independently retrieved all 17
source snapshots from their actual individual Git commit/path pairs, including
the separately retained original target and original submission. I repeated
those 17 checks against the corrected metadata. The permanent KE-04 path and
original mathematical target remain unchanged.

## Fidelity and mathematical proof

The final theorem preserves the original universal claim: real symmetric
matrices in every dimension, a full-column-rank starting block, the largest full
Krylov iteration, every `1 ≤ k < j ≤ s`, arbitrary independently chosen
orthonormal Krylov bases and every original one-based interval index
`1 ≤ i ≤ (k-1)p`. Both interval inequalities are strict. There is no added
simple-spectrum, separated-endpoint, positivity, invertibility, compatible-basis,
rationality or bounded-dimension condition. The stronger arbitrary-full-prefix
theorem is proved, and its implication to the canonical maximal-index theorem
has the correct direction.

`Vec`, matrix action, Krylov powers, spans, coefficient maps and ranks are genuine
Mathlib objects. Finite-dimensional ambient spaces and their submodules avoid
the infinite-rank convention for `finrank`. `FullBlockDimension` contains only
the actual dimension equality; it assumes no part of occupancy or polynomial
nonannihilation. Existence of orthonormal frames and of the largest full index
for positive block width is proved. The custom interface is consequently not
made vacuous by demanding nonexistent witnesses.

The spectrum reverses Mathlib's decreasing self-adjoint eigenvalues and the
matching orthonormal eigenbasis. The code proves increasing order, the actual
eigenvector equations and the complete characteristic-root **multiset**, retaining
multiplicity. I inspected the pinned library definitions and the actual
elaborated definitions. Since `Fin.revPerm` is an involution, the inverse in
basis reindexing reverses the same indices. Equal-span frames are proved
orthogonally similar and to have the same ordered spectrum. Both natural-index
endpoints are proved in range before their values are used; the fallback zero
cannot enter an admissible interval.

The substantive proof chain is present in actual theorem bodies:

1. Assuming an empty later interval `(a,b)`, diagonalization in the genuine
   later eigenbasis makes `(H-aI)(H-bI)` PSD. Equality `a=b` is allowed.
2. The earlier spectral window is the span of `p+1` distinct orthonormal basis
   indices. Its dimension is exactly `p+1`, even when eigenvalues repeat, and
   the earlier quadratic form is nonpositive there.
3. The actual dimension formula for a sum and intersection gives a nonzero
   intersection with `K_(k-1)`, whose codimension in `K_k` is `p`.
4. For an intersection vector, both spaces contain `x` and `Ax`. Symmetry gives
   equal quadratic forms, each equal to
   `‖Ax‖²-(a+b)⟪x,Ax⟫+ab‖x‖²`. The earlier squared compressed action is never
   incorrectly identified with `A²x`.
5. PSD and the zero form imply an actual zero later action through the genuine
   PSD-kernel theorem, including the singular case. Only the later space is
   asserted to contain `A²x`, since `k+1 ≤ j`, so its quadratic action equals
   `(A-aI)(A-bI)x`. The ambient lift is correctly `Q q(QᵀAQ) Qᵀ`; there is no
   extraneous `ab(I-P)` term from applying the polynomial to an ambient zero
   extension of the first compression.
6. Full rank through `k+1` excludes this nonzero kernel vector. Zero extension
   and shifting of the actual coefficient blocks give equal images under an
   injective next-prefix map. Reverse induction from the appended zero forces
   every coefficient to vanish. The proof divides by no endpoint. It first
   applies this fact to `(A-bI)x` in `K_k`, then to `x` in `K_(k-1)`, proving
   the required monic-quadratic nonannihilation also for equal or zero endpoints.

The last step is an exact implementation of the source's leading-coefficient
argument using its two affine factors. It is not a residual nonannihilation
hypothesis. The final contradiction produces a genuine later Ritz value in
the strict interval for every allowed index.

## Every approved contract

Each name below has prefix `NLA.KE04.`. I inspected its source signature,
actual elaborated type, implementation and material semantic role.

| Contract | Final finding |
| --- | --- |
| `real_matrix_semantics` | Actual transpose symmetry, coordinate action and orthonormal columns. |
| `krylov_range_semantics` | Exact block-power coefficient range, expansion and dimension bound. |
| `krylov_nesting_and_shift` | Actual empty prefix, inclusions and one-power action. |
| `fullBlockDimension_iff_independent` | Genuine column independence and the initial full-rank block. |
| `fullBlockDimension_prefix` | All earlier full dimensions and coefficient-map injectivity are derived. |
| `lastFullBlockIteration_exists` | Positive width gives an existing maximal full index, bounded by ambient dimension. |
| `krylovBasis_exists` | Genuine orthonormal bases of the stated Krylov dimension are constructed. |
| `frameProjection_semantics` | Actual Hermitian idempotent, correct fixed space and orthogonal residual. |
| `compression_semantics` | Genuine `QᵀAQ` and the represented projected action. |
| `orderedSpectrum_semantics` | Increasing genuine eigenvalues, matching eigenvectors and root multiplicities. |
| `compression_basis_independent` | Orthogonal similarity and equality of whole ordered spectra. |
| `interval_index_validity` | Both endpoints valid; `k≥2` and `p>0` follow from the source index constraints. |
| `quadratic_semantics` | Actual monic degree two, polynomial evaluation and matrix expansion. |
| `spectral_gap_quadratic_psd` | Genuine spectral sign proof, also when the endpoints coincide. |
| `spectral_window_subspace` | Actual `p+1`-dimensional indexed eigenvector span and nonpositive form. |
| `krylov_intersection_nonzero` | Actual finite-dimensional nonzero intersection is derived. |
| `psd_zero_form_iff_kernel` | Genuine PSD zero-form/kernel equivalence, with no invertibility premise. |
| `compressedQuadratic_semantics` | Correct form and PSD congruence for the actual quadratic lift. |
| `quadratic_forms_agree` | Equality of forms through both compressions, with the needed symmetry. |
| `later_quadratic_identity` | Correct later full action from containment of the first two images. |
| `fullRank_quadratic_nonannihilation` | Actual injectivity and two affine factors discharge nonannihilation. |
| `strictIntervalOccupancy` | Full arbitrary-prefix strict occupancy, without a hidden gap assumption. |
| `fullPrefix_implies_canonical` | Correct implication to the original largest-index convention. |
| `blockLanczosConjecture` | Complete original target, obtained by that implication. |

For `p=0`, there is no largest full index; the existence theorem correctly
requires positive width, while the stronger target has an empty index range.
That range is also empty for `k=1`. At `n=0`, a positive-width full-rank block
cannot exist. At the final pair `k=s-1,j=s`, the proof needs full rank only
through `s`. At `k=2`, it uses the starting block and powers through two.
Coincident endpoints are contradicted by the same quadratic argument instead
of being silently excluded. These checks cover the degenerate cases without
weakening the nontrivial theorem.

As a manual nonvacuity check, the symmetric three-vertex path matrix with
starting vector `e₁` has independent Krylov columns `e₁,e₂,e₁+e₃`. For
`k=2,j=3,i=1`, the earlier Ritz values are `-1,1` and a later value is zero.
Block diagonal copies give positive block widths and repeated Ritz values.
This example is a mathematical sanity check, not a claimed additional Lean
certificate or substitute for the universal proof.

## Fresh execution and actual trust checks

My single fresh batch compiled ten mathematical modules, `Solution`, a
namespace-renamed copy of the frozen reference, and my independent inspector:
**13 successful Lean commands in 70.356 seconds**. The output prefix began
empty and was first on `LEAN_PATH`. No prior target object, Lake command,
dependency download, dependency rebuild or cache copy was used.

The host was macOS 14.6.1 arm64. Lean reported 4.33.1, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; its binary SHA-256 was
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.
All ten dependency Git revisions and clean statuses were checked before and
after. Nine dependency object directories were read; Cli was source-only.
Mathlib was `0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert was
`621a43d7cf21f87872392a01e874f2f1dbddc926`. Selected imported object hashes,
including the actual LeanCert trust module, also remained identical.

All **24 actual exported theorem types** were definitionally equal to the
separately elaborated frozen references. The derivation changes only the
reference namespace. Its 24 deliberate admitted bodies were detected and never
used by the implementation; the inspector rejects any real proof edge into
that namespace. Actual readable and fully explicit types and key definition
values are retained in the inspector log.

The actual type-and-body traversal from the complete canonical theorem covers
**105 project declarations and 42 required material bridges**. Traversal from
all exports and, separately, every source declaration covers **147 declarations
and 57 material bridges** each. The logs contain 399 actual project axiom rows.
Every traversed project declaration is safe, nonpartial and body-bearing except
the permitted inductive/constructor/recursor forms; each transitive axiom set is
a subset of `propext`, `Classical.choice`, `Quot.sound`. The traversal includes
actual spectral, PSD-kernel, dimension, frame and coefficient-injectivity
dependencies. Merely importing or mentioning a helper would not satisfy the
material-dependency checks.

There were **128 executed `#assert_trust kernel` commands with 128 actual axiom
reports**: 77 in the supplied sources, plus my 24 export and 27 definition checks.
No implementation admission, custom axiom, native decision or native-compiler
trust was found. I read the actual pinned LeanCert command implementation,
which checks transitive axioms and succeeds silently.

The only implementation warning was the already present unused simp argument
`hr` at `Krylov.lean:107`. It does not alter the proof and was not suppressed.
The derived reference emitted exactly its 24 expected admission warnings;
my inspector emitted no warnings. All raw outputs are retained. An expected
empty bounded Krylov/Lanczos name search exited 1; it was not a build failure.
Earlier author/referee failures remain frozen and are not counted as my own
successful execution. The preparation note records my initial missing-path
lookup and truncated exploratory listings. No fresh Lean or evidence-auditor
failure occurred in this review.

All 26 generated objects, totaling 3,304,397 bytes, were hash-recorded and then
removed from my own disposable prefix. The shared cache remained untouched.
`execution.json`, `source-and-output-audit.json`, `Inspect.lean`,
`inspection-requirements.json` and the raw command files provide the actual
evidence, rather than relying on these prose counts.

## Provenance finding and its resolution

The initial proof freeze's secondary `source_files` and `source_git_blobs` maps
used upstream paths as keys. They collapsed the original/current README and
Markdown-proof pairs, giving 15 entries and misleading current-snapshot hashes.
The complete 3,493-file inventory and the separate original-source inventory
still correctly bound all 17 distinct snapshots. I reported the discrepancy
before approval; `proof-freeze-source-map-finding.json` retains the examples.

The coordinator preserved the original freeze, explained the defect, and issued
the corrected freeze with 17 distinct project-relative snapshot keys and
explicit per-record commit/path/blob/hash/size data. My
`corrected-freeze-acceptance.json` rechecks every one of the 3,503 final inputs,
all 3,493 unchanged earlier inputs, the exact correction-directory seal and all
17 actual Git records. The finding is resolved. The mathematics, statements
and compiled bytes did not change, so no additional mathematical build is
claimed or necessary solely for this metadata correction. The original run
continues to identify its actual original metadata input honestly.

## Review standards, reuse, credit and remaining gates

I applied the pinned NLA adapter of all ten Tau Ceti rubric angles and read
the actual rubric texts. Their relevant fidelity, scope, proof quality, reuse,
generality, API, naming, placement, documentation and attribution concerns have
been assessed for this single permanent NLA target. Tau Ceti roadmap admission,
namespace/compatibility policy and service endorsement are not imported.

Actual pinned Mathlib searches and source inspection confirm use of its
self-adjoint spectral theorem, orthonormal bases, dimension formulas, finite
linear-combination injectivity and PSD kernel theorem. Twenty API/reference
files were independently retrieved at their pinned Git commits; thirteen Tau
Ceti texts were checked against the retained source archive and recorded Git
blob hashes. Schiffer and Forsythe were inspected as structural examples, not
used as mathematical KE-04 proofs. The fixed public wrappers constitute the
approved statement-comparison interface; they are not compatibility aliases
or replacements for generic Mathlib APIs.

Exact symbolic linear algebra and natural-number reasoning eliminate interval
subdivision and sampling completely. LeanCert's kernel trust assertions are
materially exercised without inventing an unnecessary numerical certificate.
The helper modules expose the significant mathematical steps and preserve
the original argument. The harmless unused-simp warning is not a mathematical
objection. Historical statement-stage prose and the old Challenge default
remain explicitly historical; publication packaging must select Solution and
preserve the old configuration through the required archive mapping.

Original mathematical credit remains Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge; the conjecture is
attributed to D. Šimonová and P. Tichý. Formalization credit is George Stepaniants,
Department of Computing and Mathematical Sciences, California Institute of
Technology, Pasadena, California, USA, with substantial ChatGPT/Codex assistance.
No George email was added. Original public source metadata, bylines, licensing
and earlier AI disclosures remain preserved.

This supplies one independent final mathematical approval. The second review,
packaging/schema checks, actual non-root Linux sandbox controls, default-kernel
replay and Comparator remain separate required gates. No actual Linux run,
external kernel replay, Comparator execution, human peer review, publication,
new mathematical solution or canonical status change is claimed here.

For read-only verification of this exact historical review boundary, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 reviews/final-referee-1-evidence/verify_inventory.py
```

The historical build/audit runners retain the original compilation freeze and
must not be rerun in-place after sealing and treated as the same evidence.
Reproduction is a new execution and requires its own output boundary. The
read-only inventory verifier checks the corrected final scope while allowing
later work outside this referee's files.
