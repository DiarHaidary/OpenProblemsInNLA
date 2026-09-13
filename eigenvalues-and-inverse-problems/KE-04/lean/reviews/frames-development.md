# KE-04 Frames: scoped author completion

13 September 2026. **Complete for the five assigned helper contracts.** This is implementation evidence, not an independent mathematical review, a complete KE-04 proof, or an authoritative Linux verification.

Original mathematical resolution: Matthew J. Colbrook, Department of Applied Mathematics and Theoretical Physics, University of Cambridge, Cambridge, United Kingdom. The original conjecture remains attributed to D. Šimonová and P. Tichý in the preserved source. Formalization credit: George Stepaniants, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. The `formal_review_standards` AI agent implemented these helpers after the accepted statement gate, and is a proof contributor rather than an independent final referee.

## Exact results

`NLA/KE04/Frames.lean`, SHA256 `bfea6b02091db4e999c2c870b4b1f238cb546ad84df010c7d5431fe82904db0b`, proves these exact frozen contracts under `NLA.KE04._proved`:

| Contract | Actual conclusion |
| --- | --- |
| `real_matrix_semantics` | Real Hermitian symmetry is transpose symmetry; `act` is the usual real matrix sum on the actual Euclidean space; `QᵀQ=I` is equivalent to orthonormal columns. |
| `krylovBasis_exists` | Full dimension of the actual Krylov subspace supplies a genuine orthonormal frame of exactly `ell*p` columns spanning that subspace. |
| `frameProjection_semantics` | `Q Qᵀ` is Hermitian and idempotent, its fixed space is precisely the actual column span, and the projection residual is orthogonal to every vector in that span. |
| `compression_semantics` | The defined compression is exactly `Qᵀ A Q`, is Hermitian, and lifting its action on subspace coordinates equals the projected action of `A`. |
| `compressedQuadratic_semantics` | The actual lifted quadratic form equals the subspace quadratic form, and genuine PSD is preserved under the lift `Q q(QᵀAQ) Qᵀ`. |

The original quantifiers and hypotheses are unchanged. All natural dimensions, including zero dimensions, are included. No compatibility between bases at different iterations, nonempty-frame condition, eigenvalue premise, or desired projection identity is added. The lifted quadratic is not replaced by the polynomial of the zero-extended first compression.

The supporting generic interfaces are `act_apply`, `act_mul`, `act_one`, `inner_eq_sum`, `inner_act_transpose`, `inner_act_left`, `inner_columns`, `frame_iff_orthonormal`, `act_eq_column_sum`, `columnSpace_eq_range_act`, `act_transpose_act`, `frameProjection_act`, `frameProjection_fixed_iff`, and `submodule_frame_exists`. Along with the five contracts, these are nineteen ordinary theorem declarations.

## Proof and library reuse

Matrix action and composition use `Matrix.toLpLin` and its actual multiplication and identity theorems. Transposition is the adjoint for the genuine real L2 inner product, proved by commuting the two finite sums. The column-span/range identity follows from the genuine column sums and coordinate vectors. This identifies the fixed space of `Q Qᵀ`; its residual-orthogonality statement then follows from the transpose left inverse.

The stronger `submodule_frame_exists` works for any submodule of the finite-dimensional Euclidean space. It uses Mathlib's `stdOrthonormalBasis` on the actual submodule, reindexes by the supplied finrank equality, and includes the vectors by the submodule's linear isometry. The mapped basis-span theorem proves equality with the original submodule. Krylov basis existence is its direct specialization. Thus the existence result is neither a frame-selection axiom nor a vacuous compatibility premise.

Hermitian compression and PSD lifting reuse `Matrix.isHermitian_conjTranspose_mul_mul` and `Matrix.PosSemidef.mul_mul_conjTranspose_same`. No new spectral theorem, orthogonal-projection object, interval calculation, or diagonalization is needed for these contracts. The matrix identities themselves establish precisely the projector properties demanded by the frozen boundary.

The rectangular inner-column/orthonormal proof pattern adapts the coordinator's earlier locally compiled IE-05 QR helper. Its exact source and the limited adaptation are recorded under `verification/frames-development/consulted-proof-pattern.json`; no IE-05 theorem or module is imported. Eleven complete pinned primary API source texts are retained with actual Git blob and SHA256 identities. The accepted package's Schiffer/Forsythe and Tau Ceti source correspondence remains preserved; no external service execution or endorsement is claimed here.

## Actual checks and trust

The final fresh attempt is `verification/frames-development/attempt-_2m2tvtu`. All three commands—Definitions, Frames, and the author's actual type/dependency inspector—exit zero. The measured sum is 21.364057333092205 seconds on Darwin arm64 with Lean 4.33.1, core commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`. Its result SHA256 is `285163aff817ba3c0000bd8944fb5619c0935e033736cdc263240c20231d9e7d`.

The mathematical sources have zero warnings. The inspector retains four transparent unused-binder warnings in the exact expected propositions: `hfull`, `hQ`, `hA`, `hQ`. These names are preserved from the frozen quantified hypotheses; the warnings do not concern an omitted proof argument or an admission. No linter is disabled to hide them.

Lean checks all five actual theorem types against assumption-free Prop-valued definitions generated from the exact frozen headers. Challenge is not imported. The inspector explicitly audits all nineteen new roots, reaches 38 actual project declarations, and confirms 34 named dependencies in the actual type/body graph. It rejects unsafe or partial project declarations, unexplained bodyless constants, reference-proposition dependencies, unfinished traversal, admissions, and axioms beyond `propext`, `Classical.choice`, `Quot.sound`.

There are 27 explicit LeanCert kernel assertions with matching standard-three reports: eight in Frames and nineteen in the inspector. LeanCert's role here is genuine kernel trust auditing; no artificial numerical certificate or native execution axiom is introduced.

Reproduction from the project directory:

```
python3 verification/frames-development/compile.py --inspect
```

Use a separate source copy for a new build if preserving the original sealed evidence directory. The read-only seal check below does not create new attempt records.

The runner starts from an empty private output prefix on every attempt and invokes only the pinned Lean executable. It reads the ten clean pinned dependency repositories and their nine existing object directories in the shared MI-22 checkout. `Cli` has no built object directory and is not imported. No Lake invocation, dependency download, cache copy, shared build write or Git mutation occurs. Each attempt snapshots all actual source inputs, commands and complete logs; only its own generated `.olean`/`.ilean` objects are hashed and removed.

## Attempts, preservation and remaining gates

Three actual attempts are retained. The first, `attempt-gv4tb6yr`, passed Definitions and the substantive projection/compression/quadratic arguments but failed at the basis-span transport because `Set.image_range` is not the pinned API name. The correction uses the actual `← Set.range_comp` theorem. An unused deprecated simplifier argument was also removed. The failed error-recovery axiom reports are retained and are not presented as proof success. The second, `attempt-irwnym99`, passed both mathematical modules with zero warnings. The third is the complete fresh source/type/dependency run named above; it required no mathematical or inspector corrections.

`audit_result.py` independently rehashes the retained author run, all 1598 frozen statement-package inputs, all seventeen original source/Git snapshots, the ten current clean source pins, all eleven API snapshots, all attempt input/log bytes, exact expected headers and cleanup records. This is an evidence check by the implementing agent, not an additional independent referee. `verify_seal.py` performs the read-only scoped integrity check without rerunning Lean or overwriting the audit result.

The seal includes the new Frames source, this report, its complete owned evidence and explicit immutable statement/configuration boundaries. Concurrent Krylov/Spectral and later assembly modules are excluded. All prior frozen source, statement, review and policy bytes remain unchanged. The historical statement-only text in those files remains historical. No complete-proof freeze, Solution, formalization metadata, status promotion, problem-ID change, commit, push or publication is made. Complete assembly, two eligible independent final mathematical reviews and actual Linux Comparator/default-kernel checks remain later gates.
