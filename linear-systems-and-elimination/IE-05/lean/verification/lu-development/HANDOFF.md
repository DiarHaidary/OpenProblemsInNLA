# IE-05 generic scaled-LU helper handoff

`NLA.IE05._proved.scaledLU_trajectory` is complete with the exact frozen generic
signature. Import `NLA.IE05.LUTrajectory`. The source is frozen at SHA256
`96d71b7a46ec692f9e84e6450adacfa71b9c79ef69ff17222e44173f3e6abcbb`.

It proves the actual first-available no-swap path, actual scan equality, and all
scaled trailing-product states for every `k ≤ n`. Its hypotheses are exactly
unit-lower `L`, lower multipliers of absolute value at most one, upper `T` with
positive diagonal, and positive column scales. It does not assume determinant
nonzero, a valid path, or a desired trajectory. The terminal-zero state and all
ties are covered.

The fresh four-command run `attempt-x4p3dxwm` passes the exact frozen type,
42 actual project declarations, 29 material dependencies, and 23 explicit
kernel/standard-three checks. All 733 frozen inputs, 27 original Git blobs, ten
pins, and both previous complete handoff inventories remain unchanged. All
three raw attempts and private-object cleanup records are retained.

See `../../reviews/lu-completion.md` for the complete route, nine helper
interfaces, counts, roles, original attribution, and scope limits. This is an
author handoff, not an independent final approval or actual Linux verification.
No other proof module, canonical status, registry, metadata, or Git branch was
changed. Root retains the integer certificates and real-growth work.

`EVIDENCE-MANIFEST.json` includes the entire scoped directory and explicit
source/boundary bindings, including nested manifests. Only the exact outer
manifest itself is excluded. `python3 verify_seal.py` checks integrity read-only.
