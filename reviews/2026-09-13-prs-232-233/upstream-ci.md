# IE-05 and KE-04 GitHub CI authentication

**PASS.** Each listed workflow completed successfully on the exact reviewed pull-request head. The GitHub artifact digest and size, complete tracked input set, every input SHA-256, checked merge parents and tree, configuration, tool receipt, and actual proof and rejection-control transcripts agree.

| PR | Project | Head | Run | Artifact | Tracked inputs | Exports | Standard axiom reports |
|---|---|---|---|---|---:|---:|---:|
| [#232](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/232) | linear-systems-and-elimination/IE-05/lean | `5ce3e36cacbebcafda267eb6a9f2a42c461b189b` | [34762080497](https://github.com/ajt60gaibb/OpenProblemsInNLA/actions/runs/34762080497) | `10318952831` | 3,306 | 17 | 89 |
| [#233](https://github.com/ajt60gaibb/OpenProblemsInNLA/pull/233) | eigenvalues-and-inverse-problems/KE-04/lean | `ecd7d63a22e40db0967a9cb8e785555a0fad6ca8` | [34761728434](https://github.com/ajt60gaibb/OpenProblemsInNLA/actions/runs/34761728434) | `10319615824` | 4,284 | 24 | 77 |

Across the receipts: **7,590 inputs, 41 exports, and 166 standard-axiom reports**. All ten actual dependency checkout revisions for each project match its committed Lake manifest; the log includes each clone URL and exact revision.

Each proof was built from a fresh project snapshot and accepted by the Lean 4.33.1 default kernel and the pinned Forsythe Comparator. Challenge and Solution export the identical configured theorem list. Every axiom report is tied to its actual `#print axioms` source line and uses only `propext`, `Classical.choice`, and `Quot.sound`.

The audit checks actual case transcripts: an honest inductive/quotient fixture is accepted; the malformed raw proof and quotient mismatch are rejected; all five Comparator regression cases produce their required real acceptance or exception. The admitted-proof and native-decision fixtures are rejected for `sorryAx` and the generated native axiom. This is more than reading a final PASS line.

Both actual Linux sandbox modes pass their filesystem, namespace, process, capability, network, AF_UNIX, and nested-namespace probes. Build permits only its designated `.lake` write; export rejects that write. All four invalid sandbox option fixtures are rejected.

The shared verifier, workflow, and toolchain files are unchanged from the reviewed base and the previously reviewed `5830ed4fb06da0659414a3deb2a40ad327aca052` anchor. The source lock binds Forsythe `8d1b0c0545a77b40245e84705aa7d273e6c81e62`; the live pinned probe source and exact locally applied CI adaptation hash match the receipt.

The adjacent JSON records full commit identities, artifact digests, input-manifest hashes, theorem names, tool receipts, dependency pins, and individual log hashes. Original raw GitHub responses and artifact ZIPs remain beside each input receipt in the audit scratch directories. Mathematical correspondence and scope are assessed in the independent problem reviews.

Authenticator SHA-256: `dc6d6b1429ef796fad57d92eab2880a91630262c2f9617650e6be71dd652db5c`.
