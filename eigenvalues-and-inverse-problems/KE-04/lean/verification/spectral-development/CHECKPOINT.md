# KE-04 Spectral development checkpoint

Paused at the coordinator's request to free a slot for the independent final
IE-05 reviews. This is incomplete proof development, not an approval or a
successful proof build. No command remains live.

Owned source: `NLA/KE04/Spectral.lean`, SHA-256
`a184f264d365dac03a865cf8dfd29d7997c5404faf5d351dcb29f507e6ba0e4b`.
Only this new module and `verification/spectral-development/` were written.
The module targets the exact frozen contracts 10, 13, 14 and 17 under
`NLA.KE04._proved`. It imports Definitions, LeanCert verification and Mathlib
tactics, not Challenge or concurrently developed project modules.

The full gate, Definitions, Challenge, numerical strategy, original Colbrook
proof, source correspondence, review standards and detailed original informal
review were read. The accepted gate is SHA-256
`5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624`;
the 1598-file statement freeze is SHA-256
`85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e`.
All 1598 hashes matched before and after the attempt. The inherited statement
documentation's old "no approvals" prose remains frozen; the accepted gate is
the authority for this proof phase.

Actual command:

```
python3 /tmp/nla-lean-formalization/next-ke04-statements-draft/lean/verification/spectral-development/run-attempt.py
```

The driver completed with exit 1. Attempt `attempt-qr384kbx` retains the exact
driver and source inputs, all 43 commands and raw stdout/stderr, source hashes,
10 package pins before and after, toolchain receipt, object hashes and cleanup.
The 43 commands are 40 read-only package identity/status commands, Lean version,
Definitions compile (exit 0), and Spectral compile (exit 1). Dependencies stayed
clean; nine existing package object directories were used read-only. Cli has
no objects. The fresh own output prefix began empty. Its two Definitions output
files were hashed, matched, and removed with that prefix. No cache was copied,
downloaded, built or modified. This is macOS local development, not Linux or
Comparator execution.

Next action on resumption: correct the current failed source using the retained
diagnostics, then run a new fresh attempt. The principal failures are:

- The roots proof through matrix `eigenvalues₀` leaves a cardinality `Fin.cast`.
  Prefer the linear-map roots theorem with a direct matrix/linear-map charpoly
  bridge, or transport the cast explicitly. The full multiset target must remain.
- The polynomial degree proof needs explicit nonzero `X - C` factors for
  `Polynomial.natDegree_mul`; the matrix expansion needs scalar distribution.
- `λ` is reserved syntax here; rename the eigenvalue argument `mu`.
- The PSD-zero bridge needs `dotProduct_comm` because Mathlib's Euclidean inner
  product formula puts the second argument first in its dot product.
- The assertion syntax is `#assert_trust kernel declaration`, as confirmed from
  the installed project convention. The current draft has its arguments reversed.

The eigenbasis action and monotonicity steps elaborated; the gap's scalar sign
argument covered both endpoint order branches. These observations are only
diagnostics inside a failed module. The printed `sorryAx` dependencies are Lean's
error-recovery output and are explicitly not accepted theorem evidence. No
admission was intentionally authored.

Proposed extra helper is `quadratic_apply_eigenvector`: from `act M v = mu • v`,
derive `act (quadraticMatrix M a b) v = ((mu-a)*(mu-b)) • v`. It is not yet a
stable API. No global `act_mul` helper is declared, avoiding collision with
the concurrent Frames module.

After source success, still required: remove warnings, a separate admission-free
exact-type/dependency inspector for all four frozen contracts, material-lemma
kernel assertions and actual axiom reports, final fresh compile, explicit
source/dependency bindings and sealed portable read-only verification evidence.
The contributor cannot serve as an independent final KE-04 mathematical referee.
