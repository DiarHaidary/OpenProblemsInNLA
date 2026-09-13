# KE-04 spectral-window helper completion

**COMPLETE for frozen contracts 11 and 15.** This is proof-author completion by
AI contributor `/root/ie05_statement_referee2`, not independent final mathematical
approval of KE-04 or Linux/Comparator execution.

Completed source: `NLA/KE04/SpectralWindow.lean`, SHA-256
`c59a80ed6a6dff4e879fb6b8ca602a1d0946ef29b61ff400ffba0122bc86760f`.

The exact exports in `NLA.KE04._proved` are:

- `compression_basis_independent`: for arbitrary equal-span orthonormal frames,
  an actual square orthogonal change of basis, the compression similarity,
  characteristic-polynomial equality and equality of the increasing Ritz-value
  function, including multiplicities.
- `spectral_window_subspace`: a genuine subspace of the column space with dimension
  `p+1`, on which the actual lifted quadratic has nonpositive form, for every
  admissible `i,p` with `i+p<m`.

The extra reusable helper is:

```lean
orthonormal_span_form_nonpos {n q : ℕ} (M : Mat n)
    (v : Fin q → Vec n) (d : Fin q → ℝ) (hv : Orthonormal ℝ v)
    (heig : ∀ j, act M (v j) = d j • v j) (hd : ∀ j, d j ≤ 0)
    (x : Vec n) (hx : x ∈ Submodule.span ℝ (Set.range v)) : form M x ≤ 0
```

## Source and proof assessment

The complete original Colbrook proof, frozen numerical strategy and original
mathematical target were read in the preceding spectral phase. For this phase,
the accepted gate, both exact Challenge contracts, and the complete actual Frames
and Spectral modules were read again. Their read-only preservation verifiers
passed before development. The original mathematical proof remains credited to
Matthew J. Colbrook, Department of Applied Mathematics and Theoretical Physics,
University of Cambridge. Formalization credit is George Stepaniants, Department
of Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA, with substantial AI assistance.

For basis independence the constructed matrix is `O = Q.transpose * R`.
The actual projection fixed-space theorem proves `R = Q * O`; the two genuine
frame equations give `O.transpose * O = 1`, hence the opposite square inverse
identity. Direct matrix algebra gives the similarity. Characteristic polynomials
are invariant by `Matrix.charpoly_mul_comm`. Mathlib's self-adjoint
`eigenvalues_eq_eigenvalues_iff` then gives equality of the exact ordered spectral
functions after matching the characteristic polynomials of the Euclidean linear
maps. No basis compatibility or spectrum equality is assumed.

For the window, `t j = i + j.val` embeds `Fin (p+1)` into `Fin m`.
The family consists of `act Q (orderedEigenbasis (compression A Q) hM (t j))`.
The frame's inner-product identities and the injective index embedding preserve
orthonormality. `finrank_span_eq_card` proves that the actual span has dimension
`p+1`, regardless of repetitions among the corresponding eigenvalues. Monotonicity
places each eigenvalue between the two actual endpoint values, so each quadratic
eigenvalue product is nonpositive. The existing quadratic action lemma gives the
lifted eigenvector equations. The extra helper expands any member of the span
as a finite linear combination and uses `Orthonormal.inner_sum` to express its
form as a sum of nonpositive eigenvalues times coefficient squares.

Thus eigenvalue multiplicities, `p=0`, coincident endpoint values and every
dimension allowed by the exact hypotheses remain included. No distinct-value,
positive-gap, nonzero-vector or simple-spectrum premise was added. There is no
interval or approximate numerical computation.

## Actual source and trust checks

Final fresh attempt `attempt-zq1v44eo` compiled Definitions, Frames, Spectral,
SpectralWindow and a separate admission-free inspector; all five commands exited
zero, with no warnings. The preceding source attempt `attempt-5sd34slq` had already
compiled all four source modules successfully. No proof compilation followed the
successful final inspection.

Inspector SHA-256:
`b7ad5ff8b97294567ccec35990803a6e94c22cbb2cb5a8208fa07492af9d4382`.
It checks that both actual exports are theorem declarations whose types are
definitionally equal to the frozen propositions. The read-only verifier also
compares the actual source signature text to the frozen Challenge signatures.
Neither the proof nor inspector imports Challenge or a placeholder proof.

The actual project closure has 43 declarations, including imported definition
proofs, equation theorems and five new arithmetic proof auxiliaries. It follows
both types and actual values, rejects unsafe/partial project declarations and any
diagnostic expected proposition, and checks every transitive axiom against
`propext`, `Classical.choice`, `Quot.sound`. Thirty-seven declarations use all three;
five arithmetic auxiliaries use `propext` and `Quot.sound`; one imported definition
proof uses only `propext`. All 25 required material dependencies occur in the actual
proof terms. Six new material kernel-trust assertions and six corresponding axiom
reports pass across the source and inspector. Imported modules' existing kernel
assertions also execute during the fresh build.

All actual types, project edges, full direct dependencies, printed proof terms and
raw Lean outputs are retained. The inspector is an author mechanical check, not a
substitute for the later independent final reviews.

## Preservation and failed attempts

All four attempts retain exact source/driver snapshots, 181 executed command
receipts with raw stdout/stderr, before/after source bindings, ten clean package
pins, toolchain identity and object cleanup records. Each own output prefix began
empty. Nine existing pinned package object directories plus Lean 4.33.1 were used
read-only; tooling-only Cli has no object directory. Thirty own output objects
were hashed and matched before removing the four own prefixes. No dependency
cache was copied, downloaded, built or modified.

The first attempt `attempt-cmujju9q` failed before elaborating the new module because
the guessed `Mathlib.Tactic.Omega` module does not exist in this pin. It was replaced
by the actual Lean `Lean.Elab.Tactic.Omega` import. The second attempt
`attempt-k3h_4ob1` failed on namespace/explicit-argument API mismatches and an
unfolded compression bridge. Both complete failed attempts remain historical
diagnostics; their errors and the second attempt's error-recovery `sorryAx` reports
are not accepted theorem evidence. No admission, native proof command or custom
axiom was authored.

The statement freeze SHA-256 remains
`85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e`,
and the accepted gate remains
`5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624`.
Every one of the 1598 frozen hashes matched before and after every attempt.
Both imported seals and their complete 2245-file union also matched before and
after every attempt:

- Frames source `bfea6b02091db4e999c2c870b4b1f238cb546ad84df010c7d5431fe82904db0b`;
  seal `73770debb7678e443032c5f30e77ef82365cd32b81d24bba161990e2ac7f8db8`.
- Spectral source `64e8255697387e32e65cf591a0cb7dbf7986f471c82b4f1715c9a88a7650e20e`;
  seal `27a8328c569a17db1e6cf671a0a79034e3ce9eb2dc85c4640d13be7624191ca2`.

The additional API capture retains twelve actual read-only Git command receipts
and six complete Mathlib source snapshots, each equal to the clean pinned working
file and its exact commit/path/blob. Prior original-source bindings, statements,
reviews, failed attempts and seals are preserved through the imported seal union.
There are no basename exclusions or substituted historical hashes.

The successful read-only content preflight is `validation-i82h7cu_`, retaining its
executed verifier/driver, actual command, stdout and stderr. The final outer seal
enumerates the entire own module/evidence plus the explicit imported union. Its
only self-exclusion is the exact path
`verification/spectral-window-development/EVIDENCE-MANIFEST.json`.
Concurrent Krylov and coordinator implementation files are outside this scope.

From the project root, the portable verifier runs without executing Lean, Git,
an old driver, a build or cleanup:

```
python3 verification/spectral-window-development/verify_seal.py
```

The seal is checked after creation without writing a self-referential final-run
log inside it. `HANDOFF.json` and `audit-result.json` bind the final source and
actual checks. No frozen statement, imported source, previous evidence, metadata,
permanent ID, canonical status or Git state was changed. Whole-proof assembly,
remaining contracts, independent final mathematical reviews and the actual
Linux/Comparator gates remain outstanding. This contributor is ineligible as an
independent final KE-04 mathematical referee.
