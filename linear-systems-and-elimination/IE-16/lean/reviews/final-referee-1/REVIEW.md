# IE-16 final canonical-source referee addendum

**Reviewer:** `/root/lean_iv01_next` (OpenAI Codex AI agent)

**Date:** 13 September 2026 (America/New_York)

**Role and independence:** This is an independent final mathematical and
mechanical addendum. I did not implement IE-16, did not modify its proof
sources or publication worktree, did not run Lean/Lake locally, and did not
use another final referee's verdict. I directly inspected the immutable
canonical Git blobs and the retained raw Linux evidence. This is an AI review,
not external human peer review or an official Tau Ceti review.

## Exact object reviewed

The reviewed project is
`linear-systems-and-elimination/IE-16/lean` at commit
`697a2a1d88337a6747aa5c82fb6e554d3ff1b356` in
`sgstepaniants/OpenProblemsInNLA`. The parent of this canonical packaging
snapshot is the fifth compiled source snapshot
`281fc3790412b7ab2b05c202c0351b4d259a6382`.

The raw evidence is the retained artifact directory
`/tmp/nla-ie16-canonical-ci-34774629327/extracted/verify-20260913T182805Z-4150`.
It records run `34774629327`, verification job `103770408910`, and artifact
`10322764134` (`lean-IE-16`). The downloaded artifact is 22,598 bytes with
SHA-256
`1e1662ad25d3ea724277a840f9c4579c034cae08c9f6fce76bc08cd48795eefd`.
The exact raw receipts and log hashes are recorded in `CHECKS.json`.

## Source and target fidelity

I approve the original IE-16 target. `Definitions.lean` retains the complete
quantifiers over every `n >= 3`, every finite set of `n` distinct nonzero
complex points, and every `1 <= k <= n - 2`; `M` is the infimum over arbitrary
complex polynomials of degree at most `k` with `p(0)=1`, and `subsetMax` is the
maximum over all powerset subsets of cardinality `k+1`. The source snapshot
also binds the canonical README, problem TeX, Holden's solution, submission
README, exact verifier, and all 126-subset certificate to the upstream
revision `b73cd1804e40e0d101294eedb156984f0d62b4a6`; all six recorded hashes
match the corresponding current Git blobs.

The current formalization metadata lists George Stepaniants with the Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA; no email address is present.

The fifteen Challenge types are preserved exactly and the current
`Solution.lean` exposes all fifteen names. The proof supplies the explicit
nine-point finite witness with `n=9`, `k=4`, the exact full minimum and its
attainment, the all-five-point-subset upper bound and attainment, positivity
of the actual subset maximum, and the strict ratio bound. The final
`not_IE16Conjecture` declaration is therefore the unconditional negation of
the original universal assertion, rather than a fixed-polynomial,
single-subset, numerical-approximation, or weakened-domain claim.

The proof-bearing source transition from the fifth compiled snapshot to this
canonical path was checked independently. `Definitions.lean`, `Challenge.lean`,
`Numeric.lean`, `NUMERICAL_TARGETS.md`, `comparator.json`, and
`lean-toolchain` are byte-identical. Every other proof module and `Solution.lean`
has the same non-comment, non-whitespace body after the documented packaging
move; the changes are leading comments and author/status wording. The only
configuration change affecting execution is the required Lake default target,
from `Challenge` to `Solution`. This proves that the final CI result is for the
same mathematical proof bodies reviewed in the fifth snapshot.

## Independent raw CI audit

The raw API receipt binds the successful run and job to the exact reviewed
commit. The job's relevant steps all completed successfully: manifest
validation, pinned Lean setup, the Lean build, unprivileged Linux isolation,
fresh sandboxed statement/axiom/kernel verification, and log retention.
The recorded input inventory contains 281 files; I recomputed every SHA-256
from both the commit's Git blobs and the worktree, with all 281 matching. The
pinned `tools/lean/source-lock.json` also matches the receipt's source-lock
SHA-256.

The raw `comparator.log` records successful Challenge and Solution builds,
export of the configured fifteen declarations, `Lean default kernel accepts
the solution`, `Your solution is okay!`, and exit status 0. The raw
`comparator-controls.log` records all five regression controls passing. The
raw `kernel-controls.log` records all three actual default-kernel replay cases
behaving as required, including rejection of an invalid raw proof and a
quotient post-check mismatch. The raw `negative-sorry.log` rejects `sorryAx`,
and `negative-native.log` rejects the native-decision axiom.

The raw `sandbox.log` records successful build and export probes with writes
outside the permitted build area denied, private user/PID/mount/network/IPC/
UTS namespaces, no host parent visibility, denied host signaling and loopback,
denied AF_UNIX sockets, no effective capabilities, and `no_new_privs`; all
four malformed-option negative controls are also rejected. These are actual
log checks, not an inference from a green workflow badge.

The fifteen measured public axiom sets in the raw Solution output are all
exactly `{propext, Classical.choice, Quot.sound}`. The current Solution source
contains fifteen matching `#assert_trust kernel` commands. Its active proof
modules contain no `sorry`, `admit`, custom `axiom`, or `native_decide`; the
fifteen `sorry`s remain confined to the deliberate Challenge placeholders.

## Verdict and remaining publication condition

**PASS for the full original IE-16 target and PASS for this exact canonical
Lean proof candidate.** The exact finite counterexample is kernel-accepted by
the recorded Linux Comparator/default-kernel run, and the source transition
does not alter the reviewed mathematics. This addendum is ready to be
retained as one independent final compiled-source review.

The candidate's current README and `formalization.yaml` intentionally still
say that final acceptance is pending. They should be updated only after the
second independent final proof-source addendum and the repository's normal
publication review bind both reports and this run's raw evidence. No claim
of external human peer review or author endorsement is made here.
