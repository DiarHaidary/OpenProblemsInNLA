# KE-04 independent final mathematical review 2

**Verdict: APPROVE the complete mathematical formalization at the corrected
proof freeze below. No mathematical correction is requested.** This is an
independent AI-agent mathematical review, accompanied by fresh macOS source
checks. It is not human peer review, an official Tau Ceti service result, a
Linux/Comparator result, or authorization to promote the canonical status.

Reviewer: `/root/leancert_examples`, 13 September 2026. I made no KE-04 statement,
route, definition or proof contribution. My unrelated campaign work and general
LeanCert guidance are disclosed and do not constitute a KE-04 contribution.
I read the complete original target, complete Colbrook proof and every
mathematical implementation module before my fresh compilation. The author's
PASS assertions and either earlier statement review were not substitutes for
this review. My writes are confined to this report and its evidence directory;
the earlier read-only preparation is retained there.

## Exact boundary and the provenance correction

The accepted current freeze is `reviews/proof-freeze.json`, SHA-256
`394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4`.
It binds **3,503 existing project inputs and 17 distinct original Git source
records**, before these final reviews. Every bound byte passed my initial and
final checks. All 1,598 statement-freeze inputs remain included unchanged.

| Mathematical boundary | SHA-256 |
| --- | --- |
| Definitions | `ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4` |
| Challenge | `a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e` |
| Numerical targets | `ad963526a371cdfee8eaaf179674d5cabd2a1d5a9ae5b123c96ac2f2b4271c47` |
| Source correspondence | `399f28847f52a6c5ff309a25b9501c0c6d4bd5a76892de2f5adaa9c25fe80a00` |
| Proof exports | `f3920f297fdd8de840e88cad46322ce69ddcfd106b6dec51dd92fc386ccc76da` |
| Completion | `4014011a7c6435c362ce4cf304aed8d7a8ad2e32ffb03448fbf43223c59a3f97` |

The initial freeze `d45703f80e35612826060bc53d7a46da7c341234f2edd8cd6269e1ed72c53c16`
contained 3,493 full inputs. Its supplementary upstream-path maps collapsed two
historical/current pairs, although the full input map and original snapshot
inventory retained all 17. Referee 1 identified that coordinator metadata defect.
I had independently verified all 17 actual `git show`/`git rev-parse` records,
and archived the exact initial freeze, before the correction. The corrected
maps use distinct snapshot paths and match the statement freeze; every earlier
3,493 input is unchanged. I checked the correction before starting my Lean run.
This is a resolved provenance finding, with no mathematical source change.

The original source base is `5830ed4fb06da0659414a3deb2a40ad327aca052`. The original
target at `b4123194697bdf6f8f82518c1dd7d6c40a30c2e0` and first submitted proof at
`fe025e14d2639cbae59f98cacf4023d83addcb89` are separately retained. I checked all
17 original blobs and bytes, including the current canonical page, both complete
Markdown proofs, the complete TeX proof, informal review and contribution/review
policies. The actual current upstream-base policy files equal those snapshots.
The permanent path remains `eigenvalues-and-inverse-problems/KE-04/README.md`.

## Full-target fidelity and actual mathematics

The final claim universally quantifies the real symmetric matrix, the starting
full-column-rank block, its largest full iteration, every `1 ≤ k < j ≤ s`,
independent orthonormal frames at the two iterations, and every one-based
`1 ≤ i ≤ (k-1)p`. The later value lies **strictly** between the prescribed
earlier indexed endpoints. It retains eigenvalue multiplicities. No spectral
simplicity, separated endpoints, compatible Lanczos recurrence, invariant
Krylov space or nonannihilation premise has been added.

`krylov` is the actual span of columns of `A^r V`, `r < ell`;
`krylovCombination` is the actual finite linear combination. Full block
dimension is the actual finrank of a finite-dimensional submodule. The proof
derives independence, earlier full dimensions and coefficient-map injectivity
from it. An `IsKrylovBasis` is exactly an orthonormal matrix with this column
space; basis existence is proved, so the universal frame quantifiers do not
hide an empty interface. The compression is the genuine `Qᵀ A Q` over the reals.

The implementation reverses Mathlib's decreasing self-adjoint eigenvalue list
and reverses its matched orthonormal eigenbasis. I inspected the actual pinned
`eigenvalues`, `eigenvectorBasis`, order and eigenvector theorems, and root
multiset theorem. The reindexing is an involution. The characteristic-root
identity is a **multiset** equality; equal eigenvalues do not collapse distinct
indexed basis vectors. The separate arbitrary-frame equivalence constructs the
orthogonal change of basis, proves similarity, then derives equality of the
entire ordered spectral functions from the characteristic polynomial.

The decisive window really contains `p+1` indexed orthonormal eigenvectors.
Its dimension is proved from their linear independence, even with repeated
eigenvalues. Their quadratic coefficients are nonpositive, which gives a
nonpositive form on their full span. The finite-dimensional supremum/intersection
identity then produces a **nonzero** vector in its intersection with the previous
Krylov space: the latter's codimension is exactly `p`.

The lifted quadratic is `Q q(Qᵀ A Q) Qᵀ`, extended by zero on the orthogonal
complement. It is not incorrectly computed as the polynomial of the ambient
zero-extended first compression. On the selected vector, both quadratic forms
equal `‖Ax‖²-(a+b)⟪x,Ax⟫+ab‖x‖²`. The earlier squared action is never asserted
to equal `A²x`. Only the later space contains `x, Ax, A²x`, using `k+1 ≤ j`, and
therefore only its action is identified with `q(A)x`. Absence of a later value
in the open interval makes its actual quadratic PSD. The imported PSD
zero-form/kernel theorem has no invertibility requirement and is used correctly.

The final rank argument is an exact adaptation of Colbrook's monic leading-block
argument. The formal proof first excludes an eigenvector in `K_ell` when the
next prefix has full rank. Injectivity equates the shifted coefficient blocks
with the zero-extended blocks times an endpoint. Backward induction from the
appended zero forces every coefficient to vanish, without division. Applying
this result first to `(A-bI)x` in `K_k` and then to `x` in `K_(k-1)` proves the
quadratic nonannihilation contract. This uses precisely full rank through `k+1`,
works for `a=b` and zero endpoints, and does not require symmetry for that
algebraic helper. The final contradiction materially reaches these lemmas.

## All 24 completed contracts

Every name below is prefixed `NLA.KE04.`. I read each signature and its
implementation, then compared its actual compiled type with a namespace-only
copy of the frozen Challenge, compiled independently before Solution.

| Contract | Checked completed content |
| --- | --- |
| `real_matrix_semantics` | Real transpose/Hermitian equivalence, genuine action and orthonormal columns. |
| `krylov_range_semantics` | Exact range, coefficient representation and dimension bound. |
| `krylov_nesting_and_shift` | Empty prefix, nesting and the actual one-power shift. |
| `fullBlockDimension_iff_independent` | Actual block rank equivalence and starting-column rank at iteration one. |
| `fullBlockDimension_prefix` | Every preceding full dimension and injective coefficient map. |
| `lastFullBlockIteration_exists` | Positive-width existence of the genuine maximum, bounded by ambient dimension. |
| `krylovBasis_exists` | An actual orthonormal frame of the full Krylov subspace. |
| `frameProjection_semantics` | Hermitian idempotence, exact fixed space and orthogonal residual. |
| `compression_semantics` | Genuine transpose compression and projected-action identification. |
| `orderedSpectrum_semantics` | Increasing eigenvalues, matching eigenbasis and full root multiplicities. |
| `compression_basis_independent` | Orthogonal similarity and equality of complete ordered spectra. |
| `interval_index_validity` | Both endpoints valid; `k≥2` and `p>0` derived from the source indices. |
| `quadratic_semantics` | Genuine monic degree two, polynomial evaluation and matrix expansion. |
| `spectral_gap_quadratic_psd` | Actual spectral decomposition makes the quadratic PSD, also for equal endpoints. |
| `spectral_window_subspace` | The actual `p+1`-dimensional window and its full nonpositive form. |
| `krylov_intersection_nonzero` | Actual dimension identity yields the required nonzero intersection. |
| `psd_zero_form_iff_kernel` | Exact PSD form/kernel equivalence, including singular matrices. |
| `compressedQuadratic_semantics` | Actual congruence transports both the form and PSD property. |
| `quadratic_forms_agree` | Correct equality of forms on the previous prefix. |
| `later_quadratic_identity` | Correct later action on a vector and its first two matrix images. |
| `fullRank_quadratic_nonannihilation` | Full block-rank injectivity excludes both affine factors' annihilation. |
| `strictIntervalOccupancy` | Complete stronger arbitrary-full-prefix strict occupancy theorem. |
| `fullPrefix_implies_canonical` | Correct implication to the original largest-full-iteration formulation. |
| `blockLanczosConjecture` | Complete original target with no added premise. |

For `k=1` or `p=0`, no admissible interval index exists. Positive width is needed
only for the separately proved existence of a largest full iteration; at width
zero no such largest index exists. The main full-prefix statement still includes
that empty case. For positive width and zero ambient dimension, a full starting
block is impossible. Valid indices ensure the total eigenvalue helper never
uses its out-of-range default. At `k=2` the vector begins in the starting block;
at `k=s-1,j=s` the argument needs no iteration beyond `s`. Coincident endpoints
are contradicted by the same square-quadratic argument, not excluded up front.

I also independently reconstructed a nondegenerate example over exact rationals:
`A=diag(-2,1,4)` and starting column `(1,1,1)ᵀ` give a full third Krylov matrix
of determinant 54. An orthogonal basis for the second space gives compression
`[[1,√6],[√6,1]]`, and the later value 1 lies strictly between its endpoints.
Disjoint copies give larger block widths and repeated Ritz values. This is a
sanity check on nonvacuity, not a finite test substituted for the universal proof.

## Independent execution and actual trust evidence

The fresh attempt is `final-referee-2-evidence/attempt-m7jifjwc`. All **13 Lean
commands exited zero**: Definitions, the renamed reference, the other nine
mathematical modules, Solution and my inspector. The output prefix started
empty. No old KE-04 object, Lake invocation, dependency copy/download or dependency
rebuild was used. The actual import environment contained 5,028 modules; I
recorded their resolved paths, sizes and hashes, and rehashed all 5,016 external
objects. The other twelve imported objects came from my fresh prefix. All
thirteen generated objects were hash-recorded and only that prefix was removed.

Lean is 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, binary SHA-256
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.
Mathlib is `0df444a360eaa60ab8c11dca51a86af692955474`, LeanCert is
`621a43d7cf21f87872392a01e874f2f1dbddc926`. All ten source pins and clean statuses
matched before and after. Nine existing dependency object directories were
read directly; Cli remains a tenth source-only tooling pin.

The proof sources executed 77 actual LeanCert `#assert_trust kernel` checks and
axiom prints. My inspector executed 24 more. **All 101 permit only `propext`,
`Classical.choice` and `Quot.sound`.** The inspector directly compares axiom
`Name`s, independently of printed text. Every actual target is a theorem and
matches its frozen type. The reference's 24 deliberate admissions are separately
identified and never occur in the actual proof closure. Their warnings and one
harmless unused Krylov simp argument are the only 25 warnings in my run.

The actual final-target type/body closure contains **105** safe, nonpartial,
body-bearing project declarations and passes **31** required material dependency
checks. The closure of all exports contains **147** declarations and passes
**40** required checks. Each reached declaration's transitive axioms and direct
body/type dependencies are retained. This checks the live window, intersection,
PSD, transport and coefficient-induction chain, plus the real spectral, matrix,
rank and dimension APIs; it does not infer dependence from source names alone.

The runner's original Python postprocessor rejected printed universe decorations
such as `Classical.choice.{u}` after all Lean checks had passed. Its failed result
and all original logs remain unchanged. A separate corrected diagnostic, recorded
in `accepted-compiled-result.json`, strips only those formatting decorations;
the actual Lean name-level allowlist checks already passed. No proof or inspector
source was changed and no unnecessary recompilation was used to conceal this
reporting failure. A separate initial policy-path lookup failure is also retained.

These are macOS source checks using imported objects. The actual local environment
reports elaboration trust level **1025**, so this is expressly not external
default-kernel replay or a rebuild of every imported library from source.
The real Ubuntu sandbox, Comparator, default-kernel and rejection-control gates
must still run for this candidate. LeanCert is used for explicit kernel trust
auditing of the actual proofs; no interval certificate is claimed or needed.

## Tau Ceti angles, attribution and remaining packaging

I read the NLA adapter and all ten rubrics at Tau Ceti commit
`afb424eda89e8ac96d9eb69f6a88972055a4cd1b`. I independently bound all 33 retained
API/example/policy snapshots to their Git identities and reconstructed all seven
Tau Ceti trees, including the commit's actual root tree. The review applies the
rubrics to this permanent NLA target, not Tau Ceti roadmap admission or its
namespace/compatibility policies, and claims no official service endorsement.

- **Correctness and scope:** complete original real exact-arithmetic target,
  genuine definitions, strict indices and all actual semantic bridges pass.
- **Proof quality and reuse:** the argument is factored at its mathematical
  steps; affine-factor coefficient induction avoids unnecessary polynomial
  coefficient expansion. The proof reuses actual Mathlib spectral, dimension,
  orthonormal-frame and PSD APIs. My bounded Krylov/Lanczos search found no direct
  named replacement; it is not an exhaustive assertion about all abstractions.
- **Generality and API design:** the auxiliary transports omit unnecessary
  symmetry/frame assumptions where appropriate; no extra premise narrows the
  main target. The 24 bundles and wrappers preserve the independently reviewed
  problem-specific audit boundary rather than claiming a new general library.
- **Naming and placement:** the scoped `NLA.KE04` interface and separate Krylov,
  frame, spectral, transport and rank modules match their actual content. Proof
  imports are specific and do not import the admitted Challenge.
- **Documentation and attribution:** source and proof map describe the actual
  argument and adaptation. Colbrook's mathematical authorship and Cambridge
  affiliation are retained; George Stepaniants is credited with formalization,
  Department of Computing and Mathematical Sciences, California Institute of
  Technology, Pasadena, California, USA, with substantial AI assistance and no
  added contact email. Original-author metadata in archival sources is preserved.
  Schiffer and Forsythe are credited structural references; no Schiffer proof is
  imported or relicensed. Their inspected statement/proof separation informs the
  present checking layout.

The frozen README still says statement-only and the Lake default remains
Challenge; there is no current publication YAML yet. `PROOF-MAP.md` and the
coordinator acceptance explicitly identify these as preserved historical inputs.
They must be archived and refreshed truthfully at candidate packaging, before
publication. That is a known later-stage requirement, not a correction to the
approved frozen mathematics. Canonical status remains Solved until every
remaining mechanical, metadata and publication gate is satisfied.

## Evidence and reproduction

`final-referee-2-evidence/EVIDENCE-MANIFEST.json` binds this report, all reviewed
project inputs and this review's source snapshots, original commands/logs,
failed diagnostics, exact type/body outputs, imported-object provenance and
cleanup receipts. Its only self-exclusion is that exact outer manifest. The
concurrent sibling's exact `final-referee-1.md` and
`final-referee-1-evidence/` scope is separately excluded; no filename-wide or
nested-manifest exclusion is used.

Use `python3 reviews/final-referee-2-evidence/verify_evidence.py` for the read-only
identity check. Re-executing `run_fresh.py` creates a new review attempt outside
this historical seal; it must not be represented as covered by this verdict.
This approval supplies one independent final mathematical review only.
