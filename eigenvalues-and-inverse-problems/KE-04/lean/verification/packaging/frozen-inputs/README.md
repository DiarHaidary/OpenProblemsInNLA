# KE-04: statement-only Lean draft

This isolated draft proposes the complete strict open-interval occupancy theorem
across block Lanczos iterations. The permanent canonical problem remains
`eigenvalues-and-inverse-problems/KE-04/README.md`, mathematically **Solved** at the
pinned upstream base `5830ed4fb06da0659414a3deb2a40ad327aca052`.

The draft contains actual real block Krylov spaces, arbitrary orthonormal bases,
genuine ordered compression eigenvalues with multiplicities, and all original
dimension and index quantifiers. The full-prefix theorem follows the original
proof's stronger hypothesis and is accompanied by the complete canonical
largest-iteration target. Positive block width is required for the separate
maximal-index existence obligation. No endpoint separation, spectral simplicity,
interval occupancy, or quadratic nonannihilation is assumed in the input model.

Read [NUMERICAL_TARGETS.md](NUMERICAL_TARGETS.md), the complete retained originals,
[Definitions](NLA/KE04/Definitions.lean), all 24
[Challenge contracts](Challenge.lean), and
[SourceCorrespondence.md](SourceCorrespondence.md) before reviewing. The
[statement handoff](STATEMENT-HANDOFF.md) and `DRAFT-INVENTORY.json` identify the
exact review input; the inventory excludes only itself.

No proof is implemented. Challenge has 24 intentional `sorry` bodies. Neither
`Solution.lean` nor a proof module exists. Two fresh independent statement
approvals and the coordinator's acceptance are required before proofs; this
authoring package is not frozen and supplies no independent approval.

Original mathematical proof: Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge, Cambridge, United
Kingdom. The retained source discloses its ChatGPT draft origin and independent
Codex-agent informal review. Prospective formalization: George Stepaniants,
Department of Computing and Mathematical Sciences, California Institute of
Technology, Pasadena, California, USA, with substantial AI assistance. No external
human peer review, formal proof certificate, or Tau Ceti endorsement is claimed.

## Development validation

Lean is pinned to 4.33.1, LeanCert to
`621a43d7cf21f87872392a01e874f2f1dbddc926`, and Mathlib to
`0df444a360eaa60ab8c11dca51a86af692955474`. The complete ten-package manifest is
included as draft configuration; it has no floating dependency identities.
`Solution` in the project and Comparator configuration is a reserved future
module, not an existing proof. Comparator's 24 targets match Challenge exactly,
`definition_names` is empty, and only `propext`, `Classical.choice`, and
`Quot.sound` are permitted.

The author runner is:

```sh
python3 verification/statement-development/check_statements.py
```

It makes a new immutable input snapshot and a new private output prefix on each
invocation, calls the pinned Lean binary directly, and uses the existing nine
read-only dependency build directories. The tenth manifest dependency, Cli, is
tooling-only and unbuilt here; it is not added to `LEAN_PATH`. It checks all ten
source pins and clean statuses before and after, hashes and removes only its own
objects, and retains failures. It neither calls Lake nor copies, downloads,
rebuilds, deletes or modifies dependency caches.

The successful attempt `attempt-r5fn2nl_` elaborated Definitions, Challenge and
two inspectors, all with exit code zero. The definition-only inspector did not
import Challenge; all 27 custom definitions passed actual LeanCert
`#assert_trust kernel` commands and transitive `#print axioms` checks. The separate
type inspector printed every target signature. The first run's reporting failure,
subsequent capture diagnostics and an integrity-runner write-path error are
documented in the evidence. The latter required this new identical-source run;
see `verification/EVIDENCE-RECOVERY.md`. These checks
establish source elaboration and definition trust only, on macOS with preexisting
dependency objects. They establish no KE-04 theorem, full proof build, Comparator
pass, raw-kernel replay or authoritative Linux sandbox result.

The later proof must import shared Definitions independently, never Challenge.
It must prove all advertised declarations, audit their transitive axioms, and
pass the repository's actual independent and mechanical gates. This argument is
pure finite-dimensional algebra; the pinned LeanCert trust audit has a concrete
role, and no artificial interval computation is required.

## Provenance and license

Original Git-bound sources and prior review are preserved in `verification/`.
Selected pinned Mathlib, LeanCert, Schiffer, Forsythe and Tau Ceti text files are
archival inspection evidence, with their own copyright/license terms preserved.
They are not project proof implementations or replaceable dependencies.

The root Apache-2.0 license applies to newly authored draft code. It does not
relicense retained third-party source snapshots. Schiffer is a structural
reference only; no implementation is reused. The source correspondence names
the formal APIs and structural patterns actually inspected.

No canonical file, ID registry, status, publication YAML, Git state, PR or commit
is modified by this isolated draft. Eligibility is a bounded dated observation,
not a priority or exhaustive duplication claim.
