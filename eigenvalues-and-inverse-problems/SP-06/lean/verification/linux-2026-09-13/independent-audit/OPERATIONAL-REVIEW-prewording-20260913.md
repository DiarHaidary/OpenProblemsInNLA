# SP-06 independent Linux operational review

**Reviewer:** OpenAI Codex agent `/root/lean_ie15_next` (AI agent; I did not author the SP-06 proof candidate).  **Review date:** 13 September 2026.

## Verdict

**PASS — authoritative Linux operational gate for the pushed SP-06 candidate.** The terminal GitHub Actions run fetched the exact candidate commit, completed the real non-root Linux sandbox and project verification, and returned success. This report is an operational audit of the submitted bytes and receipts; it is separate from the two local mathematical final reviews and does not itself change catalog status or publish a PR.

## Identity and terminal run

- Fork/repository: `sgstepaniants/OpenProblemsInNLA`
- Branch: `codex/lean-sp06-jordan-curve`
- Candidate commit: `3122d69460b0ed6dda3ea00dfaa899f93411ce2f`
- Workflow: `Lean verification`, run `34765629739` (event `push`)
- Run URL: https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34765629739
- Verify job: `103745998196`, `verify (SP-06, eigenvalues-and-inverse-problems/SP-06/lean)`
- Job URL: https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34765629739/job/103745998196
- Final observed run state: `status=completed`, `conclusion=success`.
- Final observed verify-job state: `status=completed`, `conclusion=success`, 15:27:18Z–15:30:43Z.

I waited for the run to leave its running state before issuing this verdict. The raw `run.json`, `run-api.json`, `verify-job-api.json`, and complete `verify-job.log` are retained here.

The separate `checker-controls` matrix job `103745998768` was **skipped**, as the workflow condition permits when checker/tooling files are unchanged. The verify job itself ran the project-side sandbox, kernel replay, Comparator regression, negative axiom, and fresh Comparator controls recorded below. This expected skip is disclosed rather than treated as a pass.

## Artifact integrity and byte binding

The uploaded artifact is `lean-SP-06`, artifact ID `10320127872`, 14,504 bytes, unexpired. GitHub’s API digest and the independently downloaded ZIP agree:

`sha256:fac2ebe5f81ec421a7b478fcbd1a11768887b8678ad5d166adac3a1402aece6c`

The ZIP contains 13 ordinary log/result files. I extracted it with path traversal, absolute-path, symlink, special-file, and destination-escape checks; all 13 entries passed. `EXTRACTION-RECEIPT.json` records each entry and the ZIP hash. The raw ZIP is retained as `lean-SP-06-artifact.zip`.

The CI result records `repository_commit=3122d69460b0ed6dda3ea00dfaa899f93411ce2f`, `result=comparator-accepted`, and input SHA-256 values for the package. Recomputing every one of its 61 input hashes from `git show 3122d69460b0ed6dda3ea00dfaa899f93411ce2f:...` produced an exact match (`commit-input-hashes.json`, `all_match=true`). The candidate worktree was observed clean at this same commit; no source, Git ref, or dependency cache was changed by this audit.

## Linux and trust controls

The tool receipt in `result.json` identifies Ubuntu’s x86_64 Linux environment (platform `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39`), Lean `Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)`, Go `go version go1.27.1 linux/amd64`, LeanCert/Forsythe revision `8d1b0c0545a77b40245e84705aa7d273e6c81e62`, source-lock hash `b3833b07916e5db77579b9cc53ca582282f6a841f36d6a60d693e5b02d342b6b`, CI sandbox-probe hash `31057195baf238807cacbb4126c5b07f02cec55a4e4437de5f3a755b3fada803`, and hashes for Comparator, lean4export, and Landrun. The result permits only `propext`, `Classical.choice`, and `Quot.sound`.

The retained raw logs establish:

- the build/export sandbox probe passed build and export modes, denied outside-project writes and AF_UNIX, isolated user/PID/mount/network/IPC/UTS namespaces, reported no effective capabilities, set `no_new_privs`, and passed negative sandbox argument cases;
- all three actual default-kernel replay cases behaved as required: honest case accepted, invalid raw proof rejected, and quotient post-check mismatch rejected;
- all five Comparator regression cases passed;
- the `sorryAx` and native `native_decide` fixtures were rejected with exit status 1;
- the fresh strict Comparator run built the project, ran Lean’s default kernel, printed `Your solution is okay!`, and exited 0.

No warning in the logs is a failure of the submitted proof: the 20 `sorry` warnings are emitted while building the deliberately placeholder `Challenge.lean`; `Solution.lean` builds without that proof hole and is the environment checked by Comparator.

## Twenty Comparator identities

The result and `comparator.json` each list exactly 20 theorem exports, and the final export line in `comparator.log` contains every same name. Their order is retained in `result.json`; the corresponding count and equality checks are recorded in `controls-and-identity.json`. The permitted axiom closure is exactly the three standard axioms above, with no custom or native proof axiom reported.

## Proof/source review linkage

Two independent local final proof reviews are committed in the candidate. Their reviewed core bytes match the Linux input hashes for `Challenge.lean`, `Definitions.lean`, `Numeric.lean`, `Curve.lean`, `Proof.lean`, and `Solution.lean`; the hash-presence checks for both referee reports are in `controls-and-identity.json`. The source map pins the original canonical SP-06 source at `50838e37dd793830e2cecd1055cfc7e0349490f1`. Rechecking its four recorded source hashes yielded:

- canonical README: `e2eb891930c96d6a3bdd25c75bfe6bd2798cc8c540ce00ec851f7bf1f0ceb25c`;
- complete solution Markdown: `c7adb8f97238049b20e82044d8527b70301779ba041169f74fe603a88ea1ae7a`;
- problem TeX: `183127180596a36c108ed8575420e3845ca890f3048a32ec1252d61cf60d5311`;
- solution TeX: `b7340bf85e0b776ed49a4303af64820b72708eb249fbdc885b9179945e60ffc9`.

The two local reports remain local/macOS mathematical and proof reviews. The Linux result is the independent operational evidence; CI itself records `semantic_review=not-performed-by-this-command`.

## Retained evidence

`EVIDENCE-MANIFEST.json` is the complete hash/index record for this audit directory. `MANIFEST.sha256` binds all retained evidence files. `verify-job-key-lines.json` provides line-number navigation into the raw job log, while the full raw logs and result remain under `extracted/`. `COMMANDS.txt` records the read-only retrieval commands. No canonical status, solved marker, branch, or PR was changed by this audit.
