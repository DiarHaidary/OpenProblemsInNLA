# IE-05 candidate package author handoff

This is a packaging-author handoff for an independent concrete package audit.
The accepted mathematical proof is complete; actual Ubuntu default-kernel and
Comparator verification with real negative controls is pending. No candidate
commit, push, PR, canonical-page change, or Lean-verified status is claimed.

Author: George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA, with substantial
ChatGPT/Codex assistance. The original counterexample and integer data remain
attributed to George Stepaniants; the conjecture and cited growth analysis remain
attributed to John Peca-Medlin.

The package author is OpenAI Codex agent `/root/ie05_final_math_referee1`.
Its earlier independent mathematical review was sealed before this separate
packaging assignment. That report and every file in its scope are unchanged.
The later authoring role provides no independent packaging or publication
approval. The second final mathematical review is likewise unchanged.

The required coordinator gate was present before copying:
`verification/final-review-acceptance.json`, SHA-256
`6e1de72e81a0603066544133f7bb52a7217b31bd6f05372a8c1abe109ff03d61`.
Its accompanying complete root evidence seal is retained, including the first
filename-classification diagnostic and the successful acceptance attempt.

All 2,338 regular files in the accepted original draft were copied, without an
ignore function, dependency caches, or Git objects. Exact previous versions of
only `README.md`, `SourceCorrespondence.md`, and `lakefile.toml` are preserved
under `archive/pre-package/`, with explicit original path, old SHA-256, byte
length, and archive destination in `ARCHIVE-MAP.json`. All other old files remain
at their original project-relative paths with identical bytes. The new Lake
default target is `Solution`; its only configuration edit replaces the old
`Challenge` default. The live documentation and v0.4 `formalization.yaml` state
the completed mathematical scope and pending runtime gates.

The 12 final `NLA/IE05/*.lean` modules, `Challenge.lean`, `Solution.lean`,
`comparator.json`, toolchain, and all ten package pins are unchanged. Final
`Proof.lean` SHA-256 is
`f8ef9d1901845439e7c09f4e9d004eb49d87ed28d8a6d567d48ac4d16199a950`;
`Solution.lean` SHA-256 is
`3e12274c074f9d221230bd3939a76d433532b067c7123a12effe2b9e6f6a5c9a`.
`LIVE-SOURCE-SELECTION.json` binds the exact live source/control selection.

The readonly `verify_inventory.py` checks the complete original 2,338-file
snapshot, every member of all 29 historical files inventories (14,280 historical
member checks), and the original 27 content Git blob identities. Three exact
wrapper path-and-old-hash mappings preserve the old versions without basename
exemptions. Seven small pinned primary-library source files make the old
external API-source inventory portable; these are source archives, not cached
objects or new IE-05 imports. Original commit/path provenance is retained in
the accepted source and review receipts, not reconstructed from a new Git store
inside this package.

The new complete project-relative selection is `../candidate-inputs.json`.
It excludes only its exact own path. The default verifier checks its exact
current whole-tree membership. Its explicit `--candidate-members-only` mode
is available for checking that fixed selection after separately recorded
later-phase additions; it neither alters an old scope nor ignores manifests.
The `--preseal` mode is an authoring check and does not verify a final outer.

`audit_metadata.py` validates the actual pinned v0.4 schema and current NLA
coverage rules, all 17 result files and export names, complete original
mathematical bytes, all pins, the Solution entry point/default, the isolated
17 Challenge placeholders, 89 literal final-source kernel assertions, credits,
and pending runtime status. This is a source-preservation and metadata check;
the accepted earlier actual Lean type/body and axiom inspections supply the
mathematical evidence. No unchanged mathematical module was recompiled while
packaging.

The preseal packaging audit attempts are under `author-checks/`. Attempt 001 passed
historical preservation but its metadata command failed because the existing
Python 3.10 environment lacks `tomllib`. The corrected audit checks the exact
preserved Lake text and its one permitted replacement. Attempt 002 then exposed
the author's reversed argument order in a lexical `#assert_trust` counter.
The corrected counter matches the actual `#assert_trust kernel declaration`
syntax. Attempt 003 passed the full metadata audit. Attempt 004 separately ran
the current repository's actual `tools/lean/validate_manifest.py` and passed
all 17 declarations. These were tooling diagnostics, not Lean compilation
failures. Their executed script snapshots, commands, raw logs, and results are
retained. Earlier interactive preparation diagnostics are summarized in
`authoring-diagnostics.json`.

The one-shot outer-sealing receipt and read-only checks of the completed seal
are recorded in the separate external package-author handoff. Their outputs
cannot be inserted into the already sealed candidate without creating another
phase; the independent auditor will bind its own checks separately.

The package integrity command is standard-library Python; the metadata command
also needs the PyYAML and jsonschema dependencies recorded in
`schema/requirements.txt`. Both checks are read-only. The independent auditor
should inspect the current documents, full archive mapping, exact source bytes,
all historical memberships, metadata, and final complete candidate selection.
Actual Linux/default-kernel/Comparator, independent operational acceptance, and
reviewed canonical publication remain later gates. The canonical ID, original
target, and existing **Solved** status remain unchanged.
