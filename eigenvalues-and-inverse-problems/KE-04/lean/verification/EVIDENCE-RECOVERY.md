# Retained integrity-runner write-path error

Before any statement freeze or independent review, the first author integrity
validator used the local name `attempt` both for its new validation output
directory and for a later loop over elaboration attempts. It read the original
successful `attempt-xrn2jug1/result.json`, passed its checks, then wrote the
integrity report to that same path because the loop variable had replaced the
intended output path. The tool printed exit 0 and 126 checks but the wrong output
directory. This was caught immediately on reading the actual output.

The overwritten original final JSON is no longer available. Its exact object
hash records and dependency postflight records must not be inferred from the
remaining prose or treated as retained. The original immutable source snapshots,
all four exact Lean logs, `preflight.json` and `progress.json` are unchanged and
remain in `statement-development/attempt-xrn2jug1`. The misplaced integrity report
is retained at its actual write path, with phase `author statement integrity only`;
it must not be read as an elaboration result. The original executed validator
source is retained in `validation-attempt-v4kpdcg6/validate_draft.py`, whose intended
result file was not written. The misdirected report at
`statement-development/attempt-xrn2jug1/result.json` has SHA-256
`c372f3b71cfd02027286a0d6f2da14d5d2c2ed6dda0013941734dde44301b3e0`.

The validator has been corrected to use a separate `validation_dir` name. Fresh
identical-source attempt `statement-development/attempt-r5fn2nl_` exited zero and
provides intact commands, source/dependency bindings and removed-object hashes.
The final handoff names only that fresh complete attempt as the accepted
author-development evidence. This incident changed no mathematical definition,
Challenge signature, canonical source, dependency, proof file or independent
review. It is an evidence-handling failure, not a Lean or theorem result.
