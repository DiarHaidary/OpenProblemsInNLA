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
3. `NLA.IE16.Minimax` (independent of Numeric)
4. `NLA.IE16.WeightedDraft`
5. `NLA.IE16.WeightedBridgeDraft`
6. `NLA.IE16.FullMinimumDraft`
7. `NLA.IE16.SubsetBoundsDraft` (independent of Numeric)
8. `NLA.IE16.SubsetGeometryDraft`
9. `NLA.IE16.FinalContractsDraft`
10. `Solution` (public export assembly and LeanCert trust/axiom diagnostics)

Each direct Lean invocation uses `-M4096 -j1` inside a GNU `timeout 120s` bound.
The driver reads the direct local imports, checks this order, and records the
resulting dependency graph. A failed dependency skips only its descendants;
independent modules are still attempted. No aggregate `lake build` is run.

The artifact retains exact input copies and SHA256 hashes, command arguments,
separate raw stdout/stderr, return codes, timings and dependency pin records,
including on failure and including hidden input files. Source hashes are rechecked after compilation. Successful
draft compilation alone must never change canonical verification status.

`ci_compile.py` refuses to run outside Linux GitHub Actions. No local Lean/Lake
execution or dependency copies are required to prepare or update this branch.

The previous run at commit `d820c88c8720dd5dcadda222d11520af9725290e`
(run `34770760353`) compiled LeanCert Verification and Definitions successfully;
Numeric failed and the then-dependent Minimax was skipped. This is compiler
feedback, not a complete verification result. The new snapshot preserves those
source bytes under `history/run-34770760353` before applying fixes. That first
artifact omitted two hidden input copies because of the upload default; their
recorded hashes match the exact Git commit. Subsequent uploads explicitly include
hidden files. The original artifact remains unchanged in the private run evidence.

Run `34771972369` at commit `28bdf9e85541764b6a5cb2debd647b9cebaea21f`
retained all 38 input copies, with matching hashes and ten matching dependency
pins. LeanCert Verification and Definitions passed; Numeric and Minimax failed
and their descendants were skipped. The retained raw compiler errors motivated
the next exact coordinate and syntax repairs in `NUMERIC_OPTIMIZATION.md` and
`SOURCE_CHANGES.json`. None of these development runs establishes final proof
acceptance. The previous source bytes are under `history/run-34771972369`.

Run `34772589024` at commit `5d9212c7f52448872e01852926be448c38d882a4`
retained all 46 input copies with matching hashes. Numeric's sole remaining
compiler error was the four-moment theorem reaching its default heartbeat
limit; the current draft grants that theorem 800,000 heartbeats after reducing
the algebraic degree to seven. Memory, one-thread execution and the 120-second
module wall-clock bound are unchanged. Minimax's three concrete API errors
are repaired in this snapshot; analogous explicit arguments are supplied in
the downstream drafts. These changes await new remote feedback. The prior
source snapshot remains under `history/run-34772589024`.
