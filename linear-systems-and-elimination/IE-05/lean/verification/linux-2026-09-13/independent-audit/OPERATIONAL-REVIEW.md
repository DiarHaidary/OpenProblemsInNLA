# IE-05 independent operational review

**Verdict: PASS for IE-05's actual Ubuntu verification, workflow attempt 1.**

Reviewer: OpenAI Codex agent `/root/leancert_examples`, 13 September 2026. I contributed neither IE-05's statements, proof, candidate packaging nor Git publication. This is an independent operational review, not a new mathematical referee approval or final publication/PR approval. The two previously accepted mathematical referees remain `/root/ie05_final_math_referee1` and `/root/mf16_final_referee`.

## Exact verification identity

- Candidate: [`71cf72f9db2af0f01b5cfa7f18a69e28310eb52f`](https://github.com/sgstepaniants/OpenProblemsInNLA/commit/71cf72f9db2af0f01b5cfa7f18a69e28310eb52f), branch `codex/lean-ie05-orthogonal-extremizer`.
- Project: `linear-systems-and-elimination/IE-05/lean`.
- [Workflow 34751393873, attempt 1](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34751393873/attempts/1); [IE-05 job 103708463461](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34751393873/job/103708463461), successful from 10:16:12 to 10:20:28 UTC.
- The independent checker-controls job `103708463293` also succeeded. Every step of these two jobs succeeded.
- Actual runner: Ubuntu **24.04.5**, image `ubuntu-24.04`, x86_64; sandbox UID **1001**. Linux Lean **4.33.1**, compiler revision `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Go **1.27.1**.

The overall attempt-1 workflow concluded **failure**: 18 of 20 jobs succeeded, while only MI-06 (`103708463532`) and RA-07 (`103708463566`) failed. Their original logs show HTTP **500** while downloading the elan installer, before their proof checks. This does not invalidate the successful IE-05 job. A later coordinator-authorized failed-job retry is outside this report; no retry result is used here, and I neither dispatched nor reran a workflow.

## Sources and retained evidence

I independently downloaded the completed run/job/artifact API records and both original artifacts. The uploaded ZIP SHA256, GitHub artifact metadata, locally downloaded ZIP digest and every extracted byte agree:

| Artifact | ID | ZIP SHA256 | Extracted files |
|---|---:|---|---:|
| `lean-IE-05` | 10316715133 | `e2740cccc2531b1f4a41b08d885199a1c8488ef2f95b9a3acbc8424525da631a` | 13 |
| `lean-checker-controls` | 10316610253 | `b5e5f5491af333ddba936929ede04ab930be234e40720a613b5bc17815c12874` | 10 |

The IE-05 extraction also equals all 13 files originally retained by the coordinator. Archive CRC checks passed; extraction rejects duplicate members, symlinks and escaping paths. Complete individual IE-05, checker-controls, selection, permanent-ID, MI-06 and RA-07 job logs are retained. The full-run logs endpoint returned a valid **empty ZIP**, also preserved; I make no claim that this empty archive contains all workflow job logs.

`candidate-binding/` records the immutable Git tree/blob identities, source hashes and selected verbatim mathematical/governance files. The full 2,543-file candidate was hashed directly from actual Git objects; every candidate working-tree byte and the entire `result.json.input_sha256` map match. No `.lake` or compiled object is among these committed inputs. The large duplicate source tree was not copied: immutable Git objects plus complete per-file identities preserve that boundary without unnecessary disk use.

The successful independent read-only audit is `audit-8mi1v2oq/result.json`, selected by `AUDIT-LATEST.json`. Its scripts and every command, stderr, original attempt and consulted source are retained. The complete evidence directory, including this report, is bound by `EVIDENCE-MANIFEST.json`; only that exact outer file is excluded from itself. `verify.py` checks the seal without writing or invoking Lean.

## Mechanical verification

The actual Comparator log separately builds the frozen Challenge (**2,380 jobs**) and the submitted Solution (**3,089 jobs**). The only Challenge holes are its 17 deliberate statement placeholders. All project implementation modules and the Solution are built from the fresh committed-source snapshot. The log then exports **all 17 configured declarations** from each side, accepts the Solution with Lean's **default kernel**, and reports `Your solution is okay!`, exit 0.

The actual runtime configuration is exactly the committed `comparator.json`: no definition holes, 17 distinct theorem names, and only `propext`, `Classical.choice` and `Quot.sound` permitted. The build prints **89 source axiom reports**, each exactly those three axioms. This is the observed Linux count; the earlier mathematical referees' 106 checks additionally include their separate 17-export inspectors and are not presented as 106 Linux source reports.

I inspected the pinned Comparator axiom traversal and statement/dependency comparison code, and the harness's fresh Git snapshot, source-lock checks, exact configuration validation, clean environment, unchanged-input checks and actual default-kernel invocation. Acceptance is therefore not inferred merely from a generic build-success line or a local macOS build.

Both the target job and the separate checker-controls job ran all of these actual controls:

1. **Three default-kernel cases:** honest inductive/quotient proof accepted; invalid raw proof rejected by the kernel; quotient post-check mismatch rejected after raw replay.
2. **Five Comparator cases:** matching theorem accepted; declaration mismatch, extra axiom, kind mismatch and theorem type mismatch rejected. The retained case logs identify their actual rejection phases.
3. **Two axiom fixtures:** the real `native_decide` theorem is rejected for `checked._native.native_decide.ax_1_1`; the real `sorry` theorem is rejected for `sorryAx`.
4. **Actual build/export sandbox probes:** outside writes, truncation, creation and symlink escape denied; build writes permitted only in its designated `.lake`; export `.lake` writes denied; private user/PID/mount/network/IPC/UTS namespaces, absent host-parent PID, blocked host loopback and AF_UNIX, no effective capabilities, and `no_new_privs` verified. Unknown or excess writable options are rejected. The outer and export fixture files remain unchanged.

The attempted nested namespace write was rejected at Bubblewrap's UID-map setup (`Permission denied`), in both modes. This proves rejection of that actual attempt; it does not claim a write was tested inside a successfully created nested UID namespace. Host-file confidentiality is not claimed by a read-only-host sandbox; credential isolation relies on the dedicated GitHub runner and the recorded clean execution environment.

The ten dependencies were freshly cloned and checked out at exactly the committed revisions, including Mathlib `0df444a360eaa60ab8c11dca51a86af692955474` and LeanCert `621a43d7cf21f87872392a01e874f2f1dbddc926`. The run actually downloaded/decompressed **8,690 matching Mathlib cache files**. It is not described as rebuilding all of Mathlib. The project sources were compiled fresh, and the exported solution was replayed by the default kernel.

All **58** tool-source lock records were independently checked against original Git blobs at Forsythe `8d1b0c0545a77b40245e84705aa7d273e6c81e62`; source-lock SHA256 is `b3833b07916e5db77579b9cc53ca582282f6a841f36d6a60d693e5b02d342b6b`. The exact CI probe derivation matches recorded SHA256 `31057195baf238807cacbb4126c5b07f02cec55a4e4437de5f3a755b3fada803`. The independently built target/control jobs report identical checker/exporter/Landrun binary hashes and receipt identities. No native or custom axiom is permitted for an IE-05 target. LeanCert's role in this exact algebraic proof is its kernel-trust audit tooling; no unused or artificial interval certificate is claimed.

## Mathematical-review and candidate preservation

I checked the complete canonical target, compiled-boundary source, source correspondence and candidate scope against the actual selected exports, without representing this operational check as another proof referee. The package retains the full original universal orthogonal GEPP growth-extremizer claim, actual positive-diagonal Euclidean QR candidate, all admissible partial-pivot ties, first-available-row convention and genuine nonempty bounded real supremum. Its order-eight counterexample proves the negation of that full claim. The strict witness comparison is supported by the exact squared gap `117335164/1147041`; the package does not assert the true supremum or a different asymptotic result.

The accepted review gate `6e1de72e81a0603066544133f7bb52a7217b31bd6f05372a8c1abe109ff03d61` and both referee reports are unchanged. Independent rehashing checked:

- all **1,800** proof-freeze inputs (`72d9a694d6c337937c6edd28ee632dc4a92464ac2dc7ba58ef98f5322405f251`);
- all **733** statement-freeze inputs (`bd329885eb323bd4f3fd40879649b56c201918d8c2bd6f63fbd0e86f48ca770c`);
- all **27** original source Git blobs at their recorded source paths;
- all **2,338** accepted pre-packaging files, using only the three exact path-and-hash wrapper archives for README, source correspondence and Lake defaults;
- all **29** discovered historical inventories, including their nested manifests and earlier failures;
- all **4,854** installed independent-packaging inventory members, and the later coordinator installation seal.

No blanket basename exclusion was used: all 13 candidate files named `EVIDENCE-MANIFEST.json` remain in the runtime input binding, and their historical selections were preserved. The original permanent ID/path and canonical target page are byte-identical. The actual permanent-ID workflow `34751393871` passed, validating all **217** registered IDs and all **17** ID regression tests. The actual selection/harness test steps also succeeded. The committed candidate has no local changes, and both commit author and committer are **George Stepaniants with empty email fields**. Public wrappers retain George's name and **Department of Computing and Mathematical Sciences, California Institute of Technology** affiliation without a contact email; original mathematical authorship is retained rather than reassigned.

## Publication boundary and diagnostics

This operational gate is ready for coordinator acceptance and subsequent publication preparation. The canonical page remains **Solved**. Its candidate wrappers intentionally retain their earlier pending/uncommitted phase statements. Before promotion or a final upstream PR, update the live publication wording with the exact immutable candidate, this actual attempt-1 evidence and accurate reviewer roles, retain the historical wrappers as archives, and perform the separate final publication/PR review. This report does not change status, authorize a count increment, imply a merged PR or certify unrelated retry jobs.

All audit-local failures are retained. Initial Git lookup in the user's other checkout could not find the candidate object; the correct isolated IE-05 checkout was then used. Initial GitHub CLI raw-log requests refused ANSI sequences; the documented `--allow-escape-sequences` flag was used only to capture original bytes into files. The first local metadata audit used system Python without PyYAML; the existing pinned metadata-validation environment passed the same schema/coverage check. No proof/source change or CI rerun followed any of these diagnostics.

I performed no local Lean build, dependency copy, Git mutation, candidate edit, status edit, dispatch, commit, push or PR action during this review.
