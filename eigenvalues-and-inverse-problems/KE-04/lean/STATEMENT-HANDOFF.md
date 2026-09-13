# KE-04: statement-only handoff for independent review

Phase: **draft statements awaiting two fresh independent reviews**. This package
is not frozen, supplies no statement approval, authorizes no proof work, and
establishes no KE-04 theorem. All 24 Challenge theorem bodies are intentional
placeholders. No project `Solution.lean`, proof module or publication YAML exists.

Draft author: the AI agent `/root/ie05_statement_referee1`, acting here as KE-04
statement author, not as an independent referee. The coordinator `/root` provided
design feedback about positive block width and pinned spectral APIs; neither this
author nor the coordinator can count as an independent KE-04 statement approval.
The same agent's earlier IE-05 review remains a separate sealed task and is not
evidence of KE-04 approval.

The draft directory is
`/tmp/nla-lean-formalization/next-ke04-statements-draft/lean` (the host resolves
`/tmp` to `/private/tmp`). Every file below that root is included in
`DRAFT-INVENTORY.json`, including all old failures, source snapshots, nested
manifests, commands, logs and scripts. Its only excluded path is exactly
`DRAFT-INVENTORY.json` itself. The handoff and outer inventory SHA-256 values are
returned separately to the coordinator, avoiding self-referential hashes.

## Source and bounded eligibility

Permanent ID: **KE-04**. Unchanged registered canonical path:
`eigenvalues-and-inverse-problems/KE-04/README.md`.
Canonical and standards base:
`5830ed4fb06da0659414a3deb2a40ad327aca052`.
The read-only current-upstream query at `2026-09-13T06:58:52.032700+00:00` observed
that exact main commit. The canonical status there is **Solved** and the complete
canonical tree has no `lean/` project.

All-state public upstream PR title/body searches for `KE-04`, `KE04`, and
`block Lanczos` returned only the historical original Colbrook mathematical
submission #6 and the unrelated KE-05 mathematical submission #143. Each query
returned its complete result set within its recorded search scope. No competing
KE-04 formalization was found within those searches and the canonical tree.
This does not cover private, deleted or unidentifiably named work or prove
priority. Exact query strings, response item bodies, URLs, timestamps, response
hashes and commands are retained. The coordinator note is not eligibility or
statement approval. The existing campaign entry only records this assigned
statement-only track.

The complete current canonical README, Colbrook `solution.md` and `solution.tex`,
original target at `b4123194697bdf6f8f82518c1dd7d6c40a30c2e0`, original submitted
proof at `fe025e14d2639cbae59f98cacf4023d83addcb89`, detailed original informal
review and pinned repository standards were read. Seventeen original files have
exact Git-blob, source-byte, SHA-256 and actual retrieval-command bindings.
The original and current theorem/proof blocks are unchanged; the full surrounding
manuscript metadata is separately preserved and is not claimed byte-identical.

Original mathematics: Matthew J. Colbrook, Department of Applied Mathematics and
Theoretical Physics, University of Cambridge, Cambridge, United Kingdom.
The original proof discloses its ChatGPT draft origin and Codex-agent informal
review. Prospective formalization: George Stepaniants, Department of Computing
and Mathematical Sciences, California Institute of Technology, Pasadena,
California, USA, with substantial AI assistance. No George contact email is
added. No external human peer review or formal certificate is claimed.

## Exact primary draft bytes

| File | SHA-256 |
| --- | --- |
| `NLA/KE04/Definitions.lean` | `ae1baccc0cb622f83103eff8bb4a5efe4cd9a3bae4822ccca38da29554ae9ca4` |
| `Challenge.lean` | `a27de227d483072e395b6658a97cbf31296503c7fab36e5f9dbf248b2efa299e` |
| `NUMERICAL_TARGETS.md` | `ad963526a371cdfee8eaaf179674d5cabd2a1d5a9ae5b123c96ac2f2b4271c47` |
| `SourceCorrespondence.md` | `399f28847f52a6c5ff309a25b9501c0c6d4bd5a76892de2f5adaa9c25fe80a00` |
| `README.md` | `a842060b717a02f2cbc7f204b0773ee847f724d2ed0b4ceebd98a087a3b66cf6` |
| `comparator.json` | `c0c7086cb81abe8f422762d0db2cc55419828f08ba80d33f9157cb3f396a8b8e` |
| `lakefile.toml` | `1e860d6ff5d2754de834dcb8d458f3d95e4da3ad43a7b5ecbd48e91ed2f18363` |
| `lake-manifest.json` | `6590a604a552411f07cd4806d378bf6c8ed3f2cf3b957b2b41b0e7669dcf29c6` |
| `lean-toolchain` | `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71` |

The README and source-correspondence hashes above must be checked against actual
bytes and the outer inventory; prose never substitutes for that check. All 24
Challenge exports are listed in the comparator configuration with
`definition_names = []` and permitted axioms exactly
`propext`, `Classical.choice`, `Quot.sound`.

## Mathematical boundary requiring independent judgment

The target retains every original `n,p,s,k,j,i` quantifier and actual real
symmetric matrix `A`, full-column-rank starting block `V`, true block-power Krylov
spaces, actual finite dimensions, arbitrary orthonormal bases, and genuine
increasing compression eigenvalues with multiplicities. The complete canonical
largest-`s` claim and the source proof's stronger full-prefix claim are both
exported; a separate contract connects them.

There is no largest full-dimension index when `p=0`; only its existence lemma
requires `p>0`. The full-prefix theorem still includes zero dimensions, where the
source index ranges are empty. The separate index contract proves `k≥2,p>0` and
valid endpoints from `1≤i≤(k-1)p`; no target endpoint uses a total-indexing default.
Both occupancy inequalities remain strict. Endpoint separation, simplicity,
invertibility, positivity or norm bounds for `A`, and compatible Lanczos bases
are not imposed.

The spectrum directly uses the pinned `LinearMap.IsSymmetric.eigenvalues` and its
matching `eigenvectorBasis`, reversed by `Fin.rev`/`Fin.revPerm`. Monotonicity,
actual eigenvector equations, characteristic-root multiset equality and arbitrary
basis independence remain explicit semantic obligations. The direct Hermitian
APIs were compared with a custom sorted-root route before choosing this smaller
boundary. Existence of every required basis, dimension/rank equivalence and full
prefix dimensions are also explicit obligations, not presumed semantic fields.

The source's finite-dimensional proof route is exposed completely: the actual
monic degree-two `q`; a `p+1`-dimensional earlier spectral-window subspace; its
nonzero intersection with `K_(k-1)`; equality of the earlier and later quadratic
forms; conversion of a zero PSD form to its kernel; the later quadratic action
equal to `q(A)x`; and contradiction from full column rank through degree `k`.
Quadratic nonannihilation is a theorem conclusion to be proved, not a condition
inserted into Definitions or the complete target.

`compressedQuadratic` is `Q q(Qᵀ A Q) Qᵀ`, the subspace quadratic extended by
zero. Its transport obligations avoid the unwanted `ab(I-P)` term from applying
the polynomial to a zero-extended ambient first compression. Equality of the
earlier and later **forms** is asserted; only the later squared action may be
identified with `A²x`. Coincident proposed endpoints remain part of the argument
and are ruled out by its conclusion in the admissible range.

The author-written `SourceCorrespondence.md` maps all 24 obligations and gives
actual pinned API locations. Independent reviewers must judge their truth,
completeness, nonvacuity and informal-to-formal fidelity from the original sources
and full definitions, including the imported Mathlib definitions.

## Actual validation and retained limitations

Accepted author elaboration evidence:
`verification/statement-development/attempt-r5fn2nl_/result.json`, SHA-256
`a785ca2fa354af12abff313b1867ee97202920a4ccda3a32e0cee648fcd5ef93`.
Actual invocation:

```sh
python3 verification/statement-development/check_statements.py
```

This fresh attempt compiled immutable own source copies into a new private
prefix. Definitions, Challenge, a definition-only trust inspector and a target
type inspector all exited zero. Challenge emitted exactly 24 intended placeholder
warnings. All 27 concrete definitions passed explicit actual LeanCert
`#assert_trust kernel` commands and `#print axioms`; every reported transitive
axiom set contains only the three permitted foundational axioms. The definition
inspector never imports Challenge. Four private objects were hashed and removed;
their records and all exact commands, logs and source hashes remain in the result.

The host is `macOS-14.6.1-arm64-arm-64bit-Mach-O`; the binary reports Lean 4.33.1,
commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, with executable SHA-256
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.
Mathlib is pinned to `0df444a360eaa60ab8c11dca51a86af692955474`; LeanCert to
`621a43d7cf21f87872392a01e874f2f1dbddc926`. All ten dependency source pins and clean
statuses were checked before and after. The nine existing non-Cli build
directories were read directly; Cli is tooling-only and unbuilt. No package or
cache was copied, downloaded, rebuilt or modified. This uses preexisting
dependency objects; it is not a full dependency source rebuild.

The corrected final author integrity validator invocation
`python3 verification/validate_draft.py` exited zero with 127 checks. Its complete
record is `verification/validation-attempt-nxgen1so/result.json`, SHA-256
`e212f99663c1eeff69db4f819475ef82346ccb3922ae4dbd3a9f83ef90e5dd29`.
It independently re-read the 17 original Git bindings, selected external Git
bindings, actual final elaboration inputs/logs/results, target coverage and
absence of project proof files. It is still author integrity checking, not
independent mathematical approval.

The original source inventory has SHA-256
`abd69d833529a547b2418f2d16f3110142b80bce6bb38e2dde371e3dff3c24d5`.
The final 33-file API/reference inventory has SHA-256
`ed70b651127277936ceb2f80c521a81cd55b4bbe4d9be66fdad73d984aa1aaf2`.
Selected Schiffer, Forsythe and pinned Tau Ceti standards were inspected for their
documented structural/review roles; no external mathematical implementation is
reused as a KE-04 proof, and no Tau Ceti service run or endorsement is claimed.
LeanCert's concrete role is its kernel trust audit; no artificial interval work
is included in this algebraic task.

The evidence also retains failures and their limits: an initial eligibility
preflight lacking raw child diagnostics, a statement-runner reporting error for
LeanCert's silent success, two API-capture errors corrected in separate snapshots,
and an initial integrity-runner output-path error. The last overwrote an earlier
successful elaboration's final JSON; it is explicitly disclosed in
`verification/EVIDENCE-RECOVERY.md`, with the misdirected report and exact executed
script retained. That lost JSON is not accepted evidence. The final fresh attempt
named above supersedes it with intact source, dependency and object-hash records.

No theorem proof, full proof build, Comparator execution, raw-kernel export
replay, non-root Linux sandbox result, publication approval or status promotion
is claimed. Source elaboration checks types of deliberate placeholders only.

## Remaining gate

Two fresh independent statement reviewers must inspect the complete originals,
`NUMERICAL_TARGETS.md`, every actual definition, all 24 Challenge statements,
source correspondence, configured target list, pinned standards, source bindings
and exact evidence. They must record concrete findings or approval against these
bytes. The coordinator must then accept the reviews and explicitly authorize the
proof phase. No such approval or authorization is included here. Any later
mathematical boundary change requires renewed statement review.

The permanent ID, canonical path, target, original source files, canonical
status, Git state and publication files have not been changed. All work in this
handoff is isolated statement preparation.
