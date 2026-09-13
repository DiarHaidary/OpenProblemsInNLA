# RA-20 independent candidate packaging review — 13 September 2026

**Verdict: APPROVE the fixed candidate documentation and preserved evidence
for the subsequent committed-candidate Linux verification stage.** This is a
metadata, reproduction and evidence-preservation review. It adds no mathematical
approval and records no Linux execution, operational acceptance or publication.
The canonical problem remains **Solved**.

Reviewer: OpenAI Codex agent `/root/ra20_final_referee2`. I previously completed
the separately sealed independent final mathematical review 2. I did not author
the candidate README or YAML. Their author, `/root/ra20_final_referee1`, released
an explicit fixed-byte handoff before I inspected them. Its later document-author
role supplies no packaging approval. I read the other final mathematical report
for this packaging review only after my own mathematical report had been sealed
and accepted. The coordinating agent contributed mathematical source and is not
counted as an additional independent final referee.

## Concrete reviewed boundary

Paths in this table are relative to the RA-20 `lean/` project.

| Artifact | SHA-256 |
| --- | --- |
| `README.md` | `83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc` |
| `formalization.yaml` | `bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197` |
| `verification/linux-candidate-2026-09-13/HANDOFF.md` | `b2277179cad1d686c684abe6f676fe9680e5510d26935f7c7a72205ba79db4ae` |
| Installer `EVIDENCE-MANIFEST.json` | `60f056cd293d2b093786a34e55b670975dd6b27e7e927acdbf8513438c28b381` |
| `verification/final-review-acceptance.json` | `a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb` |

The complete candidate documents, actual repository review policy, contributing
instructions, pinned v0.4 schema and its validator, canonical mathematical
statement, original resolution and retained reconstruction were available for
this audit. I read the complete new README/YAML/handoff and the relevant actual
harness commands and validation/snapshot/control/verification implementation.
The source files, policy identities and original Git blobs were checked against
base `5830ed4fb06da0659414a3deb2a40ad327aca052`. The publication check did not
perform a new live HTTP probe or an affiliation lookup; it verifies the already
authorized name and full affiliation against the concrete submitted metadata.

## Evidence preservation

I independently rehashed all **958 preinstallation project files**. Exactly one
prior path changed: the current project `README.md`. Its original bytes remain
at `verification/pre-candidate-README.md`, SHA-256
`7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50`.
The only historical mapping applies when both the resolved original path is
this exact project's `README.md` and the expected hash is that exact old hash.
All other **957** prior paths retain their original bytes. There is no basename
renaming or blanket exclusion of README files or nested manifests.

All **1,010 installer-bound files** passed: **992 project files** (including
all **32** installer evidence files except its outer manifest) and **18 live
original/check-tool files**. The outer manifest itself is an additional fixed
input to this review. I checked complete membership of that installation and
found no unaccounted project file before adding my own review artifacts.

The independent checks covered every entry of the **521-file proof freeze**,
the **68-file statement freeze**, and all **16** original source/policy inputs
in their live, archived and original Git-blob forms. I also rehashed every
entry of all **14 historical inventories**, including the entire **699-file**
and **793-file** final-referee inventories, the statement package, statement
referee evidence and every development inventory. All nested manifest bytes
themselves remain bound. The full accepted gate, both report hashes, all 26
recorded successful final-referee source commands, their source/log hashes and
all 138 corresponding printed axiom records remain preserved and consistent.

## Metadata and mathematical scope

All twelve `main_results` and all twelve `alignment` entries match the exact
ordered declarations selected by `comparator.json` and actually exported by
`Solution.lean`. There are no replaceable definition holes. The candidate keeps
the full original four-formula conjecture and its parameter range; the allowed
`n=s=3` instance refutes the conjunction by an actual generic count of three
instead of four. It does not claim to settle the remaining individual formulas.

I checked the new descriptions against the actual definitions and exports and
the already accepted proof evidence. In particular, they accurately describe
the quotient by the entire vanishing ideal, genuine point-prime algebraic
smoothness, the whole-ideal tangent condition including singular points, actual
complex Fréchet derivatives, both off-diagonal contributions to the bilinear
full-entry distance, arbitrary exceptional polynomials on symmetric data, and
`Cardinal.mk` of the actual critical-point subtype. The component Hessian
description allows the nonsymmetric data that the exported theorem allows.

Two possible sources of overstatement are explicitly resolved in the wrapper.
The frozen `abcLocalChart` phrase “complete local ring” is disclosed as referring
to the ordinary localization, with no adic completion theorem. Hessian
nondegeneracy is not advertised as a separate scheme-theoretic multiplicity
formalization. Earlier statement/development phase notices remain historical
and are identified as such; they have not been silently rewritten.

Both final referees' retained evidence supports **61 source plus 12 diagnostic
LeanCert kernel assertions**, and **57 source plus 12 diagnostic printed
standard-three axiom reports**, per referee. Thus 73 assertions and 69 printed
reports are different counts, not conflicting claims. Referee 1 records 236
project declarations globally, 214 in the actual export closure and 39 material
dependencies. Referee 2 records the same 214-element closure and 28 independently
selected material dependencies. Thirteen fresh commands mean eleven mathematical
modules, a separate namespace-only admitted reference, and an inspector. The
reference admissions remain outside the proved dependency closure and the
development's zero-sorry assertion. This review did not repeat those builds.

The pinned Lean version and all **ten dependency revisions** match the actual
toolchain file and Lake manifest. The allowed axioms are exactly `propext`,
`Classical.choice`, and `Quot.sound`; no new axiom or imported literature premise
is asserted. LeanCert's actual `#assert_trust kernel` role is stated accurately.
The absence of interval computation follows from using exact algebra and the
fixed three-coordinate counterexample, rather than an artificial numerical
certificate.

The attribution publishes **George Stepaniants**, **Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA**, with AI assistance. It preserves the original Codex automated maintainer
audit's negative-resolution credit and the original Kubjas–Sodomaco–Tsigaridas
conjecture attribution. It does not claim source-author endorsement, human peer
review, historical priority or official Tau Ceti endorsement. No private API or
authentication receipt was read or copied for this review. The new candidate
documents contain no email-like address.

## Reproduction and actual checks

The concrete README explicitly uses `lake build Solution`. The historical
`defaultTargets = ["Challenge"]` remains unchanged, so a bare `lake build` is
correctly distinguished from checking the proof. The future repository-root
`bootstrap.sh`, `selftest.sh` and `verify.sh` commands identify the actual pinned
harness and the RA-20 project. Their non-root Ubuntu, clean committed candidate,
real isolation, rejection/control suite, exporter/default-kernel and Comparator
requirements agree with the repository harness. A local source/type replay is
not called a Linux Comparator run. Operational acceptance and canonical
Markdown/TeX/PDF/index publication are explicitly still required.

My [machine-readable result](../verification/candidate-packaging-referee-2026-09-13/RESULT.json)
and numbered command directories retain **21 successful read-only command
receipts**: sixteen `git show` original-source checks, the actual v0.4 schema and
export-coverage validator, both permanent-ID validators, the installer's portable
sealed-inventory verifier, and the canonical-file Git diff. The schema check
passed all twelve declarations; each ID check validated **217** permanent IDs.
The canonical problem, registry and canonical indexes remain unchanged.

I independently resolved **22 README links plus 7 handoff links** and **40 YAML
file-path occurrences**, checking their actual target bytes. The two original
source links specify the immutable original base and agree with its Git files.
Schema success establishes metadata consistency, not mathematical truth.

One reviewer-only diagnostic occurred: my initial parser inspected only README
but asserted the combined README-and-handoff count of 29. The actual README has
22 links. I preserved the failed script, traceback and explanation, then added
the seven handoff links and the independent metadata-path walk. The resumed
audit passed without a candidate edit. Its already successful sixteen immutable
Git receipts were reused only after checking exact commands, successful exits
and raw-log hashes; their outputs were not regenerated or replaced. Earlier
navigation diagnostics are separately recorded. No Lean compilation, copied
cache, numerical evaluation, Linux run or Git mutation occurred in this task.

## Seal and remaining boundary

The separate [review inventory](../verification/candidate-packaging-referee-2026-09-13/EVIDENCE-MANIFEST.json)
binds every installer input, the installer outer manifest itself, the additional
actual harness files read, this report, and all of this review's scripts,
snapshots, raw commands and diagnostics. Only its own exact outer manifest path
is excluded from its declared scope. Every earlier nested manifest is included.
The accompanying read-only `verify_inventory.py` rechecks complete membership,
all hashes and the narrowly defined historical archive mapping. Later root
acceptance/publication artifacts outside this review directory are outside this
fixed review seal.

No packaging correction is required for these exact bytes. This approval allows
the next committed-candidate verification stage; it does not promote RA-20 to
**Lean verified**. Actual Linux default-kernel/Comparator/controls, independent
operational acceptance and reviewed canonical publication remain pending.
