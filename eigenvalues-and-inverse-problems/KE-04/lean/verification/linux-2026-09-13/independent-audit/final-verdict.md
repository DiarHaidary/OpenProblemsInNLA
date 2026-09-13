# KE-04 independent operational audit — final verdict

Audit target: `sgstepaniants/OpenProblemsInNLA`, branch
`codex/lean-ke04-block-lanczos-v2`, commit
`40b0bf52e73e776e7769f0f12dbbda7cd9fff183`.

Reviewer: `/root/lean_iv01_next` (independent AI agent). Date: 13 September
2026, America/New_York. I did not implement KE-04 or contribute to its Lean
mathematics; this review covers packaging, source identity and operational
evidence only.

## Verdict

**Operational verification: PASS.** The exact KE-04 Linux job completed
successfully. The mathematical acceptance remains the two independent final
referee approvals already sealed in the candidate. The repository metadata at
this commit deliberately still says Linux and operational approval are
pending; it should be promoted only after this report is accepted and the
promotion commit records the receipt.

## Exact CI evidence

- Workflow: `Lean verification`, run `34759746409`.
- Exact KE-04 job: `103730400358`, status `completed`, conclusion `success`.
- Job head: `40b0bf52e73e776e7769f0f12dbbda7cd9fff183`.
- Artifact: `lean-KE-04`, artifact ID `10318925539`, compressed size 92,864
  bytes, GitHub digest
  `c48f544782d0d051396bb7ccca11808ea546a5254f314175dfd8e92a9c5bb591`.
  The independently fetched archive has the same SHA-256 digest.
- The extracted artifact contains the bootstrap receipt and the verify log
  set, including `result.json`, Comparator, default-kernel, sandbox,
  comparator-control, negative-axiom, dependency and user-service logs.

The workflow run's aggregate conclusion is `failure` because another matrix
job (IE-23) failed. The KE-04 job itself is independently recorded as
successful in the raw job receipt, and this verdict relies on that job's own
artifact and raw logs rather than the aggregate label.

`result.json` reports `result: comparator-accepted`, repository commit exactly
matching the target commit, project exactly
`eigenvalues-and-inverse-problems/KE-04/lean`, 24 theorem names, the expected
three permitted axioms, and source-lock hash
`b3833b07916e5db77579b9cc53ca582282f6a841f36d6a60d693e5b02d342b6b`.
The result input map has 4,250 files. An independent Git-object replay found
the same 4,250 files, with no missing, extra, or mismatched hash, and the
artifact Comparator configuration equals the committed `comparator.json`.

## Controls inspected

- The main Comparator log builds Challenge and Solution, exports all 24
  `NLA.KE04` declarations from Solution, reports only
  `propext`, `Classical.choice`, and `Quot.sound` for the declarations, runs
  the Lean default kernel, and ends with `Lean default kernel accepts the
  solution`, `Your solution is okay!`, and exit status 0.
- The kernel replay log passes all three actual `runBuiltinKernel` cases,
  including rejection of an invalid raw proof and quotient post-check.
- The sandbox probe passes private user/pid/mount/network/IPC/UTS namespaces,
  absent host parent, denied host signal lookup, denied loopback listener,
  denied AF_UNIX sockets, no effective capabilities, `no_new_privs`, UID
  1001, and nested namespace rejection. Its four malformed-option negative
  cases all reject, and the outer/export fixtures remain unchanged.
- Comparator regressions pass all five cases. The independent negative fixtures
  reject both `sorryAx` and the Lean 4.33 native-decision axiom.
- Dependency materialization and the pinned checker build both exit with zero;
  the tool receipt records Lean 4.33.1 on Linux and hashes the Comparator,
  lean4export, landrun, environment and CI sandbox probe.

Scope limitation: I did not independently re-audit all 58 pinned tool-source
files or their upstream repositories. I checked the committed source-lock hash
against the CI result and tool receipt, and inspected the executable,
environment and sandbox-probe hashes reported there. A separate source-level
audit would be needed to make a stronger claim about every dependency source.

## Independent source and package checks

- `verification/packaging/verify.py` passes all three sealed manifests:
  proof freeze 3,503 files, referee-1 evidence 3,758 files, and referee-2
  evidence 3,990 files.
- All 17 `proof_freeze.json` source records match their retained bytes,
  recorded Git blob IDs, and recorded source commits. At base `50838e3`, the
  15 shared source files are byte-identical to the retained `5830ed4` files;
  the original submission and original target are intentionally preserved from
  their separate historical commits and are not falsely collapsed.
- All ten `formalization.yaml` dependency pins match `lake-manifest.json`.
  The metadata publishes George Stepaniants and the full California Institute
  of Technology CMS affiliation without an email address. The default Lake
  target is `Solution`, and `Solution.lean` imports `NLA.KE04.Proof`.
- Comparator and YAML list the same 24 declarations. The proof modules and
  Solution contain no textual `sorry`, `sorryAx`, or `native_decide`; only the
  intentionally admitted, unimported Challenge reference contains contracts.

## Promotion note

This audit is independent of the two mathematical referee reports and did not
modify the candidate. To make the repository claim Lean verification, the
parent should update the pending status fields and receipt links in a new
commit, then run the repository metadata validator and bind the published
receipt to that exact commit. The current commit itself has a complete,
artifact-backed operational PASS.

## Evidence seal

`EVIDENCE-MANIFEST.json` binds this report, the raw run/job API receipts,
`artifact-metadata.json`, the independently downloaded artifact archive, all
extracted raw logs, and the read-only checking scripts. It lists every regular
evidence file under this directory and excludes only the manifest itself.
`verify_evidence.py` passes the sealed bundle without network access or writes.
