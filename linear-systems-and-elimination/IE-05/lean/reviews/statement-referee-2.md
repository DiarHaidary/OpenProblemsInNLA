**IE-05 independent statement referee 2 — APPROVE**

Phase: statement-only review, 13 September 2026. Reviewer: independent Codex AI
agent `/root/ie05_statement_referee2`. I did not draft IE-05, provide its numerical
design feedback, implement its proofs, or participate in the author's checks.
This approval covers the exact bytes below. It is an automated-agent statement
review, not human peer review, a mathematical Lean verification, a statement
freeze, or permission to begin proofs before the coordinator accepts both
independent statement approvals.

I found no blocking mathematical, scope, definition, transcription, or
configuration defect. The proposed final negative theorem preserves the full
original all-dimensional extremizer equality. The reduced numerical obligations
are sufficient to refute that equality without promising the manuscript's
stronger exact growth tables.

**Reviewed inputs and immutable original sources**

| Boundary input | SHA-256 |
|---|---|
| `STATEMENT-HANDOFF.md` | `f2a38aa918a4f00a7b8f1986e80e87548827d44592ea055930051513f1aab5e0` |
| `DRAFT-INVENTORY.json` | `85265ec4d16e1c69570f5a7aab4bf068336fb84aa9e67dd3c5121a9c4eaa9568` |
| `NLA/IE05/Definitions.lean` | `aa9a18994bb8d1889af8b30290cb71846af5424436d720afaf15a54184164dfa` |
| `Challenge.lean` | `0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e` |
| `NUMERICAL_TARGETS.md` | `361c0b45ccc9e759d4ce6c910e6e75778978b49f175b6b0c043895dbabf2d956` |
| `SourceCorrespondence.md` | `3bc79e5aeefc1f5f07c6faecedb4c3bd14cdd4fa23b6aea65adce1d467b0ebc2` |
| `comparator.json` | `24bc843f6e0382012e7194c21fa441447cc75f6982b6e1995b81afabb1a5329b` |

I read the complete handoff and inventory, then independently checked the
inventory's 102 inputs plus the inventory itself. The complete project input
tree, excluding the concurrent `reviews/` outputs, contains exactly those 103
files. All sizes and SHA-256 hashes match, and exact copies are retained under
`statement-referee-2-evidence/inputs/`. `input-binding.json` records every file.
The additional `inputs/Referee2Inspect.lean` is my inspector, explicitly separate
from the 103 handed-off inputs.

I independently resolved the 27 original source/policy paths at Git commit
`5830ed4fb06da0659414a3deb2a40ad327aca052`, obtained each actual Git blob, and
compared its bytes, length, blob ID, and SHA-256 with the copied source. Every
comparison passed. The permanent registry still maps IE-05 to
`linear-systems-and-elimination/IE-05/README.md`.

I read the complete canonical README (SHA-256
`b5e980fa1f171ac540465212341dfc589d4f34d33c0b59d54a520dd3b0a4f1f5`),
the complete canonical `solution.md`
(`1b94eda6df18066f2f09b66b8b28a18ca071c0c2fb070b536dc8c798992ae434`),
its full TeX (`7282b644fa4f83612393c2a0d9679a77f0e30b10c2cad1aa94002b3c3fed3d3a`),
and the complete retained `full-proof.md`
(`18d49f30a3ef26f4c88a85c8ea1fc9e5c4e1702b4be6061d39aec892e96a4af7`).
I also read the informal review, attribution/provenance record, recovered
solution and recovery comparison, `AGENTS.md`, `CONTRIBUTING.md`, the Lean
workflow and review protocol, and the pinned harness policy. The informal
review and author's development results are background, not this approval's
independent verification.

`git-source-binding.json` binds all 27 original files, including the policy and
checker sources. This review verifies the supplied immutable source revision;
it does not claim to repeat the author's current public-PR eligibility search.

**Definitions, target fidelity, and all 17 contracts**

I inspected the entire actual Definitions and Challenge sources and printed all
41 local definitions/abbreviations from the freshly elaborated module. The
field is `ℝ`, matrices are square `Matrix (Fin n) (Fin n) ℝ`, and `Orthogonal`
means precisely `A.transpose * A = 1`. For square real matrices this gives the
usual orthogonal group and nonsingularity; neither is replaced by a numerical
test or by a pivot hypothesis.

The prescribed lower matrix has unit diagonal, zeros above it, and `-1` below
it for every natural dimension. The candidate uses the actual normalized
Gram–Schmidt procedure on `EuclideanSpace ℝ (Fin n)` columns in increasing
`Fin n` order. Inspection of the pinned Gram–Schmidt and PiL2 source, and the
actual printed definition, confirms L2 normalization by the nonzero residual's
norm. Positive-diagonal factorization and uniqueness remain universal
conclusions in `candidate_positiveQR`; they are not encoded as assumptions or
selection properties that conceal their proof.

The actual Schur step swaps only the chosen current row with row `k`, then
updates every `i,j > k` by
`B i j - (B i k / B k k) * B k j`. Inactive entries are zero. Pivot admissibility
requires `p ≥ k`, a nonzero pivot, and maximal absolute magnitude in the active
column. Thus total real division does not make an admissible path accept a zero
pivot. The separate first-available condition selects the least current row
among all maxima; the ascending scan replaces its current row only on a
strict increase. All tied choices remain available in `AdmissiblePath` and on
the supremum side. No assertion that all tie paths have the same growth is used.

The entry and stage maxima are actual finite suprema of absolute real entries,
implemented through nonnegative real norms. Growth includes exactly stages
`0,...,n-1`, including the input and final pivot, and divides by the actual input
maximum. It excludes stored multipliers and the post-elimination zero matrix.
`orthogonalGrowthSup` is the actual real `sSup` of the growths of every
orthogonal input and every admissible path. Its nonemptiness and boundedness are
conclusions to prove, not preconditions in the conjecture. The final conjecture
still quantifies over every `n ≥ 2`; dimension eight supplies its negation.

| Challenge declaration (prefix `NLA.IE05.`) | Independent assessment |
|---|---|
| `entryMax_semantics` | Genuine entrywise maximum, nonnegative, dominating and attained for `n ≥ 1`; correct nonempty-index premise. |
| `schurStep_bound` | The factor-two active bound follows from the actual partial-pivot multiplier bound and scalar triangle inequality. Row swapping stays inside the active rows. |
| `gepp_growth_bound` | Correct all-path, all-`n ≥ 1` bound with a proved positive denominator and inclusion of stage zero. The exponent `n-1` counts the last active stage. |
| `firstPath_semantics` | Nonsingularity is an appropriate premise for the generic theorem; nonzero pivots, trajectory agreement for every natural stage, and uniqueness of the tie rule are conclusions. |
| `orthogonalGrowthSet_bounded` | Requires genuine nonemptiness and an upper bound for the entire set, with bounds on every member. Identity gives a possible witness; no supremum default is exploited. |
| `candidate_positiveQR` | Full positive-diagonal QR existence for the actual candidate and uniqueness against every competing `Q,R`, in every dimension of the original target. |
| `scaledColumns_orthogonal` | A positive diagonal Gram identity implies genuine square real orthogonality after the stated column scaling. |
| `scaledLU_trajectory` | Generic unit-lower/upper factors, multiplier bounds, and positive diagonals/scales suffice to derive the first-available no-swap path and exact tail formula through stage `n`. No trajectory is assumed. |
| `integer_factor_certificates` | Both full Gram and LU identities, unit-lower and upper structure, multiplier bounds, and positive integer diagonals/scales are asserted; independent exact reconstruction passes. |
| `integer_entry_certificates` | Exactly the sufficient 64 witness input inequalities, 204 candidate active inequalities, candidate input entry, witness last scale and last pivot. Index and constant directions are correct. |
| `canonical_integer_identification` | Connects the exact integer-column candidate to the original all-dimensional QR definition at eight; the selected path is also a conclusion. |
| `witness_orthogonal_path` | Proves actual real orthogonality and the exact first-available, admissible no-swap path. These are not finite-certificate hypotheses. |
| `bounded_growth_data` | One-sided bounds have the correct direction for a larger witness growth and smaller candidate growth. Candidate nonnegativity is explicitly available for the squared comparison. |
| `numerical_gap_positive` | Correct exact rational identity and positive gap, with no floating-point or interval premise. |
| `witness_strict_growth` | Strict comparison of the actual executions, not of surrogate growth data. |
| `supremum_strict_gap` | Correct strict lower comparison with the actual real supremum, using genuine membership and boundedness. |
| `orthogonalExtremizerConjecture` | Negates the complete original all-dimensional equality, with no extra premise. |

The empty dimension has total definitions; it does not enter the original
`n ≥ 2` assertion. The generic stage and LU signatures handle empty and terminal
tails consistently. For `n=1`, the generic growth bound has exponent zero.
There is no rectangular, complex, approximate, or norm-convention substitution.

**Independent numerical reconstruction and reduction**

My new standard-library Python program imports none of the author's checkers or
numerical outputs. It parses `integerH`, `integerD`, and `integerT` directly from
the reviewed Lean source, checks the literal `integerLower` rule, and separately
parses all displayed matrices and scaling vectors from each of the canonical
Markdown, TeX, and retained full proof. They match exactly. The supplied candidate
`integerT false` also equals my independent unit-lower forward-substitution
solution of `L_8 T = H_0`, although the manuscript does not print that matrix.

The witness changes exactly one-based entry `(8,2)` from `-1` to `0`.
One-based `(7,2)` remains `-1`. The recovered witness has a different row/sign
representation and is correctly excluded from the literal formal certificate.

Independent integer multiplication verifies both Gram and LU identities, all
positive diagonals/scales, triangular structure, and all lower multiplier
bounds. Independent rational elimination agrees entry-for-entry with the
tail products, including the zero tail at stage eight. The ascending scan
selects the diagonal at all stages and correctly resolves every exact tie.
Squared normalized entries retain each column's actual denominator `D_j`;
positive column scaling preserves the pivot comparison within a column, but is
not treated as preserving the growth ratio.

All 64 inequalities `5272*H_w(i,j)^2 ≤ 3969*D_w(j)` pass. Together with a
positive input maximum and the final pivot `5272/sqrt(5272)`, they give witness
growth at least `5272/63`. A lower bound for that positive input maximum is
available from genuine admissibility/orthogonality; it need not be an additional
numerical certificate.

The actual candidate input entry `(2,2)` in zero-based indexing is
`51/sqrt(3286)`. All 204 active tail inequalities
`tail(k,i,j)^2 ≤ 5462*D_c(j)` pass. Thus the candidate numerator is at most
`sqrt(5462)` and its growth squared is at most `17948132/2601`. This argument
requires no sharp candidate input upper bound and no witness intermediate
upper bounds. The exact reduced comparison is

```
(5272/63)^2 - 17948132/2601 = 117335164/1147041 > 0.
```

My diagnostic also reproduces the stronger exact stage maxima and growth
values, as a check against the source. Those extra diagnostics are not Lean
theorems, are not additional required numerical obligations, and do not replace
any universal bridge. The one-sided reduction genuinely suffices for the full
target, including its strict real-supremum gap.

**Actual independent mechanical evidence**

I invoked the exact Lean 4.33.1 executable in the coordinator-specified toolchain.
The independently checked ten package Git revisions equal the manifest, with
clean tracked status before and after each run. Nine existing package object
directories were read in place. `Cli` is pinned, has no object directory, and
is tooling only; it is not imported. No Lake invocation, package build,
download, cache copy, or package mutation occurred.

The successful run used my own initially empty private prefix, then freshly
elaborated the snapshotted Definitions, Challenge, and my definition-only
`Referee2Inspect.lean`. The inspector imports Definitions and LeanCert's actual
verification module, never Challenge. It explicitly sets kernel trust, prints
all 41 local definitions and their actual transitive axiom sets, and runs 41
`#assert_trust kernel` commands. Every check passes. Axiom sets are empty,
`{propext}`, or exactly `{propext, Classical.choice, Quot.sound}`. Definitions
and Inspector have no warnings; Challenge has exactly its 17 intended `sorry`
warnings. No mathematical statement is proved by those placeholders.

The successful elapsed times were 8.40 seconds for Definitions, 2.90 seconds
for Challenge, and 5.68 seconds for Inspector. The three generated objects
totaled 986,352 bytes. Each was hashed, then removed from my own prefix. The
prefix is absent and the ten package revisions/statuses are unchanged afterward.

My first attempt had the same successful Lean exits, but its Python post-check
incorrectly expected apostrophes around `sorry`; Lean prints backticks. That
post-check failure is retained in `elaboration-result.json`,
`attempt-1-elaborate.py`, `attempt-1-terminal.log`, and the original raw logs.
I changed only my checker, retained the reviewed source and identical Inspector,
and reran in a second empty prefix. The successful result is
`elaboration-result-2.json`. The first attempt's own three objects were also
hashed and removed. No failed Lean or mathematical proof was discarded.

The actual Comparator configuration contains exactly the 17 advertised names,
empty `definition_names`, and only the three permitted foundational axioms.
The statements import no solution; no `Solution.lean` or proof module exists.
Comparator and an authoritative Linux run have not occurred. The definition
auditor's success establishes no theorem proof, and an eventual retained
LeanCert numerical check must explicitly use kernel trust in the actual proof
dependency chain. No artificial interval computation is required for this
rational point gap.

**Evidence, scope, and disposition**

All evidence is in `statement-referee-2-evidence/`. The actual subprocess
commands, exit codes, timings, and raw stdout/stderr are retained, along with
complete handed-off snapshots, source bindings, independent scripts, the failed
post-check and successful rerun, and final consistency checks. Material output
hashes are:

| Evidence file | SHA-256 |
|---|---|
| `input-binding.json` | `6d2b54011ee16080fd00dc31e1691367a65e60bba825948ebaae135c5741cd04` |
| `git-source-binding.json` | `42b0e4bef79bbe2bb26886782b99bb39450058e4027e55c7d4351baa8316d07c` |
| `numerical-result.json` | `9ab388b78905fc5e3606aa67dace1bcc20948dc0a1ca0826e5dee19fe144d1a8` |
| `elaboration-result-2.json` | `ff0bf76b444ab633c22d8e12c65a2d8413868dccfd6b86e8883742dc9ce5f195` |
| `logs/attempt-2-fresh-inspector.stdout` | `dbfde092442648514ad88d98dfe01f8decffa941d4567ac39e04a8c8230066e8` |

`EVIDENCE-SEAL.json` covers this report and every file in my evidence directory,
excluding exactly itself from its own scope. It includes no concurrent
other-referee directory. The report and outer seal hashes are returned to the
coordinator separately to avoid a self-hash cycle. This is an evidence seal,
not the project's statement freeze.

The principal remaining implementation work is the all-dimensional positive QR
and uniqueness bridge, nonsingular GEPP with a shrinking active block, and the
finite-maximum/supremum arguments. In particular the padded full stage matrix
has zero rows after the first step: its full determinant cannot support the
nonsingularity induction. These are visible obligations, not defects or omitted
premises. The target must be reviewed again if a mathematical boundary changes.

Source credit correctly retains George Stepaniants and his full Caltech
Department of Computing and Mathematical Sciences affiliation, Peca-Medlin's
conjecture attribution, and the AI-assistance disclosures; no email is added.
This review claims no proof of the true supremum or asymptotic constant, no
Linux verification, and no human or service endorsement. I changed no draft
definition, Challenge, canonical source, permanent ID, Git data, publication
metadata, or status. No freeze or proof gate was created.

**Final verdict: APPROVE the complete IE-05 statement boundary at the exact
hashes above. No blocking finding remains. Proof implementation must still await
the coordinator's acceptance of both independent statement reports.**
