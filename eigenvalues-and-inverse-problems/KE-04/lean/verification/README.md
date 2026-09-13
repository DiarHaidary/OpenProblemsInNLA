# KE-04 statement development evidence

These are author-development records, not independent statement approvals.
No proof, Comparator run, raw-kernel export replay, or authoritative Linux gate
is recorded. Original and external source snapshots are evidence, not additional
project proof implementations.

## Eligibility and originals

`check_eligibility.py` performed read-only upstream-main and all-state public PR
title/body checks, then inspected the immutable local Git objects at the observed
base. The successful dated result is
`eligibility-attempt-kvdvfcpy/eligibility-query.json`; `eligibility.json` gives the
bounded interpretation. The first script and `eligibility-initial-failure.json`
retain a failed preflight. That initial wrapper had not saved its child output;
the record explicitly states that limitation instead of inventing a cause.

`capture_sources.py` captured 17 exact Git-bound source files. Every source file's
commit, repository path, Git blob, SHA-256, byte count and actual successful
`git show` command is in `original-source-inventory.json`. Both the original
Colbrook manuscript and the current complete Markdown and TeX were read, as were
the original/current canonical targets and original detailed informal review.
The coordinator note is copied only as context and explicitly not as approval.

## Fresh source elaboration

The actual invocation for all three attempts was:

```sh
python3 verification/statement-development/check_statements.py
```

Working directory:
`/tmp/nla-lean-formalization/next-ke04-statements-draft/lean`.
The runner resolves this to `/private/tmp/...` on the host. Each attempt contains
an exact immutable copy of its runner, Definitions, Challenge, configuration and
generated inspectors. Each input file has mode 0444. All Lean commands run from
that attempt's `source/` directory. The actual toolchain binary hash, version,
platform, environment search path, commands, exit codes, log hashes, source
bindings, source pin/status checks before and after, and removed object hashes
are recorded. The logs themselves are retained.

| Attempt | Actual result |
| --- | --- |
| `attempt-2n_e6pes` | All four Lean commands exited 0. The reporting script then exited 1 because it incorrectly expected a `Trust check passed` message from `#assert_trust`, which succeeds silently at the pinned release. Actual type and axiom logs remain available. Four private objects were hashed and removed. |
| `attempt-xrn2jug1` | Corrected reporting script exited 0 and the four exact Lean logs and immutable inputs remain. Its original final JSON was later overwritten by an integrity-runner output-path bug. That lost record is not accepted evidence; the misdirected report is preserved at the actual path and explained in `EVIDENCE-RECOVERY.md`. |
| `attempt-r5fn2nl_` | Fresh identical-source rerun after the evidence-handling fix. All four Lean commands and the reporting script exited 0. Its intact result records all 24 printed target signatures, 24 placeholder warnings, 27 explicit kernel trust commands, all transitive definition axiom reports and unchanged dependency pins/statuses. Four private objects were hashed and removed. |

The definition inspector imports `NLA.KE04.Definitions` and the actual pinned
`LeanCert.Tactic.Verification`, never Challenge. The type inspector imports
Challenge, so its success establishes only elaboration of deliberate placeholders.
None of these results proves a KE-04 theorem. The current Definitions, Challenge,
configuration and runner bytes equal the final `attempt-r5fn2nl_` immutable inputs.

Existing dependency caches were read only. Every attempt checks the ten source
pins and clean statuses before and after. Cli has no build directory and is not
used in `LEAN_PATH`; the other nine package build directories are used directly.
No package, cache, `.lake` tree, object or binary is copied into this project.
Only selected external source text is retained for inspection. No dependency
download, update, build, deletion or shared-cache mutation was performed.

## API and structural evidence, including failures

The actual capture invocation was
`python3 verification/capture_api_evidence.py` from the project directory.
The attempts are preserved separately:

1. `api-evidence/` contains the first 19 successful exact text snapshots, the
   executed original script, partial manifest and `failure.json`. This runner
   exited 1 after `git show` exited 128 in the Tau Ceti source directory, which is
   an existing pinned API archive rather than a Git checkout.
2. `api-evidence-final/` retains the second script, captured Tau Ceti provenance
   responses, and manifest with the actual assertion traceback. It exited 1
   because its Git-tree validator removed the leading dot from `.github` when
   determining parent directories. No source or mathematical assertion failed.
3. `api-evidence-complete/` contains the corrected executed script, 33 complete
   selected source texts, five actual search logs and command results, the source
   archive provenance and final successful manifest. The 33 working source files
   equal the pinned bytes. All selected Tau Ceti blob hashes and all directory
   tree hashes were independently reconstructed from the retained recursive tree,
   including the root tree named by the pinned commit response.

The unbuilt external sources are never imported from these snapshots. Library
imports resolve only through the stated read-only dependency directories. The
Schiffer/Forsythe material is structural evidence and is not proof code for this
project. `SourceCorrespondence.md` records the exact scoped uses and license terms.

`validate_draft.py` performs a final read-only integrity check of source bindings,
successful elaboration inputs and logs, declaration coverage, permitted axioms,
external selected sources and the absence of project proof files. Its own
validation evidence is retained separately. The initial validator's output-path
error is preserved in `EVIDENCE-RECOVERY.md`; it is not suppressed as a clean
integrity run. `DRAFT-INVENTORY.json` is the outer
review-input inventory and hashes every file, including this document, all source
snapshots, old failures and nested manifests; its only exclusion is itself.

Fresh independent statement reviews and coordinator acceptance are still
required. This evidence directory does not supply either approval or a freeze.
