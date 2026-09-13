# NR-03 conditional bridge Linux result

The exact authorized run **34782819568** succeeded at commit
`3b3eb8f3fa384e4b3bf640d48bca87cf40db9565`. This is an implementer operational
audit of a conditional helper diagnostic, not independent acceptance of the
complete NR-03 proof. No duplicate run, retry, cap change, local compiler,
source edit, or public status update was performed.

Job 103792798110 ran from 21:06:42 to 21:09:01 UTC on 13 September 2026
(139 seconds). Artifact 10325795906 is retained as `artifact.zip`:
153,418 bytes, SHA-256
`a26f6da9cbd27cc1827af952b7060ff86e75c9f1e2e68990677ef3e8a68ebbf8`.
The raw metadata, command records, dependency pins, source copies, and logs
are retained unchanged beside this report and under `extracted/`.

All 107 recorded source copies match the exact Git commit, the independent
source-reviewed candidate, the before/after source inventory, and the 106
entries of SOURCE_INPUTS (which excludes itself). All ten package revisions
match the pinned manifest. Every executed Lean module retained 4096 MiB,
one thread and a 120-second GNU timeout; the workflow retained 30 minutes.

Six modules exited zero:

| Module | Actual seconds |
| --- | ---: |
| LeanCert.Tactic.Verification | 3.160 |
| Definitions | 2.251 |
| Encoding | 3.605 |
| FamilyDefs | 3.356 |
| Index | 3.573 |
| CertificateBridge | 3.242 |

CertificateBridge's actual stdout prints the three original generic data
types and axiom diagnostics for genericD_positive, full_sum_decomposition,
full_identity_of_components, and scaled_identity_of_full. Every observed
axiom set is exactly `propext`, `Classical.choice`, and `Quot.sound`.
All four theorem declarations completed in the successful module; stderr is
empty and no compiler error was reported. The raw stdout SHA-256 is
`103425e369d91b638542af2a2363bb04ce87b5ff076a8d04f830ec7917973f30`.

The diagnostic deliberately did not compile the row chain, the final
unconditional Certificate wrappers, Rank, or Solution. No ten-public-export
acceptance, Comparator result, default-kernel pass, or sandbox/negative-control
result is inferred. The prior successful family diagnostics remain separate
evidence. Complete canonical verification and final independent acceptance
are still required before NR-03 can contribute to the campaign count.

`CHECKS.json` contains the collector's Git/pin/source/bounds checks;
`BRIDGE-RESULTS.json` contains the actual declaration and timing audit.
The independent source review predating this run is
`/tmp/nla-nr03-bridge-source-review/REVIEW.md`, SHA-256
`f50de91e27abd5ccf98800f1adb80c53c1f5e6942302c37968ec3b07aefd216d`.
Its source bytes match this run, but that earlier report was source-only.
