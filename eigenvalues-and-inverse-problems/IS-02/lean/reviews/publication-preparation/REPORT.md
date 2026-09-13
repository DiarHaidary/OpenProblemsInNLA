# IS-02 publication preparation and validation

Prepared in `/tmp/nla-lean-is02-worktree` at candidate HEAD
`522f091b9f0d39d4846f5939bcafc1549ba16a55`. No commit, push or pull request was
created. The changes are ready for the coordinator's independent publication
review and final Git operations. This report is a preparation/self-check
record, not an independent review of my own metadata edits.

The canonical IS-02 entry is promoted from Solved to Lean verified on the
strength of the actual successful Linux run 34766178560 / target job
103747466088, the root's independent operational audit and the earlier
independent mathematical/cleanup approvals. The unchanged complete proof
covers all nine advertised exports and the full original negative target.

## Preservation and attribution

Before editing publication metadata I checked every one of the 119 original
Linux input hashes against the clean candidate. I archived exact committed
copies of README.md, formalization.yaml and verification/package-inputs.json,
with an explicit candidate-metadata-map.json. These are the only original
in-project files changed. Every original mathematical definition, Challenge,
proof source, dependency pin and review report remains byte-identical.
The entire independent Linux operational audit was copied without changes,
including its original ZIP, API receipts, scripts, raw logs and manifest.

The original canonical mathematical target is byte-identical between its
Problem statement and References headings. The informal solution.md,
solution.tex and solution.pdf are byte-identical; their hashes are in
BASELINE.json and PUBLICATION-CHECKS.json. The permanent-ID registry and all
shared tools remain unchanged. The existing RESOLVED entry, canonical page
and formalization metadata retain Matthew J. Colbrook's mathematical credit
and list George Stepaniants's separate formalization authorship with the full
Department of Computing and Mathematical Sciences / Caltech affiliation.
No George email was added; retained API author/committer receipts have none.

## Checks completed

- Offline publication verification passes: all 119 original inputs map to the
  live unchanged source or three exact archived metadata copies; the current
  inventory covers 146 files plus the inventory itself. The copied original
  ZIP, all nine actual Linux statement/axiom reports, run/job receipts,
  default-kernel and rejection controls pass the retained offline checker.
- Manifest v0.4 validation and all nine Comparator declarations pass.
- Permanent-ID validation passes for all 217 IDs against origin/main.
- Catalog regeneration succeeds, and all 17 permanent-ID tests pass.
- git diff --check passes after removing trailing spaces on the two edited
  status/date metadata lines. This does not change their PDF interpretation.
- The canonical README, generated TeX and final two-page PDF were inspected.
  Existing Pandoc/XeLaTeX rendering initially produced a split problem
  statement and unnecessary third page. The private render_layout.py applies
  two layout-only changes to generated standalone TeX: a page break before
  Problem statement, and removal of the forced break before References.
  XeLaTeX passed twice without overfull or missing-character warnings.
  Both final page PNGs were visually inspected with no clipping, overlap or
  missing glyphs; the complete original mathematical statement stays together.

No local Lean or Lake process was launched. The actual proof verification is
identified by the retained Linux receipts, not inferred from metadata checks.
The small added package evidence is about336KiB; publication QA, including
small PNGs, remained below the requested10MiB scratch limit. PDF rendering
started only after the coordinator recovered disk space. The earlier failed
ENOSPC directory creation occurred before any publication mutation and did
not change any source.

## Coordinator handoff

PR-TITLE.txt and PR-BODY.md follow the repository's three-section template and
explicitly request merge into main. No related issue number was invented.
Ten tracked paths are modified: canonical README/TeX/PDF, Lean README/YAML/live
inventory, RESOLVED and the three generated indexes. Additional paths are
only the archived candidate metadata, immutable Linux evidence, metadata map
and offline verify_publication.py. No work outside this IS-02 worktree was
changed except the requested private publication-review output directory.

This branch's generated index reports27 Lean-verified entries: its published
base contained26 and this publication adds IS-02. That branch-local number
must not be mistaken for the whole campaign count or used to overwrite a
concurrently merged SP-06 promotion. If the coordinator merges a newer
upstream base before publishing, regenerate the indexes and rerun the
required ID checks on that merged state.

The stable proof link points to the verified candidate revision. New metadata
and evidence are separate, source-preserving publication additions; no claim
is made that the still-uncommitted publication tree is itself the old Linux
commit. The coordinator should run the ordinary final branch CI after its
publication commit. No PDF output is pending.

## Final artifacts

- canonical PDF: SHA-256 `c9b3fcda5b60d7d091b559dc853069c2fe217fb1d299c36c810f4d1ff61705d8`
- canonical TeX: SHA-256 `911a62b55f6c411e9cbbe802a54fd94af6a9f2ab16b89d9eb746157609632a40`
- canonical README: SHA-256 `613d20156a459e37d7be73b46ec7570d4b748eaac748343cb969367614291f5c`
- formalization.yaml: SHA-256 `7ec0f902a4ae9bb954d3e5918002d73a229bae465b5fa6df48e709c9fd59c4d9`
- current package inventory: SHA-256 `b97d2f447e08999826c72b37763c5596d39d3bf12e160ef1e21c30b2d28bf77e`
- offline publication checker: SHA-256 `3ca92829c1d07f0ae58db9c9adcfd5b44f883dcc7033adce6d7a17d6e914e535`

EVIDENCE-MANIFEST.json binds this private handoff record and QA files using
relative paths. Raw logs preserve actual historical execution paths.
