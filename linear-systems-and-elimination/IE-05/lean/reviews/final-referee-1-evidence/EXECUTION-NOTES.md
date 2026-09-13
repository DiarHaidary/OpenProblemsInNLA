# Referee 1 execution record

The reviewer’s initial source reads were read-only tool invocations. They read the original canonical problem and complete Markdown/TeX solution before the statement and implementation modules. The complete reviewed project inputs are bound by the proof freeze and again by this review’s outer seal; primary external source hashes, Git identities, and API excerpts are under `primary-001/`.

The following entry points actually ran in the project directory. Their child command records retain exact argument arrays, selected environment overrides, source snapshots, stdout/stderr, exit codes, and timing. No environment secrets were logged.

| Entry point | Actual result |
| --- | --- |
| `python3 reviews/final-referee-1-evidence/review.py preflight` | PASS, tool result `06ed08`; exact 1800/733 members, 27 original Git paths, 10 source pins and 9 built paths. |
| `python3 reviews/final-referee-1-evidence/review.py build` | PASS, tool session `77940`, final tool result `2f73e3`; 13 direct-source Lean commands in `attempt-001/commands/`. |
| `python3 reviews/final-referee-1-evidence/prepare-inspection.py` | Produced the initial proof-free reference types and inspector. Its executed generator and initial source manifest are retained. |
| `python3 reviews/final-referee-1-evidence/run-inspection.py run-001` | Reference compiled; inspector failed with the recorded IO lift mismatch. Tool session `3565`, final result `d5341a`. |
| `python3 reviews/final-referee-1-evidence/run-inspection.py run-002` | Reference compiled; overbroad environment-entry seeding detected the partial compiler alternative `trajectory._unsafe_rec`. Tool session `83190`, final result `3d706f`. |
| `python3 reviews/final-referee-1-evidence/run-inspection.py run-003` | Both files compiled and actual declaration inspection succeeded. Tool session `74454`, final result `4681dd`. Exact source declaration roots and full environment-entry inventory distinguish source math and its body/type closure from unrelated generated alternatives. |
| `python3 reviews/final-referee-1-evidence/exact-check.py` | Initial independent diagnostic PASS, tool result `ee3726`; its unchanged source and output were then run again under recorded child-command capture in `postchecks-001/commands/exact-check/`. |
| `python3 reviews/final-referee-1-evidence/audit-inspection.py` | Initial independent audit PASS, tool result `295346`; its unchanged source and output were then run again under recorded child-command capture in `postchecks-001/commands/audit-inspection/`. |
| `python3 reviews/final-referee-1-evidence/primary-sources.py` | PASS, tool result `71d137`; actual pinned common + ten rubric sources, three example Git blobs, and API source records. |
| `python3 reviews/final-referee-1-evidence/postchecks.py` | PASS, tool session `29389`, final result `c47490`; captured exact/audit reruns, hashed all resolved imported artifacts, matched and removed only owned private Lean objects, and rechecked original freeze memberships. |

Every failed Lean attempt has its original source snapshot and actual stdout/stderr; none was relabeled successful. `inspection-001/manifest-resolution.json` resolves the initial preparation-time source manifest to the immutable run-001 snapshots. The final edited inspector exactly matches run-003. No failed inspector produced a proof object. The reference objects produced before those failures match the recorded pre-run-003 inventory.

The initial uncaptured Python diagnostic stdout was:

```
Exact independent PASS: both QR conventions, literal Gram/LU tables and eight Schur stages; 64 witness + 204 candidate inequalities; positive gap 117335164/1147041
Independent actual-environment PASS: 17 types; 181 project / 29594 total export closure; all 157 source declarations covered; 106 successful kernel assertions; 26 material body paths
```

These diagnostics are supplemental to the actual captured postcheck executions. No source was edited between the initial and captured exact/audit runs, and their resulting JSON hashes are unchanged.

The later `seal.py` invocation creates `seal-execution.json` and the exact outer manifest; `verify-evidence.py` reads them without changing any sealed artifact. The outer includes every live file in this reviewer’s evidence directory except the exact outer path, this report, the proof-freeze file, and every one of its 1800 exact members. Other agents’ concurrent final-review files are not selected as inputs.
