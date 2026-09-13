# KE-04 spectral helper completion

**COMPLETE for the four assigned helper contracts.** This is an author development
report by AI proof contributor `/root/ie05_statement_referee2`, not an independent
final mathematical approval of KE-04. No Linux or Comparator run is claimed.

The completed source is `NLA/KE04/Spectral.lean`, SHA-256
`64e8255697387e32e65cf591a0cb7dbf7986f471c82b4f1715c9a88a7650e20e`.
The exact frozen exports, in namespace `NLA.KE04._proved`, are:

- Contract 10: `orderedSpectrum_semantics`.
- Contract 13: `quadratic_semantics`.
- Contract 14: `spectral_gap_quadratic_psd`.
- Contract 17: `psd_zero_form_iff_kernel`.

The additional generic `quadratic_apply_eigenvector` accepts any real square
matrix, real `a,b,mu`, vector `v`, and `act M v = mu • v`. It concludes
`act (quadraticMatrix M a b) v = ((mu-a)*(mu-b)) • v`. It does not need symmetry.
This helper is available for the remaining spectral-window assembly.

## Mathematical scope and reuse

The full canonical target, complete Colbrook proof, frozen Definitions and
Challenge, numerical strategy, source correspondence and repository review
standards were read before implementation. The accepted proof gate is SHA-256
`5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624`;
the complete 1598-input statement freeze is SHA-256
`85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e`.
Those files supersede the historically frozen pre-approval prose without changing
any historical statement document.

The ordered-spectrum proof reverses Mathlib's antitone self-adjoint eigenvalues
and the matching orthonormal basis. Its roots equality uses the actual linear-map
characteristic roots theorem, the matrix/linear-map characteristic polynomial
bridge, and a permutation of the complete finite multiset. It preserves all
algebraic multiplicities. It neither replaces roots by a set nor assumes distinct
eigenvalues.

The quadratic is the actual monic degree-two polynomial `(X-C a)*(X-C b)`.
The matrix statement proves both its algebra evaluation and its expanded formula.
The gap proof shows each quadratic eigenvalue product is nonnegative, diagonalizes
the actual quadratic action in the same orthonormal basis, and applies Mathlib's
diagonal PSD and orthonormal matrix/positive-operator bridges. The hypotheses
remain exactly `a ≤ b` and exclusion of every eigenvalue from the strict open
interval. Repeated values, `a=b`, and dimension zero remain included.

The zero-form/kernel equivalence transports
`Matrix.PosSemidef.dotProduct_mulVec_zero_iff` to the frozen real Euclidean action,
using dot-product symmetry. Singular PSD matrices are included. All arithmetic
is exact; no numerical interval or artificial certificate is introduced.

The module imports only Definitions from this project, plus the pinned LeanCert
verification and Mathlib module tactic. It does not import Challenge, Frames,
Krylov, or any diagnostic expected proposition. The stable Frames handoff was read
and its advertised source hash checked, but its implementation is not used or
included in this helper's seal.

## Actual verification

Final fresh attempt `verification/spectral-development/attempt-k2z1xc0b` compiled
Definitions, Spectral and the separate admission-free inspector, all with exit 0
and no warnings. The source was also successful in the preceding fresh source-only
attempt `attempt-k0z8w9ex`. No additional compilation was run after these checks.

`Inspect.lean`, SHA-256
`0eba246cae16b7faae8ab69afc3e626f18a7c2c5cf9616469ef83aeb6a362e39`,
checks that the four actual declarations are theorems and their types are
definitionally equal to the frozen contract propositions. The read-only verifier
also compares their literal source signatures with the frozen Challenge text.
The inspector follows both types and actual values of project declarations,
rejects unsafe/partial project declarations, disallows diagnostic propositions,
and checks every collected transitive axiom against the three foundational axioms.

The actual closure contains 22 project declarations, including generated
definition proof constants, the polynomial equation theorem and the generated
zero-form simp auxiliary. Twenty-one report the foundational three
`propext`, `Classical.choice`, `Quot.sound`; the remaining definition proof reports
only `propext`. All 25 explicitly required material dependencies are present in
the actual proof terms. Ten material `#assert_trust kernel` commands and ten
corresponding actual axiom reports occur across the final source and inspector.
The complete printed terms, full direct dependency lists and raw Lean logs are
retained; this report's proof assessment uses the source and actual audit output.

All four fresh attempts retain their exact driver/source snapshots, 173 actual
command receipts with stdout/stderr, toolchain identity, source hashes before and
after, and dependency checks. The ten Git-pinned packages were clean before and
after each attempt. The nine existing package object directories and the Lean
4.33.1 toolchain were used read-only; tooling-only Cli has no object directory.
Each own output prefix began empty. Fourteen own output objects across the four
prefixes were hashed and matched before removal. No caches were copied,
downloaded, built or changed.

The separate source capture retains 60 actual read-only Git command receipts,
binding all seventeen original source snapshots and thirteen reused Mathlib or
LeanCert API files to exact commit/path/blob identities. The complete original
proof block is unchanged from Colbrook's original submission: 2622 bytes,
SHA-256 `3ba1bd9a62a00aaf787758af6312e4787ca8d6db02b4487e8b956ce0553977a7`.

## Retained failures and preservation

The first Spectral attempt `attempt-qr384kbx` failed on a cardinality cast in an
alternative roots bridge, incomplete algebra rewrites, a reserved binder name,
dot-product orientation and reversed trust-assertion arguments. The second,
`attempt-wzr6ev6d`, failed on one redundant rewrite in the eigenvector helper.
Their raw error-recovery `sorryAx` reports remain explicitly historical failed
records. They are not accepted theorem evidence. The proof source contains no
authored admission, native proof command or custom axiom.

The coordinator-requested pause checkpoint remains unchanged. Its exact immutable
110-file seal is SHA-256
`ef842aa46a2b84b05be31fcf667bb2b6f60513abe34edbca62e96838845d46b8`.
It binds the first attempt's source snapshot, not the later live module; no hash
was waived or replaced. Every actual attempt source remains available by its
explicit version and full snapshot path.

All 1598 frozen input hashes matched before and after every attempt and again in
the successful read-only content preflight `validation-3xi4xrva`. Its executed
verifier/driver, actual command, stdout and stderr are retained. The final outer
seal covers the complete own evidence, this report, the completed source, all
1598 unchanged frozen inputs, the freeze and accepted gate. Its only self-exclusion
is the exact path `verification/spectral-development/EVIDENCE-MANIFEST.json`.
Concurrent modules and their evidence are outside the explicitly enumerated scope.

The portable read-only verifier is `verification/spectral-development/verify_seal.py`.
It verifies the seal and retained execution records; it does not rerun Lean or an
old mutating driver. The final seal is checked after creation without writing a
self-referential final-run log into the sealed directory.

Original proof credit remains Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge. Formalization credit
is George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, with substantial AI assistance. This work
does not change frozen statements, metadata, permanent IDs, canonical status or
Git state. The remaining KE-04 contracts, whole-proof assembly, independent final
reviews and actual Linux/Comparator gates remain the coordinator's work.
