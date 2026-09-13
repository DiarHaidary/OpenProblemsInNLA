**IE-05 coordinator-helper evidence preflight — PASS**

This is a mechanical preservation and provenance audit performed after both
independent statement reports were sealed. It is not a third mathematical
approval, a statement freeze, a proof gate, a proof implementation, or a Linux
Comparator run. The verifier and every result retain `proof_authorized: false`.
The coordinator must make the acceptance and authorization decision.

The portable `verify_preflight.py` reads inputs and writes JSON to stdout. It
does not execute either referee's driver, inspector, arithmetic checker, or seal
script. Those sources were read and their recorded evidence independently
checked. It performs no writes, Lean compilation, Git mutation, package build,
download, or cache copy. The actual fresh read-only Git and Lean-version commands
and complete stdout/stderr are embedded in its result.

Reproduce from the IE-05 Lean project, directing stdout to a new location if
desired:

```
python3 -B verification/statement-gate-preflight/verify_preflight.py \
  --project /path/to/IE05/lean \
  --source-repo /path/to/repository-containing-the-pinned-source-commit \
  --packages /path/to/the-ten-read-only-pinned-package-directories \
  --lean /path/to/Lean-4.33.1/bin/lean
```

The complete reviewed input set is 718 files: 103 draft inputs, referee 1's
124-file closure including its outer manifest, and referee 2's 491-file closure
including its outer seal. The two outer membership checks cover exactly 123 and
490 members respectively and exclude exactly their own outer path. Every byte
count and SHA-256 matches. Both complete reports and both seals remain unchanged.
The proposed input binding records all 718 files and explicitly is not a freeze.

The verifier checks all 103 files against both complete snapshots, all 27
original source/policy files against actual immutable Git blobs at
`5830ed4fb06da0659414a3deb2a40ad327aca052`, the permanent IE-05 registry path,
and every internal inventory and source snapshot. The complete original input
tree has no unlisted files. Only this exact new preflight output subtree is
excluded from that historical input-tree comparison. The original historical
drivers' broader live-tree assumptions are preserved; they were not edited or
rerun after adding preflight outputs.

All 111 nested JSON documents are parsed with duplicate-key rejection and are
bound by the draft inventory or one of the complete reviewer seals. Checks
cover the nested draft/source inventories, inspector manifests, exact package
manifests, historical attempt inputs/logs and cleanup receipts, latest-result
and reconstruction pointers, current actual API source identities, and the
source-bound policy source-lock structure. External harness payloads and
Schiffer/Forsythe structural-example records remain historical metadata; no
remote retrieval or harness execution is implied.

The actual source has precisely 41 definitions/abbreviations and 17 Challenge
declarations. All configured names match. The retained fresh contract inspector
prints all 17 actual elaborated types, which are bound individually alongside
their source signatures. Both definition-only inspectors cover every one of
the 41 definitions with actual `#print axioms` and explicit
`#assert_trust kernel`; both have the same axiom distribution: 32 standard-three,
four `propext` only, and five empty sets. The only Challenge warnings are its
17 reference placeholders at the actual declaration lines. Empty
`definition_names` and the exact foundational whitelist are checked.

The historical execution distinctions are retained exactly:

- Referee 1 ran four fresh Lean commands, all exiting zero. Its outer driver
  then exited one because its postprocessor omitted five empty-axiom reports.
  A separately retained audit of those immutable logs passed. It was not
  another Lean compile, and the failed driver/result remains unchanged.
- Referee 2's first three fresh Lean commands exited zero; its postprocessor
  then failed on the apostrophe/backtick spelling of `sorry`. It preserved that
  failure and ran all three commands again in a second empty prefix with the
  corrected checker. The second outer check passed. Both own prefixes were
  hashed and removed.

The actual ten current package Git pins match the manifest and have clean
tracked source. Nine existing object directories are used by the independent
reviewers; tooling-only `Cli` has no object directory and appears in neither
reviewer's import path. Nine API sources and 26 recorded existing imported
object files were independently rehashed read-only. Lean's binary identity and
actual `--version` output agree with both reports. Removed private objects are
not available for new hashing; their retained hashes, matching shared module
identities, cleanup receipts, and current absence are checked without claiming
a new object build.

The two exact arithmetic receipts agree on all 64 witness inequalities, all
204 candidate active inequalities, the `(8,2)` modification, scale and diagonal
data, and the exact positive gap `117335164/1147041`. These are diagnostic
receipt checks, not Lean theorems.

The successful run is `attempt-2.stdout.json`, with its exact command receipt
in `attempt-2-command.json`. It contains 85 actual read-only command receipts
and nine completed check groups. `preflight-result.json` is the compact receipt;
`proposed-input-binding.json` is extracted exactly from the successful result.
The current verifier and its successful source snapshot are identical.

My first preflight completed the seal, source, inspector, command, dependency,
and nested-manifest checks, then stopped at a numerical manuscript binding
because my helper expected `bytes` in a record that supplies only `sha256`.
This was my schema assumption, not a source/evidence defect. I preserved the
complete first script, JSON/traceback, stderr, and command receipt. The correction
checks that SHA-only field directly, while the original-source inventory still
independently checks its byte count. The corrected complete run passed.
Earlier display-only inspection diagnostics are retained separately.

`EVIDENCE-SEAL.json` seals every file under this new preflight subtree except
exactly itself. It does not add or alter either historical referee seal.
It is an evidence archive, not a statement freeze or proof authorization.
