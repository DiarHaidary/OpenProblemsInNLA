# RA-20 concrete publication handoff - 13 September 2026

**Prepared for independent publication review.** The coordinator accepted the
complete-target mathematical reviews and actual Linux verification before this
publication was authored. This handoff adds no independent approval of its own
publication. No publication commit, push, pull request or upstream acceptance
is asserted here.

Publication author: `/root/ra20_final_referee1`, previously independent final
mathematical referee 1 and then candidate-document author. George Stepaniants's
formalization credit and full Department of Computing and Mathematical Sciences,
California Institute of Technology affiliation are published without his email.
Original negative-resolution credit remains with the Codex automated maintainer
audit; original conjecture credit remains with Kubjas, Sodomaco and Tsigaridas.

## Accepted immutable proof and actual runtime

The proof revision is `43603b173beb294c2588d83f936a8a96246fd5f0`, verified by
[actual Ubuntu run 34743832047](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34743832047),
attempt 1. All 17 jobs passed. The actual default kernel and Comparator checked
the twelve exact exports with no definition holes. There are 61 source LeanCert
kernel assertions and 57 printed standard-three axiom occurrences covering 45
distinct names. The matching official Mathlib cache supplied 8,690 dependency
files; a from-source rebuild of all Mathlib is not claimed.

The [accepted root gate](../root-linux-acceptance-2026-09-13/ROOT-ACCEPTANCE.json)
has SHA-256 `a2c3a74eb858edb859d34d8bd2985dc54710e31816412d285c32a547e080e57e`.
Its complete 1,604-entry seal has SHA-256
`40d68224c966fc5114995418bf47ee2fc38f3ebbacc50536cae3b1c9d98ca0b8`.
The independent operational report has SHA-256
`7f7532bbc01533d0c35fe0ac3aece0ff66cb43c1444e41275db0784cee6b8ae7`,
and its complete 1,589-entry seal has SHA-256
`89b3cd2aa8c47835be4531cca85561a70aee7f20be6e9f3bcdaaa48d23812dcd`.

Before authoring, I rehashed both complete inventories and ran the original
read-only independent operational verifier successfully, including its runtime
and privacy recheck. That command, original stdout/stderr and result are
retained here. The [preauthoring baseline](PREFLIGHT.json) has SHA-256
`ca08a0e2f2525dd009ee41e7fe99fd0e8d55d54f26884508334c3702bf555b16`;
it records all 1,580 prior project files and 17 possible canonical/index inputs.
The original source base remains `5830ed4fb06da0659414a3deb2a40ad327aca052`.

## Concrete changes and mathematical fidelity

The nine changed existing paths, relative to the repository root, are:

- `README.md`
- `CATALOG.md`
- `RESOLVED.md`
- `randomized-and-low-rank-approximation/README.md`
- `randomized-and-low-rank-approximation/RA-20/README.md`
- `randomized-and-low-rank-approximation/RA-20/problem.tex`
- `randomized-and-low-rank-approximation/RA-20/problem.pdf`
- `randomized-and-low-rank-approximation/RA-20/lean/README.md`
- `randomized-and-low-rank-approximation/RA-20/lean/formalization.yaml`

The canonical page now directly records Lean verified status, all twelve exact
export names, original-target correspondence, immutable proof link, exact
Lean/Mathlib/LeanCert pins, explicit non-root Linux reproduction commands,
accepted actual logs and the standard-three transitive axiom boundary, as
required by CONTRIBUTING. RESOLVED links that evidence and gives George's name
and department. Generated indexes change only the RA-20 status and aggregate
Solved/Lean-verified counts. All 217 permanent IDs and paths remain unchanged.

The complete text starting at the canonical `## Statement` heading remains
byte-for-byte unchanged. The original full four-formula conjecture is negated
by its allowed case `n=s=3`, with genuine generic count three instead of four.
No separate verdict on the other formulas, or separate scheme-theoretic
multiplicity theorem, is added. The whole vanishing ideal, actual reduced ring,
algebraic smooth locus, entire-ideal tangent, complex bilinear differential and
genuine generic cardinality scope remain explicit. The misleading source
comment about a complete local ring is explained as ordinary
`Localization.AtPrime`, without adic completion. No Lean proof, frozen
statement, dependency pin, proof map or prior evidence/review file was edited.

## Exact archive mappings and complete prior evidence

Both checked candidate wrappers were archived before mutation:

- [Candidate README](archive/candidate-README.md):
  `83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc`.
- [Candidate metadata](archive/candidate-formalization.yaml):
  `bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197`.

[ARCHIVES.json](ARCHIVES.json) records exact copies of those two files and all
17 prepublication canonical/index inputs. A historical expectation may map to
an archive **only when both the original full repository path and its expected
SHA-256 match that explicit entry**. The earlier exact project-README mapping
for SHA-256 `7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50`
still maps solely to `verification/pre-candidate-README.md`. There is no
basename exception, blanket README exemption, hash rewriting or ignored mismatch.

The new verifier preserves all 521 proof inputs, 68 statement inputs, 16
original source/snapshot/Git identities, all 1,092 tested candidate inputs,
both complete final-review inventories, and every accepted later inventory.
There are 19 prior accepted manifest/package inventories. The twentieth
retained manifest is the root's explicitly rejected
`initial-scope-diagnostic/EVIDENCE-MANIFEST.json`: its exact bytes and entire
diagnostic remain bound, but it is not promoted into an accepted inventory.
The accepted root seal includes and preserves that diagnostic.

Historical candidate scripts expecting live candidate wrapper bytes are dated
records. Use this publication's exact-mapping verifier after publication rather
than editing earlier seals or claiming that an unadapted historical verifier
accepts changed wrapper paths. The archived original source and tested proof
remain independently identifiable by both SHA-256 and their actual Git blobs.

## Actual publication validation and PDF inspection

The retained [check receipts](CHECKS.json) show schema validation for twelve
exports, both permanent-ID bases, all 17 registry tests, whole-catalog math
format checks, and the required `--base-ref origin/main` validation before
index generation. The repository's unmodified Pandoc/XeLaTeX renderer built
the canonical TeX and three-page PDF. Transparent wrappers retained the actual
Pandoc input/metadata/template, source TeX, both XeLaTeX command streams and
full logs. The required PDF operation-start marker succeeded exactly once
before publication authoring. No new Lean build or network/dependency retrieval
was performed during publication preparation.

[VISUAL-QA.json](VISUAL-QA.json) binds the final PDF and all three rendered
pages. I inspected every page: no clipping, overlaps, missing glyphs or
overfull boxes were observed; page 2 keeps the complete original quantified
statement and all four formulas together. The extracted text, original
prepublication PDF, final PDF and source/renderer receipts are retained.

An author review found one stale candidate-phase sentence in the initial
publication YAML and clarified the role chronology. Both initial wrapper
drafts and the correction script are retained under `initial-text/`; the
correction did not affect the canonical PDF. Read-only final validation checks
the final schema, relative links, immutable source links, changed-path scope,
exact original target, PDF content, whitespace and absence of personal email.
It does not claim an independent publication approval or live HTTP probe of
every external website.

## Read-only verification and next action

From this evidence directory:

```
PYTHONDONTWRITEBYTECODE=1 python3 verify_inventory.py
```

The [complete manifest](EVIDENCE-MANIFEST.json) binds all publication outputs,
the full prior project and accepted root scope, every nested manifest and all
new publication evidence. Only that exact outer manifest excludes itself.
The preseal validation result is included; the final sealed verification is
then run without writing any file inside the sealed evidence directory.
Later independent reviewer additions outside this directory are separate
evidence, not falsely included in the author's seal. Do not rerun mutating
historical preparation/check scripts into a sealed evidence directory.

The independent publication referee and coordinator must review these concrete
bytes before any Git commit, push or new pull request to upstream `main`.
All original accepted proof and Linux evidence remains unchanged.
