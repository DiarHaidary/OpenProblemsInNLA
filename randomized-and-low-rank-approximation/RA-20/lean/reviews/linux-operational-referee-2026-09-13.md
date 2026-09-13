# RA-20 independent Ubuntu operational review — 13 September 2026

**Verdict: APPROVE the actual Linux verification of candidate
`43603b173beb294c2588d83f936a8a96246fd5f0`.** The default Lean kernel replay,
statement Comparator and both real rejection/control suites passed. All twelve
exports and all 1,092 candidate Git inputs match the actual Linux receipt.
This report leaves coordinator operational acceptance and canonical publication
pending; the canonical problem is still **Solved**.

Reviewer: OpenAI Codex agent `/root/ra20_final_referee2`, independent of the proof
authors and coordinating agent who committed and pushed this candidate. I was
also the previously sealed final mathematical referee 2 and the independent
candidate-packaging reviewer. This operational task is a separate mechanical
audit, not an additional mathematical approval. I made no proof, metadata,
canonical-status or Git edit, and did not dispatch, restart or retry a workflow.
The RA-09 operational audit was consulted for structure and control-case
navigation; its results were not reused as evidence for RA-20.

## Actual run and original artifacts

The exact-head [Lean verification run 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047)
was triggered by the normal push to
`sgstepaniants/OpenProblemsInNLA:codex/lean-ra20-hollow-critical-count`.
It is attempt **1**, event `push`, and finished successfully. RA-20's actual
job is **103687982518**; the separate checker-controls job is **103687982272**.
All **17 jobs and every recorded step** completed successfully. The zero
`before` SHA on the first branch push selected all 15 projects, together with
selection and checker-controls jobs; it was not an accidental repeat dispatch.

| Artifact | GitHub ID | Original ZIP SHA-256 |
| --- | --- | --- |
| `lean-RA-20` | `10313368959` | `a988d377fa3aafbfa22349851f25872868a91c007e6ef487c6206b4d68f8f7d2` |
| `lean-checker-controls` | `10313353638` | `aaa2158a8a019683fe64f2cbdc74de7900b24f512bf46741db40c501ce4bdc6e` |

The RA-20 ZIP has 13 files and the controls ZIP has 10. I checked their complete
extracted membership, every member's bytes, archive CRCs, absence of duplicate
or unsafe paths, API digests and IDs, exact head/run linkage, and the upload-job
digest announcements. I also downloaded all **16** small workflow artifact ZIPs
and checked each against its API digest and its actual upload job. Those other
projects receive artifact-identity checks here, not new semantic proof reviews.

The original whole-workflow ZIP contains **217 log files**. Every member is
hashed and every job/step is accounted for. The separately retrieved selection,
controls and RA-20 job logs are byte-for-byte equal to their corresponding
whole-ZIP aggregate logs. All original API pages, ZIPs, raw job streams and
command receipts are retained in the
[operational evidence](../verification/linux-run-2026-09-13/runtime-verification.json).

## Committed source and review continuity

I compared the actual Git tree and batch-read Git blobs with all **1,092** live
candidate files, rejecting symlinks and tracked build artifacts. Every byte and
Git blob identity agrees. The Linux verifier's `input_sha256` map agrees exactly
with that complete candidate map and the coordinator's push receipt. The Git
author and committer are George Stepaniants with empty email fields.

The audit preserves all **521 proof-freeze inputs**, **68 statement-freeze
inputs**, and **16** original source/policy identities in their original Git,
current candidate and archived forms. Every entry and every nested manifest
byte in **17 retained inventories** was checked. This includes both complete
final-referee inventories (**699**, **793**), the installer inventory (**1,010**),
the independent packaging inventory (**1,102**), and the root candidate
inventory's ten files plus its outer manifest. The root's **1,081** previously
reviewed project files plus those **11** root evidence files account for the
entire 1,092-file candidate without overlaps or omissions.

The only historical README mapping uses the exact RA-20 project `README.md`
path together with expected SHA-256
`7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50`,
and maps it to the exact `verification/pre-candidate-README.md` archive. It does
not rename other README basenames or override other mismatches. The original
canonical problem README is a different retained source and is not remapped.
All fourteen exact hash-bound historical whitespace exceptions remain literal;
the earlier coordinator parser diagnostic is preserved, not normalized away.

The twelve actual Challenge/Solution contracts and ordered Comparator targets
agree, with no definition holes. The accepted two mathematical reports and
the independent packaging report remain bound to their exact hashes. This
audit preserves their full-target assessment: the genuine generic count three
at `n=s=3` refutes the original full four-formula conjecture. It adds no claim
about the other individual formulas or an additional scheme-multiplicity theorem.

## Real kernel, Comparator and trust checks

The actual runner reports Ubuntu 24.04 image `20260907.300.1`, Linux
`6.17.0-1022-azure-x86_64`, non-root sandbox UID **1001**, Lean **4.33.1** commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, and Go **1.27.1**. The bootstrap
receipt binds all three built executables: Comparator, `lean4export`, and
Landrun. Its source-lock and derived probe hashes agree with the **58** exact
small checker sources pinned from Forsythe revision
`8d1b0c0545a77b40245e84705aa7d273e6c81e62`.

I inspected the actual workflow, repository harness and relevant pinned checker
and sandbox code. Comparator builds and exports Challenge and Solution under
the real sandbox, compares selected constants and checks their axiom closure,
then runs the default Lean kernel and quotient post-check before its success
message. The observed main command uses `systemd-run --user`, a clean explicit
environment, `RestrictAddressFamilies=~AF_UNIX`, actual strict Landrun/Bubblewrap
and the pinned exporter. There is no skipped kernel or local macOS substitute.

The fresh project path is recorded in the actual receipt. Its Challenge graph
completed with **3,202 jobs** and its Solution graph with **3,494 jobs**. All ten
RA-20 namespace source modules and Solution were built in that fresh project.
Challenge's twelve deliberate reference admissions appear only in its build;
the Solution build has the two already frozen `letI` style warnings in
`Differential.lean` at lines 103 and 105. Those are the only Solution warnings.

The source has **61 LeanCert `#assert_trust kernel` assertions**. The actual
Linux log contains **57** standard-three printed axiom occurrences, matched
exactly by source file, line and declaration. These cover **45 distinct names**:
some supporting names print in their defining module and again in Proof.
Four kernel assertions intentionally have no print command. The twelve extra
inspector prints in each historical local final review explain its count of
69; they are not part of this authoritative source run. Every observed axiom
list is exactly `propext`, `Classical.choice`, `Quot.sound`.

The actual default kernel accepted the exported solution and Comparator
reported success for the exact twelve targets, with exit status zero. These
claims come from the original bound Ubuntu artifact and workflow job, not a
local replay of marker text or a reviewer-created Lean inspection.

## Controls, isolation and dependency scope

Both the standalone checker job and RA-20's preproof phase actually ran two
sandbox modes, four unsupported-option rejections, three raw default-kernel
controls, five Comparator fixtures and two forbidden-axiom controls. The raw
kernel rejects the invalid `True`/`False` proof; the separate quotient mismatch
passes replay and is then rejected by the required quotient post-check. The
Comparator fixtures check a valid match and the expected kind, statement and
illegal-helper rejection phases. The real `sorry` and `native_decide` fixtures
are rejected for `sorryAx` and `checked._native.native_decide.ax_1_1` respectively.

Actual isolation logs show private user/process/mount/network/IPC/UTS namespaces,
denied writes outside `.lake`, permitted designated build writes, read-only
exports, denied host-process access, denied loopback and AF_UNIX sockets, no
effective capabilities and `no_new_privs`. For the nested-namespace case,
**bwrap ran, but UID-map setup was denied before the inner write**. I do not
describe this as an executed inner write syscall. The unchanged outer/export
fixtures and all required denial outcomes passed in both runs. Complete control
texts agree after normalizing only invocation IDs, temporary axiom-directory
names, elapsed times and resource measurements.

All **ten** dependency repositories and exact revisions appear in the fresh
dependency log and agree with the committed Lake manifest. The official
matching Mathlib cache decompressed **8,690 files** successfully. This was fresh
project proof compilation using trusted matching dependency objects, not a
from-source rebuild of all Mathlib. I downloaded no dependency cache or target
object to this Mac. The small checker-source copies are evidence, not compiled
dependencies. The toolchain, dependencies, trusted Challenge and checker
infrastructure remain the disclosed trust boundary; sandboxing is not a promise
of confidentiality for host-readable files.

The exact-head [Permanent problem IDs run 34743832109](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832109)
also succeeded. Its log validates all **217** permanent IDs and reports passing
test groups of 17, 3, 16 and 11 tests. The Lean selection job separately reports
30 and 12 passing tests. No existing number, canonical target or status was
changed by this review.

## Diagnostics, privacy and final boundary

All unsuccessful retrieval and reviewer diagnostics remain retained. The first
restricted-network request could not connect; a quoted API query corrected a
shell glob diagnostic; two raw-log requests hit GitHub CLI's terminal-escape
guard and were repeated with explicit raw-output permission into files. One
reviewer assertion looked for a friendly step name in the raw job stream; it
was corrected to check that exact successful API step while retaining the raw
shell-command checks. None represents a failed Ubuntu proof run or a candidate
change. A broad privacy scan also matched a Homebrew Python-version path and
three pinned GitHub-action log filenames; their exact non-address forms were
checked, without changing original evidence bytes. No personal email was added.

George Stepaniants's authorized full Department of Computing and Mathematical
Sciences, California Institute of Technology affiliation remains in the
candidate. The original Codex resolution and Kubjas–Sodomaco–Tsigaridas conjecture
attributions remain unchanged. No private sign-in/setup receipt was read or
published, and no external human or official Tau Ceti endorsement is asserted.

The complete seal binds this report, all original candidate/frozen inputs,
every earlier nested manifest, all current operational scripts and diagnostics,
all API/raw ZIP evidence and checker-source snapshots. Only the exact new outer
manifest path is excluded from its declared scope. Its read-only verifier can
recheck hashes, membership, original ZIP identities and the precise historical
mapping without a network request or Lean run. This approval is ready for the
coordinator's independent acceptance. It does not itself publish a PR or change
the canonical status to **Lean verified**.
