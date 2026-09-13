# Local proof-stage check

The completed `Proof.lean` and `Solution.lean` are re-elaborated directly by
Lean 4.33.1 with one fresh private output prefix. The check reads an existing
pinned package tree and never runs Lake, downloads dependencies, rebuilds
shared dependency objects, or writes candidate objects. Run it as:

```sh
IS02_DEP_ROOT=/path/to/existing/.lake/packages \
  verification/proof-typecheck.sh
```

`IS02_DEP_ROOT` is required and must contain the ten package directories named
in `lake-manifest.json`. Before constructing `LEAN_PATH`, the script actively
checks every package's manifest revision and requires its tracked worktree to
be clean. The fresh prefix printed by the script retains `dependency-check.json`,
`command-results.ndjson`, one raw log per command, `source-hashes.sha256`, and
the private `.olean` output. These records preserve the exact commands,
results, dependency revisions, and source hashes for later review.

The command elaborates `Definitions.lean`, `NLA/IS02/Proof.lean` and
`Solution.lean`, then runs all nine public `#assert_trust kernel` checks and
prints their transitive axiom sets. Every public theorem must report exactly
`propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`, custom axiom,
`native_decide`, or native-evaluation axiom is accepted.

This is a local direct-elaboration and LeanCert kernel-trust result. It is not
the authoritative Linux Comparator run; final independent proof review and
catalog promotion remain separate gates.
