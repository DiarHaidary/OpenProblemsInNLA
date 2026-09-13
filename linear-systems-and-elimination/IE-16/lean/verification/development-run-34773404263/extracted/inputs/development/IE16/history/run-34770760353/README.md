# IE-16 remote development compiler

This directory holds source-only drafts for compiler feedback on the dedicated
`codex/lean-ie16-development` branch. It is **not an authoritative verification
package, a complete formalization, or a countable Lean-verified problem**.
The canonical IE-16 page, problem ID, target and status are unchanged. This
development branch is not a solution pull request.

Formalization work: George Stepaniants, Department of Computing and Mathematical
Sciences, California Institute of Technology, Pasadena, California, USA.
The underlying counterexample is due to Sidney Holden. AI assistance is used.

`SOURCE_INPUTS.json` binds the copied source/configuration snapshot. Existing
statement-stage `formalization.yaml`, `comparator.json` and `Challenge.lean` are
retained as source context; Challenge intentionally contains placeholders. This
job neither executes Comparator nor asserts statement fidelity, axiom closure,
independent kernel reconstruction or final referee approval.

The branch-scoped GitHub workflow uses Ubuntu 24.04 and pinned actions. On GitHub
only it installs the pinned Lean toolchain, runs `lake env true`, fetches the
Mathlib cache with `lake exe cache get`, and checks dependency revisions against
the committed manifest. Cached dependencies are trusted development inputs.
The directly imported LeanCert verification module is compiled from its pinned
source, then these draft modules are attempted in dependency order:

1. `NLA.IE16.Definitions`
2. `NLA.IE16.Numeric`
3. `NLA.IE16.Minimax`

Each direct Lean invocation uses `-M4096 -j1` inside a GNU `timeout 120s` bound.
A failed dependency prevents dependent draft compilations and records that skip.
Other source drafts, including `WeightedDraft.lean` when present, are retained
but not checked by this job. No aggregate `lake build` is run.

The artifact retains exact input copies and SHA256 hashes, command arguments,
separate raw stdout/stderr, return codes, timings and dependency pin records,
including on failure. Source hashes are rechecked after compilation. Successful
draft compilation alone must never change canonical verification status.

`ci_compile.py` refuses to run outside Linux GitHub Actions. No local Lean/Lake
execution or dependency copies are required to prepare or update this branch.
