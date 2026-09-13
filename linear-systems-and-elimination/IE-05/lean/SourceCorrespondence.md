# IE-05 source correspondence for the completed candidate

The canonical source is preserved at upstream commit
`5830ed4fb06da0659414a3deb2a40ad327aca052`. The full README, solution Markdown
and TeX, original integer data, and supporting source documents remain in
`verification/original-sources`; their 27 exact paths, Git blobs, SHA-256 hashes,
and byte lengths are recorded in `verification/original-source-inventory.json`.
The permanent ID and canonical **Solved** status are unchanged.

George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA, retains authorship
of the original counterexample and this formalization, with substantial
ChatGPT/Codex assistance disclosed. John Peca-Medlin retains the conjecture and
element-growth analysis attribution. The older orthogonal family is not assigned
a new origin here. This candidate adds no source-author endorsement, human peer
review, or official Tau Ceti approval claim.

## Source and complete target

The [retained canonical statement](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/linear-systems-and-elimination/IE-05/README.md)
specifies exact arithmetic, maximum absolute active-Schur entries, every
admissible tie path in the supremum, and the first available tied row for the
candidate. Its equality is universally quantified over every `n ≥ 2`.
The candidate is the unique positive-diagonal QR factor of the unit lower
triangular matrix with every strict-lower entry `-1`.

The [complete solution](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/5830ed4fb06da0659414a3deb2a40ad327aca052/linear-systems-and-elimination/IE-05/solution.md),
Theorem and Sections 1–4, supplies the exact order-eight counterexample. Its
one-based `(8,2)` modification is zero-based `(7,1)` in Lean. The full manuscript,
standalone TeX, frozen informal proof, prior informal automated review, integer
certificate programs, and recovered-proof checks were retained and inspected.
The Python data checks are evidence, never axioms or trusted Lean imports.

`Definitions.lean` defines the candidate through Mathlib's
`InnerProductSpace.gramSchmidtNormed` on `EuclideanSpace ℝ (Fin n)` columns.
The integer normalized formula is subsequently identified with that candidate
by proved positive QR uniqueness. `PositiveQR` means actual orthogonality,
matrix factorization, upper triangularity, and strictly positive diagonal.
No QR, trajectory, nonsingularity, bound, or supremum premise supplies the
desired conclusion.

The zero-padded Schur matrices contain precisely the active trailing block.
The nonzero-pivot induction uses injectivity on vectors supported in that block,
not nonsingularity of the padded full matrix after elimination. The finite
growth maximum uses stages `0` through `n-1`, including the input. Its denominator
is the input entry maximum; the proved terminal zero stage is not a growth stage.
The first-available rule is an actual ascending strict-update scan. General
admissible paths include every permitted tie choice.

The proof establishes nonemptiness and boundedness of the actual real orthogonal
growth set from orthogonality, identity membership, and the universal
`2^(n-1)` GEPP bound. Actual witness membership and `le_csSup` then give the
strict supremum gap and the negation of the whole original conjecture.

## Exact export map

All 17 names below have prefix `NLA.IE05.`, are declared in `NLA/IE05/Proof.lean`,
and are selected by the unchanged `comparator.json`. `Solution.lean` imports that
proof module only. Each exact Challenge signature is retained unchanged.

| Export | Completed implementation and source correspondence |
|---|---|
| `entryMax_semantics` | `GEPP`: the actual finite entry maximum bounds all absolute entries and is attained when the dimension is nonempty. |
| `schurStep_bound` | `GEPP`: the real row swap and admissible pivot inequality prove the active factor-two bound. |
| `gepp_growth_bound` | `GEPP`: every admissible execution has positive input maximum and growth between one and `2^(n-1)`. |
| `firstPath_semantics` | `Pivot`, `GEPP`: nonsingularity gives nonzero active pivots; the implemented scan gives trajectory agreement and the unique first-available path. |
| `orthogonalGrowthSet_bounded` | `GEPP`: the actual set over orthogonal matrices and all admissible paths is nonempty and bounded. |
| `candidate_positiveQR` | `QR`: normalized Euclidean Gram–Schmidt of the prescribed lower matrix gives actual positive QR, with uniqueness for every required dimension. |
| `scaledColumns_orthogonal` | `Scaling`: a diagonal Gram identity and positive scales give real matrix orthogonality. |
| `scaledLU_trajectory` | `LUTrajectory`: finite tail algebra proves the actual scaled Schur trajectory through terminal zero and the first-available no-swap path. |
| `integer_factor_certificates` | `ExactCertificates`: both literal integer Gram/LU identities, unit-lower and upper structure, bounded multipliers, and positive diagonals. |
| `integer_entry_certificates` | `ExactCertificates`: 64 witness input and 204 candidate active bounds, one candidate input value, witness column scale and final pivot. |
| `canonical_integer_identification` | `IntegerQR`, `Witness`: real casts and positive QR uniqueness identify the actual Gram–Schmidt candidate and its scan path. |
| `witness_orthogonal_path` | `Witness`: actual orthogonality and the exact first-available, admissible witness path. |
| `bounded_growth_data` | `GrowthBounds`, `Growth`: five one-sided estimates in the implemented maximum and growth semantics. |
| `numerical_gap_positive` | `ExactCertificates`: exact squared-gap identity and strict rational positivity. |
| `witness_strict_growth` | `Growth`: strict comparison of the actual candidate and witness executions. |
| `supremum_strict_gap` | `Growth`: strict comparison with the genuine bounded real supremum. |
| `orthogonalExtremizerConjecture` | `Growth`: the complete universal equality is false by its dimension-eight case. |

The 64 witness input inequalities give `entryMax witnessQ ≤ 63 / sqrt 5272`;
its last pivot is `sqrt 5272`, so its growth is at least `5272 / 63`.
The candidate input `51 / sqrt 3286` and 204 active inequalities give squared
growth at most `17948132 / 2601`. Their exact squared gap is
`117335164 / 1147041 > 0`. Only these sufficient one-sided consequences are
exported. The informal proof's stronger exact growth equalities, all witness
intermediate maxima, the true supremum, and a separate asymptotic conjecture
are not additional formalized claims. This reduction changes auxiliary
obligations without narrowing the original negated target.

## Dependencies, trust, and accepted review

The live sources retain Lean `v4.33.1`, Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`, LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`, and all ten exact Lake package pins.
The implementation uses the actual Mathlib Gram–Schmidt, determinant, matrix
inverse, finite maximum, square-root, and conditionally complete supremum APIs.
Integer decision and exact rational arithmetic discharge the reduced numerical
certificates; symbolic real algebra transfers them. No interval subdivision or
native-trust certificate is needed. Explicit LeanCert kernel assertions audit
material results and every export.

Two independent statement approvals preceded the accepted proof gate.
Two fresh independent final mathematical agent reviews were then accepted in
`verification/final-review-acceptance.json`. Each performed direct-source
compilation from an initially empty private project prefix using the pinned
macOS Lean toolchain and existing dependency objects read-only. Each inspected
all 17 actual elaborated theorem types, genuine declaration type/body
dependencies, and transitive axioms, and recorded 106 successful explicit kernel
assertions. The permitted axioms are only `propext`, `Classical.choice`, and
`Quot.sound`. Separate proof-free expected expressions were not imported by
the solution. Actual Linux Comparator and default-kernel replay remain pending.

The reviewers read the pinned repository review adapter and the actual Tau Ceti
common plus ten rubric sources at `afb424eda89e8ac96d9eb69f6a88972055a4cd1b`.
The Schiffer and Forsythe examples inform specification/proof separation and
trust auditing; their mathematical implementations are not imported as IE-05
proofs. Preserved third-party source excerpts retain their original attribution
and license status, including the Schiffer structural example's recorded
`UNLICENSED` metadata. Correctness, scope, proof quality, reuse, generality, API,
naming, placement, documentation, and attribution were considered within the
reviewed scope; this is no service endorsement.

The coordinator `/root` and `/root/formal_review_standards` are proof
contributors. Final referee 1 `/root/ie05_final_math_referee1` and final referee 2
`/root/mf16_final_referee` had no IE-05 implementation contribution at their
sealed mathematical review. Referee 1 subsequently authored this candidate
package, with no new mathematical changes or independent packaging approval.

## Historical preservation and next gate

The accepted original draft had 2,338 files. All remain byte-for-byte available.
Only the live README, this correspondence, and `lakefile.toml` are refreshed;
their exact prior versions are mapped individually in
`verification/candidate-package/ARCHIVE-MAP.json`. The new default target is
`Solution`. The 733-file statement freeze, 1,800-file proof freeze, both final
review seals, all failed attempts, and all 29 historical inventories retain
their exact bytes and full membership. Historical comments record their phase,
including work that is now completed.

The read-only `verification/candidate-package/verify_inventory.py` resolves
only explicit path-and-hash archive mappings. It checks all historical scopes
without applying an old whole-tree completeness rule to later additions. The
new complete candidate input selection excludes only its exact own outer path.
`audit_metadata.py` checks the pinned v0.4 schema, source-byte preservation,
17-result coverage, Solution default, credits, and pending runtime status.
These are packaging-author checks, not independent approvals. The later
independent package audit and actual Ubuntu harness with real negative controls
must be accepted before a canonical Lean-verification claim or publication.
