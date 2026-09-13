# IS-02 statement-boundary typecheck

This is a statement-stage check. It does not verify any theorem body: all
nine bodies in `Challenge.lean` are deliberate placeholders, and
`Challenge.lean` is not a proof dependency. The check only establishes that
the definitions and the exact independent theorem signatures elaborate under
the pinned Lean toolchain.

## Command and environment

The command was run on 13 September 2026 from the candidate project, using
pre-existing dependency objects from the MI-22 Lean project as a read-only
source. No Lake command was run, and no dependency cache was copied or
modified:

```sh
IS02_DEP_ROOT=/private/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages \
  verification/statement-typecheck.sh
```

The script created the fresh private output prefix
`/var/folders/pw/wkdn0vxs0b54swhpwjg6s0x00000gn/T/nla-is02-statement-typecheck.l7ar1Y`
and invoked Lean directly with `-R` and explicit `-o` paths. The pinned
version reported was:

```text
Lean (version 4.33.1, arm64-apple-darwin24.6.0,
commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
```

Both direct invocations exited zero and produced only the expected nine
`declaration uses sorry` warnings from `Challenge.lean`. The output files were
`out/NLA/IS02/Definitions.olean` (67 KiB) and `out/Challenge.olean` (36 KiB).

This local macOS result is not an authoritative Linux harness, Comparator
result, LeanCert proof audit, or independent statement approval. Those gates
remain pending until the statement boundary is reviewed and a proof is written.
