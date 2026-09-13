# KE-04 independent operational audit — initial status

Audit date: 2026-09-13.  This is a read-only audit of
`/tmp/nla-lean-ke04-worktree`, branch
`codex/lean-ke04-block-lanczos-v2`, at candidate commit
`5ece67703520210bb9bf1cbf1d220cc8be8846e0`.

## Evidence inspected

- `docs/lean/REVIEW.md` and `tools/lean/HARNESS.md` were read.  They require
  statements-first review, separate mathematical and operational review,
  actual non-root Linux execution, Comparator statement identity, the default
  kernel and negative controls, and raw receipts/artifacts.  A green status
  alone is not evidence.
- The corrected proof freeze is sealed by
  `394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4` and
  records 3,503 frozen files and 17 distinct original Git source snapshots.
- Final mathematical referee report hashes are
  `73dda444d9b3798291e879b25aea5cbe49926f6807911aa1fba55f9d72153f4a` and
  `e195faa02cacf4168d5f4f39c4fed403e67a0eccf04b632ee1fc74e0ef72054f`.
  Their evidence rechecked the corrected freeze and 24 exports, but expressly
  did not claim authoritative Linux, Comparator, sandbox, or operational
  approval.
- `NLA/KE04/Proof.lean` contains 24 `#assert_trust` exports and imports the
  completed proof; `Solution.lean` is the 22-byte `import NLA.KE04.Proof`.
  The admitted `Challenge.lean` has intentional contract placeholders and is
  not imported by Solution.  The reviewed proof modules contain no `sorry`.

## Packaging state observed

The parent agent is editing packaging in place, so this is not an acceptance
report.  At inspection time the worktree had modified `README.md`,
`formalization.yaml`, and `lakefile.toml`, plus untracked
`verification/packaging/`.

- The Lakefile change now makes `Solution` the default target and updates its
  stale comment.  The current packaging verifier must be run after the parent
  commits these changes.
- The README now has a current-phase preamble, but its preserved historical
  section still contains phrases such as “No proof is implemented” and “no
  proof module exists”.  Those statements are acceptable only if visibly and
  unambiguously historical; the final rendered page must not leave them
  looking like the current status.
- `formalization.yaml` still truthfully marks `whole_problem_verified: false`,
  `actual_linux_comparator: pending`, and independent packaging review as
  pending.  These must remain pending until raw Linux evidence is inspected.
  Its last two `main_results.file` entries currently point to `Proof.lean`,
  although their defining declarations are in `Completion.lean`; this needs
  either a deliberate re-export convention documented by the project or a
  metadata correction before final approval.
- `verification/packaging/verify.py` seals the old README and Lakefile through
  archived copies and checks the two referee manifests, but it does not check
  the current README bytes.  The final operational review should ensure the
  current README has no accidental or contradictory packaging claims.
- The current YAML source/toolchain metadata and the proof freeze use
  different historical source commits in places (`50838e3...` versus the
  frozen mathematical base `5830ed4...`).  This can be correct only if every
  source record explicitly binds the intended historical snapshot; the final
  audit must verify those records rather than infer consistency from the YAML.

## Gates still open

No Linux CI run, raw comparator log, result JSON, default-kernel replay,
negative `sorryAx`/native control, real sandbox/control receipt, or sealed
artifact was available to this initial audit.  Therefore KE-04 is not yet
operationally accepted or countable as Lean-verified.  The next audit should
start from the exact parent commit and verify clean-source identity, all 24
declarations, permitted axioms (`propext`, `Classical.choice`, `Quot.sound`),
source correspondence, Linux/non-root/sandbox controls, and the raw artifact
hashes.  No candidate files were modified and no build or dependency download
was performed by this audit.
