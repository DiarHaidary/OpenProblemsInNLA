# RA-20 smooth-locus transport helper

Completed by `/root`, a disclosed implementation contributor; this is not an independent mathematical review.

`NLA.RA20.smoothLocus_comap_algEquiv` proves, for arbitrary commutative base ring and commutative algebras, that the comap of a prime along an algebra equivalence belongs to the actual `Algebra.smoothLocus` exactly when the original prime does. It constructs the genuine equivalence of localized algebras from equality of the mapped prime-complement submonoids, then uses Mathlib `Algebra.FormallySmooth.iff_of_equiv`. There is no finite-presentation or assumed-smoothness premise.

The helper was requested by the owner of the genuine ABC local hypersurface proof, for transport through the separately proved reduced-coordinate-ring equivalence. This helper alone proves no missing RA-20 conjecture contract or final count. It changes no frozen definition or statement.

The exact prospective helper statement and ownership were recorded before its first implementation. Two fresh direct-source attempts are retained. The first failed because the diagnostic proof had not unfolded membership in a prime complement before rewriting; LeanCert correctly rejected the resulting failed declaration's temporary `sorryAx`. The correction explicitly changes that membership into nonmembership of the prime ideal. The second source compilation succeeded and executed one real LeanCert kernel assertion and one standard-three axiom report. No explicit admission, native computation or custom axiom occurs in the completed helper.

Both attempts use new empty target prefixes with all ten exact shared dependencies read-only, checked clean before and after. Their source snapshots, command identities, complete logs, pins and results are retained. Only their own generated objects were hashed and removed. These are local macOS source checks, not Linux replay or a complete-target verification. The 68 frozen statement inputs and original source snapshots remain unchanged.

Source SHA-256: `0e7717ac9e55597ed69a816f44194af569ac7b092ceb4f9231ea86e4c7ad894f`. Successful result SHA-256: `7244dfdc5b291496f9e880f761ae2b34708337bb7baa1eb524d1d7dd654e8a00`. Gate/ownership SHA-256: `6f565c866d9a6bbaea1b12f20a58570a3285c8f1ac8de5650d67fc6a11f3bdc7`.
