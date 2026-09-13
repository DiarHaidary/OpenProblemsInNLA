# NR-03 conditional bridge diagnostic provenance

This source-only refactor follows the two statement approvals recorded before
proof implementation in `INTERFACES.md` and `DISCHARGE-GRAPH.json`. The current
source inventory is `../SOURCE_INPUTS.json`; this note is not a Lean result.

Base commit: `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`.
Actual preceding Linux run:
https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34780136595

That run passed all 48 row modules (384 closed row declarations) and all three
full family identities. `Certificate` exited 124 after 120.022 seconds; both
raw output streams were empty. The evidence does not identify a failing
declaration or tactic. `Rank` and `Solution` were skipped. Nothing in this
record establishes the full original problem or its ten public exports.

The old Certificate bytes are preserved outside this package in the immutable
preceding Git commit and the raw run's recorded inputs. Their SHA-256 is
`e60c3e56f0906e1af334e84f12d07f4b3426232691b71f66ce03ecef2b358fe5`.
The retained preceding raw artifact has SHA-256
`713431f8b35ec8eaa4473b6529d1a133b969dcda97a47e716be467a0565f258d`.

This diagnostic compiles Definitions, Encoding, FamilyDefs, Index, and the new
conditional CertificateBridge, alongside the unchanged LeanCert support
module. It deliberately omits the expensive row chain and the final
Certificate/Rank/Solution modules. The complete source graph remains present:
Certificate supplies every helper premise using the existing core and full
family proofs, so no public theorem gains an assumption. All original row,
core, family, Rank, Solution, Definitions and Challenge bytes are unchanged.
The four generic data/positivity declarations only move, with exact old bodies.

The retained `../row-certificates/SOURCE-MANIFEST.json` and generator describe
the earlier full-row generation phase. Their row outputs still match exactly;
this refactor intentionally supersedes their Certificate and driver outputs.
Do not rerun that historical generator over this source without preserving the
new bridge. The current `../SOURCE_INPUTS.json` binds every candidate input.

Each direct Lean invocation retains `-M4096 -j1` and a 120-second GNU timeout;
the unchanged existing workflow retains its 30-minute job cap. No local
compiler/cache download, canonical status update, or verification claim is
part of this refactor. Final complete-graph and canonical acceptance remain
pending even if this conditional diagnostic passes.
