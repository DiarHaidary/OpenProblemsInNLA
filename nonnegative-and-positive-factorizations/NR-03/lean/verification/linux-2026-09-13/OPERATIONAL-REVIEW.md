# NR-03 repaired canonical Linux verification: operational audit

**The actual complete canonical run passed.** Run **34785341662**, verify job
**103799711659**, checked commit
`f664d07e82aaa60bc9c78dd1946e763168c5c530` for
`nonnegative-and-positive-factorizations/NR-03/lean`.
Only NR-03 was selected. The job ran from **21:57:54 to 22:26:48 UTC** on
13 September 2026: **28 minutes 54 seconds**.

This report is by the proof implementation/operational collector. It is not
an independent mathematical referee report. Independent source and final
mathematical acceptance are separate records; this audit establishes what
the actual Linux checker executed and accepted.

## Source and tool identity

The raw successful receipt binds **all 113 package input hashes** to the
exact candidate Git commit. Each hash was independently recomputed from the
committed blob and agrees with the raw receipt. `GIT-SOURCE-BINDINGS.json`
retains those comparisons. The source includes the reviewed single-line
Rank.lean cast-goal repair; all other mathematical source/boundary preservation
is documented by the separate integration and referee records.

All **ten actual dependency checkout revisions** in `dependencies.log` match
the candidate's manifest, including LeanCert and Mathlib. The tool receipt
and checked source-lock identify Lean **4.33.1**, the pinned Forsythe verifier
source, and the checker executables. No local Lean/Lake, dependency cache,
new dispatch, retry, source edit, or resource change was performed by this
collector. The previous failed canonical evidence remains separate and
unchanged at `/tmp/nla-nr03-canonical-linux`.

## Actual complete proof and checks

The raw log records all **58 active project modules** built successfully,
including all **48 row modules**, the complete family identities, the
unconditional certificate, Rank, and Solution. Rank compiled in **2.1 seconds**;
Solution compiled in **2.2 seconds**. Lake reported 3066 completed build jobs.

All **403 observed theorem axiom diagnostics** use exactly `propext`,
`Classical.choice`, and `Quot.sound`. These include the **384 row lemmas** and
all **ten public theorem exports**. The complete Solution has all ten pinned
LeanCert kernel-trust assertions, and its successful build includes their
execution. Comparator exported all ten configured declarations and reported:

```text
Lean default kernel accepts the solution
Your solution is okay!
EXIT_STATUS=0
```

The raw configuration is identical to the committed `comparator.json`: all
ten targets are present and the permitted-axiom list is exactly the standard
three. The accepted run retains no additional public hypothesis or partial
row selection through a changed configuration.

The same verify job passed the actual unprivileged sandbox checks, all three
built-in-kernel regression cases, all five Comparator regressions, and both
expected rejection fixtures for `sorryAx` and the generated native-evaluator
axiom. Their expected exit-one outcomes are control successes. The separate
infrastructure-only checker matrix job was skipped for this problem-only
change; all required per-project controls nevertheless executed in this job.

There were no compiler errors. The log retains ten intentional Challenge
placeholder warnings and five harmless unused-simp-argument warnings in the
solution graph. Those warnings are preserved in `BUILD-DETAILS.json`; no
mathematical source was changed merely to remove them.

## Retained evidence and offline check

Artifact **10326896988** is **21,628 bytes**, ZIP SHA-256:
`91f80abcbbb0f10fbf614ab259fbf5121a8dabd5c600969a260e3b8b2c8e267c`.
The full raw directory is
`extracted/verify-20260913T215907Z-4140/`.

- Raw `result.json`: `e7bd039fb9e4dcc7f46a4930b9f4dc2eb79a9977a80c0cbb4299d8edcb4eb0ed`.
- Raw `comparator.log`: `aa87f0c27e89f687804f1e655f700946aa31d1a28b40e6e71ed4b92486170ca1`.
- `OPERATIONAL-CHECKS.json`: `d41e0ddfa9ef850c515958779be795bf3639245e1423af79f0a709939e6c60db`.

`python3 -B check_evidence.py` performs a portable offline integrity check of
the retained archive, exact run/job, input-binding receipt, actual exports,
axioms, dependency checkout records, and all controls. It starts no compiler
or workflow and makes no independent semantic-review claim. Its actual
successful output and command receipt are retained alongside this report.
The collector's separate `audit_terminal.py` also independently reads the
exact candidate Git blobs when that Git repository is available.

This operational result is complete for the checked candidate. Repository
status, publication metadata, campaign counting, and final independent
mathematical acceptance remain the coordinator's separate responsibilities.
