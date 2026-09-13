# IS-02 independent final proof review 1

**Verdict: APPROVE the complete mathematical formalization at the hashes
below.** No substantive correction to the definitions, nine public theorem
types, or their proofs is required. The independent local proof build, all
nine frozen-contract checks, and the transitive axiom audit passed. Publication
still requires the separate Linux Comparator and repository verification gates.

Reviewer: `/root/nr03_statement_referee2`, an independent Codex AI agent,
acting as IS-02 final referee 1. Date: 13 September 2026. I did not author or
edit any IS-02 candidate file. This review covers mathematical fidelity,
correctness, complete scope, proof quality, reuse/API, documentation and
attribution under the repository's Tau Ceti adaptation. It is not an official
Tau Ceti service run, external human peer review, or an independent Linux
Comparator run.

## Reviewed source and statement freeze

Candidate:
`/tmp/nla-lean-is02-project/eigenvalues-and-inverse-problems/IS-02/lean`.

| File | SHA-256 |
|---|---|
| `NLA/IS02/Definitions.lean` | `4d2d2914838a91a30f12b1e20490c957d2b4e943eb2a51f7415cc2fedd0bf321` |
| `Challenge.lean` | `d72b58465096cb7049d453206727837eb53b87845a5d8faa97d88f5fb9244cff` |
| `NLA/IS02/Proof.lean` | `f108eb9d89a524514bd24b6cc379bc500b03d00143b49b14938aa75cbe72bde8` |
| `Solution.lean` | `8cf1db571f72a181107bd5cbea8910bc2fd4ff6266bbea2218783ea88cdba545` |

I read the canonical README and complete source solution directly from
upstream commit `50838e37dd793830e2cecd1055cfc7e0349490f1`, through Git in the
KE-04 worktree. The canonical README has SHA-256
`92f7c04c5ac0be67a7f6a4efd0d2439caaf000295fa27d259e01a22368f7ae24`;
the complete source solution Markdown has SHA-256
`ae29570308b2a78678875c5e56076ce09e65cea732ce6b51142399a4b234577f`.
The associated TeX source bytes, source hashes and raw Git commands are also
retained. The protocol is `docs/lean/REVIEW.md`, SHA-256
`d967ddce620d4e754e2f9c25548f30cb537f76f4ddcf8ecf2574945bcd332553`.

I read both independent statement reports and the coordinator acceptance.
The two report hashes are exactly
`26d6a4900e8c237459425e4b95a5b3c9d0101df5d7a6d564fc76a6a3ca897c4d`
and `a7dcdb93bbb0b3e98f72b73c3a88790092d8d362a289251dbc9148a711f5e5a2`.
The current Definitions and Challenge match the bytes approved in those
reports. This confirms the recorded mathematical boundary has not changed;
the claimed pre-implementation chronology is the preserved review and
coordinator record, not a fact inferred from a file modification timestamp.

All candidate inputs actually inspected are preserved in `candidate/` with
`candidate-hashes.json`. I then read every line of the 1,354-line Proof file,
all of Solution, all definitions and contracts, and the numerical/source
mapping and metadata. I did not substitute the earlier statement approvals
or the implementer's reported successful build for a proof review.

## Complete target fidelity

The ambient matrices are actual real square matrices on `Fin n`. Symmetry,
entrywise nonnegativity, row sums equal to one, and the full trace are the
canonical conditions. The uniqueness predicate quantifies every real
competitor in that polytope. Neither rational entries, block structure,
support connectivity, nor a finite candidate list is assumed for a competitor.
Simultaneous permutation of both indices is precisely permutation similarity;
using the inverse convention for the permutation does not change its
existential meaning.

The spectrum definition is equality of actual Mathlib characteristic
polynomials. The general exported
`sameSpectrum_iff_realEigenvalueMultiset_eq` proves its equivalence to equality
of real root multisets for both symmetric matrices. In `test_spectrum_bridge`,
the hypotheses are converted to Hermitian matrices, their characteristic
polynomials are proved to split through Mathlib's `splits_charpoly`, and the
monic product-over-roots formula reconstructs each polynomial. The forward
implication takes the roots of equal polynomials. Root multiplicities are
retained, and there is no assumption of splitting or of the required spectrum
as a new axiom. The empty-dimensional helper case is included by the imported
theorems; the canonical target itself remains restricted to `n ≥ 4`.

The vertex predicate is the genuine extreme-point condition in the same
symmetric-stochastic set. An interior convex combination must have equal
endpoints; the endpoint cases are explicitly allowed. No replacement of
vertices by permutation matrices occurs. The locus contains all three
families: `[I,C_n]`, every `[I,V]`, and every `[C_n,V]` for such a vertex.
Each segment uses all real parameters in the closed interval `[0,1]`.
At every dimension relevant to the original problem, `flatMatrix` is exactly
the zero-diagonal matrix with off-diagonal entries `1/(n-1)`.

The four-dimensional witness is the source's swap block direct-summed with
the all-halves block. Its positive trace is proved, rather than added as a
hypothesis. The final theorem negates the complete universal necessary
condition at the allowed dimension four. It does not claim a classification
in every dimension or a weaker finite witness identity as the whole result.

## Actual proof path for arbitrary real competitors

The implementation gives a valid, more direct finite-dimensional alternative
to the manuscript's support-component classification. I checked the entire
path, including every support-position lemma and all cases of its use:

1. `test_spectrum` computes the witness's actual characteristic polynomial and
   identifies it with `diag(1,1,0,-1)`. It expands the small polynomial
   determinant and uses exact rational algebra. `test_trace_from_spectrum`
   obtains trace one for any competitor from the characteristic polynomial's
   next coefficient, using Mathlib's trace formula.
2. `test_minus_one_root` and `test_minus_one_eigenvector` pass from the actual
   root `-1` to a genuinely nonzero real vector `z` satisfying `B z = -z`.
   They use the verified finite-dimensional characteristic-polynomial/eigenvalue
   theorem and the matrix-to-linear-map bridge. No eigenvector is postulated.
3. `test_quad_zero` derives
   `B i j * (z i + z j)^2 = 0` for **every** pair of indices. Symmetry gives
   column sums one. The double sum of these nonnegative terms is zero by row
   sums, column sums, and the eigenvector equation. Each term is bounded above
   by the full sum and below by zero. This is the source's sum-of-squares
   identity, proved directly in Lean.
4. The final uniqueness proof performs the exhaustive sixteen-way split of
   the four propositions `z i = 0`. All four zero contradicts `z ≠ 0`. All
   four nonzero forces every diagonal entry of B to vanish, contradicting
   trace one. A single nonzero coordinate forces its entire row to vanish,
   contradicting stochasticity.
5. In each of the four three-coordinate support cases, the diagonal and
   crossing entries vanish. Symmetry and row sums force every off-diagonal
   entry of the remaining three-by-three block to equal one half. Its
   eigenvector equations then force those three coordinates to zero, a
   contradiction. These are exact identities for arbitrary real B and z,
   rather than numerical sampling of their values.
6. In each of the six two-coordinate support cases, the support block has
   diagonal zero and off-diagonal one. The other block is symmetric stochastic;
   trace one forces its four entries to equal one half. Every entry of B is
   then identified with a concretely specified simultaneous permutation of
   the witness. All six permutations and the ordering conventions are checked
   by the respective `test_pair*` proofs.

Only the support pattern is enumerated; the entries of B remain arbitrary
reals throughout. The proof does not need to formalize a general graph
component-count theorem because the stated four-dimensional case is fully
resolved by the above argument. In particular it does not assume the source
classification that it is meant to justify.

## Genuine vertices and the entire locus

`splitId` and `splitSwap` are explicitly proved symmetric, nonnegative and
stochastic. The witness is their exact midpoint, and their `(2,2)` entries
prove they are distinct. Applying the intrinsic vertex condition at one half
therefore proves `¬ vertex 4 counterexample`.

For `[I,V]`, the zero `(0,0)` witness entry and nonnegativity force the segment
parameter to be one, which would identify the witness with a vertex. For
`[C_4,V]`, its zero `(0,2)` entry, the positive flat-matrix entry `1/3`, and
nonnegativity likewise force the parameter to be one. Both produce the
nonvertex contradiction. For `[I,C_4]`, the proof compares two unequal
diagonal witness entries; every matrix in that segment has equal diagonal
entries, so membership is impossible. This is a valid short alternative to
the manuscript's off-diagonal argument and covers all endpoints.

`test_outside_locus` explicitly eliminates the union and both vertex-indexed
alternatives. `test_counterexample_claim` combines membership, positive trace,
spectrum, uniqueness and exclusion. `test_not_targetNecessaryCondition`
instantiates the universal target at four with precisely these proved
hypotheses, then contradicts the full exclusion. There is no restriction to
a selected collection of vertices or omission of a segment family.

## All nine public contracts and independent Lean checks

I ran `run_review.py`, which checked the exact expected Proof and Solution
hashes, both frozen statement hashes and both statement-review hashes. It
checked all ten dependency revisions against the manifest and confirmed each
tracked dependency source tree was clean. It then ran the supplied
`verification/proof-typecheck.sh` under `bash -x`, with the explicit pinned
Lean binary, read-only pre-existing MI-22 dependencies, and fresh private
objects. It did not run Lake, download anything, rebuild dependency objects,
or write candidate objects. The command exited zero.

The actual Lean binary reported version 4.33.1,
`arm64-apple-darwin24.6.0`, compiler commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`. Definitions, Proof and Solution
were re-elaborated. All nine public `#assert_trust kernel` commands succeeded;
their printed transitive axiom sets were exactly `propext`, `Classical.choice`
and `Quot.sound`. The proof produced only nonblocking style/linter warnings,
not placeholder or proof errors. Raw commands, environment, output prefix,
stdout, stderr and exit codes are in `command-results.json` and
`proof-typecheck.log`.

I separately ran `InspectSolution.lean`, printing every definition, every
proof/helper declaration type, and every public export type. Its 47 additional
LeanCert kernel assertions succeeded. Across all 65 definitions, helpers and
public declarations, the independently printed axiom sets contain exactly
the same three standard axioms. I inspected the expanded original-target
definitions and all nine expanded public types.

I also generated `FrozenBoundaryCheck.lean` from the exact approved Challenge
signatures and type-checked every contract using its completed public
declaration. All nine checks passed, with no Challenge import:

| Contract | Completed proof |
|---|---|
| `counterexample_symmetric_nonnegative_stochastic` | Exact membership of the displayed matrix. |
| `counterexample_trace` | Trace exactly one. |
| `counterexample_positive_trace` | Strict positive trace. |
| `counterexample_spectrum` | Actual characteristic polynomial agrees with the four-entry diagonal spectrum. |
| `sameSpectrum_iff_realEigenvalueMultiset_eq` | General real symmetric characteristic-polynomial/root-multiset equivalence. |
| `counterexample_spectral_uniqueness` | Every real symmetric-stochastic competitor is permutation-similar. |
| `counterexample_outside_locus` | Exclusion from all three segment families with genuine vertices. |
| `counterexample_claim` | Complete counterexample with every required property. |
| `not_targetNecessaryCondition` | Negation of the full original universal statement. |

These local type checks are independent audit evidence; they are **not**
reported as a Comparator run. `inspection-command-results.json`,
`InspectSolution.log`, `FrozenBoundaryCheck.log`, and the actual inspection
sources preserve precisely what was checked.

## Reuse, metadata and nonblocking improvements

The implementation appropriately reuses Mathlib's matrix spectral theorem,
characteristic-polynomial splitting, monic root reconstruction, real
eigenvector existence and trace-coefficient formula. I inspected the pinned
dependency sources for those key bridges and LeanCert's actual
`#assert_trust` implementation; excerpts and source hashes are recorded in
`dependency-api-inspection.json`. No extra mathematical axiom or trusted
numerical certificate was added. Exact `norm_num`, `ring` and `linarith`
proofs remove any need for numerical interval subdivision.

The nine YAML result entries cover exactly the nine Comparator exports and
Solution declarations. The v0.4 schema check passes, dependency pins agree,
all source-map file hashes and Git blob IDs agree with the original sources,
and the observed standard axiom sets match the stated ones. Challenge's nine
deliberate placeholders remain outside the proof import closure; the zero
proof-hole claim concerns the completed Solution closure. The metadata and
README honestly leave final review, Linux Comparator and promotion pending.
The license is present, Matthew J. Colbrook retains mathematical credit, and
George Stepaniants receives formalization credit with his department and
Caltech affiliation, without publishing his email.

The following are nonblocking publication/API suggestions, already sent to
the coordinator:

- Clarify `automation.methods[0].tool_setup`: LeanCert supplies the kernel
  trust assertions, while the arithmetic itself uses Mathlib tactics. The
  current wording can sound as though LeanCert performed interval/numerical
  calculations, which it did not.
- The `test_*` helper names and duplicated support-position proofs could be
  made more descriptive or factored later. They are complete mathematical
  lemmas, not tests over a finite sample. This is a maintainability suggestion,
  not a demand to change the already verified proof before publication.
- The local proof script assumes its dependency tree is pinned; it does not
  itself check all revisions. This referee independently performed those
  checks before invoking it. Reproduction documentation should distinguish
  that precondition from the script's direct elaboration function.

No proof source change is requested. Metadata-only corrections can be
reviewed separately without changing this mathematical approval's four
source hashes.

## Limits and evidence integrity

This is an independent final mathematical review plus a real local macOS
Lean re-elaboration and axiom audit. It is not a claim to have run Linux
Comparator, rebuilt every dependency from source, completed the separate
sandbox/default-kernel CI workflow, obtained human peer review, or authorized
a catalog-status change. The coordinator must complete those remaining
operational gates and the second final referee review before publication.

The record contains no candidate edits or Git/status mutations.
`EVIDENCE-MANIFEST.json` hashes the compact source snapshots, audit scripts,
logs and report. Rebuildable private `.olean` files and shared dependency
objects are intentionally excluded; raw command records identify their
actual locations. The mathematical verdict is tied to the explicit source
hashes above, not to an unqualified statement that a directory or branch is
verified.
