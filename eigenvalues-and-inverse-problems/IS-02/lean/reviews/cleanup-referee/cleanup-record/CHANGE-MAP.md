# IS-02 presentation cleanup change map

Cleanup identifier: `IS02-presentation-cleanup-2026-09-13`.

The pre-cleanup Proof/Solution bytes and complete prior local final-review
records are preserved under `/tmp/nla-is02-before-cleanup/`. Its
`BEFORE-CLEANUP-MANIFEST.json` binds the old hashes, including Proof
`f108eb9d...`, Solution `8cf1db57...`, and the old proof-check script
`e8a6f6f7...`.

## Mathematical source changes

No mathematical statement, definition, Challenge contract, public export name,
public export type, proof strategy, or conclusion changed.

`NLA/IS02/Proof.lean` only renames private production helpers and adds section
comments. The exact identifier map is in `identifier-mapping.json`. The map
covers all former `test_*` helpers, including the six pair-support lemmas, four
single-support lemmas, four triple-support lemmas, the spectral bridge, and the
final assembly helpers. `Solution.lean` keeps all nine public declarations
exactly named and typed; only their references to the renamed private helpers
change. The duplicate `open Polynomial` commands were reduced to one, and the
initial stray space before the first public theorem in `Solution.lean` was
removed.

The comments explain the exhaustive support sizes 0, 1, 2, 3 and 4, identify
the six unordered pair positions `01`, `02`, `03`, `12`, `13`, `23`, and point
to the four triple cases and four single cases. They contain no proof input.

## Operational/documentation changes

- `formalization.yaml` now states that `norm_num`, `ring` and `linarith`
  discharge exact identities while LeanCert audits kernel trust. Its proof-stage
  note records the ten-pin clean dependency check and fresh-prefix evidence.
- `README.md` documents the same tactic/trust distinction and the required
  `IS02_DEP_ROOT` variable.
- `verification/proof-typecheck.md` documents the required environment variable,
  active checking of all ten manifest revisions and clean tracked trees, and the
  retained raw evidence files.
- `verification/proof-typecheck.sh` now checks all ten manifest package pins and
  clean worktrees before setting `LEAN_PATH`; it retains per-command logs,
  `command-results.ndjson`, `dependency-check.json`, and source hashes in every
  fresh prefix. The final script hash is in `FINAL-HASHES.json`.

## Narrow recheck instructions

Referee 1 should recheck that `Definitions.lean` and `Challenge.lean` retain the
frozen hashes, that the public theorem declarations in `Solution.lean` retain
their old names/types, and that the private renames are a bijective textual
identifier change. Referee 2 should recheck the updated YAML/README/script
presentation and the fresh evidence: all ten dependency records are pinned and
clean, all six compile commands exit zero, and the nine public exports report
only `propext`, `Classical.choice`, and `Quot.sound`.

The fresh run used:

```sh
IS02_DEP_ROOT=/tmp/nla-lean-mi22-worktree/matrix-inequalities-and-norms/MI-22/lean/.lake/packages \
  verification/proof-typecheck.sh
```

It exited zero at private prefix
`/var/folders/pw/wkdn0vxs0b54swhpwjg6s0x00000gn/T/nla-is02-proof-typecheck.an46Oh`.
Compact copies of its raw command records, dependency report, source hashes and
module logs are in `fresh-proof-typecheck/`; private `.olean` files are omitted
from this report but remain in the printed fresh prefix.
