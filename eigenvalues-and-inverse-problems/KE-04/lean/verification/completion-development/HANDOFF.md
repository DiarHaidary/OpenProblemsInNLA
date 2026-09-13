# KE-04 complete target proof handoff

**COMPLETE for the exact frozen contracts 22 and 24.** AI proof contributor
`/root/ie05_statement_referee2` implemented the full-prefix strict occupancy theorem
and its complete canonical largest-iteration consequence. This is author proof
completion, not independent final mathematical approval, Linux/Comparator
execution or publication readiness.

Source: `NLA/KE04/Completion.lean`, SHA-256
`4014011a7c6435c362ce4cf304aed8d7a8ad2e32ffb03448fbf43223c59a3f97`.

The exports under `NLA.KE04._proved` are:

```lean
strictIntervalOccupancy : FullPrefixBlockLanczosClaim
blockLanczosConjecture : BlockLanczosConjecture
```

The new generic bridge is:

```lean
psd_form_nonneg {m : ℕ} (M : Mat m) (hM : M.PosSemidef) (x : Vec m) :
    0 ≤ form M x
```

It is the existing Mathlib positive-operator nonnegative-inner-product theorem
transported through the genuine frozen Euclidean action.

## Complete mathematical assembly

The frozen target predicates and exact contracts were read, together with the
complete actual Krylov, Frames, Spectral, SpectralWindow, Transport, Intersection
and Nonannihilation modules. The original complete Colbrook proof, canonical
target, numerical strategy and review standards had been read in the preceding
spectral phases; their unchanged source bindings remain preserved here.

For arbitrary original inputs, independently chosen `Qk,Qj`, and admissible
`k,j,i`, the exact index lemma derives `2≤k` and both valid endpoint indices.
The identity `(i-1)+p = i+p-1` converts the source's one-based index convention.
Monotonicity of the actual ordered spectrum gives `a≤b`. Neither `a<b` nor simple
eigenvalues are assumed.

Under the negation of the required strict-interval existence conclusion, every
later eigenvalue lies outside the open interval. The spectral gap theorem makes
the actual later quadratic PSD, and the genuine congruence theorem lifts it to
`compressedQuadratic A Qj a b`. The actual earlier `p+1` consecutive eigenvectors
produce a dimension-`p+1` window with nonpositive earlier quadratic form, retaining
every eigenvalue repetition.

The given full dimension at `s` supplies full dimension at `k`, `k-1` and `k+1`
through the proved prefix theorem. All required inequalities are derived from
`k<j≤s`; no rank at `j+1` or additional nonbreakdown hypothesis is introduced.
The actual intersection theorem supplies a nonzero vector in both the window and
the previous Krylov space. Its earlier quadratic form is nonpositive. Transport
of the forms makes its later form nonpositive, and actual PSD makes that same
form nonnegative. Hence the later form is zero, and the genuine PSD-zero/kernel
equivalence gives the later quadratic kernel equation.

Only the later quadratic vector action is identified with `q(A)x`, using the
proved extra-power inclusion. The full-rank nonannihilation theorem at `k+1`
contradicts that kernel equation. Thus the strict interval contains a later Ritz
value for every permitted input. This argument also treats equal endpoint values
by contradiction; it never assumes separation in advance. Empty index cases and
all natural dimensions remain exactly as the frozen predicates specify.

Finally, `fullPrefix_implies_canonical` supplies the original largest-full-iteration
assertion. Both target propositions retain the original real symmetry, starting
block rank, all iteration and index quantifiers, and arbitrary independent frames.
No Challenge declaration or expected diagnostic proposition is imported.

## Actual fresh source and trust checks

The initial attempt `attempt-c7o2c3cd` compiled all nine source modules successfully.
The final fresh attempt `attempt-700n3s8e` compiled those same sources and a separate
admission-free inspector: ten commands, all exit zero. The mathematical source
was unchanged between them. There were no failed Completion proof attempts, and
no compilation was repeated after the successful final inspection.

Inspector SHA-256:
`317c5228a570227cfe4afe5b5a27240fd817a91a167c7a8bd75d94ea8cc9d3ed`.
It confirms that both actual exports are theorem declarations with types exactly
definitionally equal to the frozen `FullPrefixBlockLanczosClaim` and
`BlockLanczosConjecture`. It also prints the actual full definitions of these
predicates, `IterationOccupancy` and their rank/basis premises. The read-only
verifier compares the literal source signatures with the frozen Challenge text.

The inspector traverses both actual types and proof values to a complete closure
of 104 project declarations, including generated proof/equation/simp auxiliaries
and the actual coefficient extension/shift definitions. It rejects unsafe or
partial project declarations, diagnostic expected propositions and any transitive
axiom outside `propext`, `Classical.choice`, `Quot.sound`. Eighty-nine declarations
use all three, fourteen use `propext` and `Quot.sound`, and one uses only `propext`.
All 22 specified material dependencies occur in the actual proof terms, including
each step of the gap, window, prefix, intersection, transport, kernel and
nonannihilation path and the canonical reduction.

The final run contains 56 actual axiom reports and corresponding kernel assertions
across the imported modules, Completion and inspector. Six pairs concern the
three new material declarations across Completion and its inspector. Completion
and the inspector emit no warnings. The unchanged imported Krylov module emits
its already documented unused-simp-argument warning at line 107; that warning is
retained and has not been described as a warning-free whole build.

The complete actual source snapshots, executed driver, 101 command receipts with
raw stdout/stderr, toolchain identity, ten package pins before and after, and
all source bindings are retained. Both private output prefixes began empty and
used only the nine existing read-only package object directories plus Lean 4.33.1;
tooling-only Cli has no objects. Thirty-eight own generated objects were hashed
and matched before removing the two own prefixes. No package caches were copied,
downloaded, built or changed. No native proof execution or additional axiom was
introduced, and no interval computation was needed.

## Preservation and evidence scope

The unchanged statement freeze has 1598 inputs, SHA-256
`85d583c12fbbf1361cd128f7e98c359dd8990d3886ecfb9e8aed7c79793c305e`;
the accepted proof gate remains
`5e7cfd64709f436c684698fdb0c4adb5cc3f3e50f8945aa5fffdf70ec22fe624`.
All frozen hashes matched before and after both fresh attempts.

During the fresh builds, the existing SpectralWindow seal and four exact immutable
source pins for Krylov, Transport, Intersection and Nonannihilation supplied a
2764-file checked boundary. The last helper authors finished sealing their
unchanged sources during this phase. After the final build, their actual read-only
verifiers were inspected and executed, and the complete final imported union of
3047 files was checked before and after those three commands. This later seal
check is distinct from the earlier source-build checks.

The three preserved final imported seals are:

- SpectralWindow: 2759 files,
  `2fecf0e58267ebab396ccc9a4691fb1e41a751fe6e23e98c89a2842af01a269c`.
- Transport/Intersection: 2437 files,
  `b3232d8adb072dc44447a2a1f6f806f709bc55b4201b85d680d557645d9d72e8`.
- Nonannihilation: 1833 files,
  `d57bb205a29e51eefa1e1d67f662f052875a58961c750f6930028408251def68`.

Their original complete memberships, nested manifests, snapshots, historical
failures and command receipts remain unchanged. In particular, Nonannihilation's
sealer was executed only with its inspected read-only `--verify` branch.
`imported-helper-checks/` retains all three exact executed verifier snapshots,
commands, outputs and before/after union bindings.

The actual successful local read-only content preflight is `validation-tyefblp0`,
with its executed verifier/driver, command, stdout and stderr retained. The final
outer seal binds all own source and evidence plus the exact final imported union.
Its only self-exclusion is
`verification/completion-development/EVIDENCE-MANIFEST.json`.
Concurrent final wrappers and unrelated project changes are outside this scope.

From the project root, verify the bounded evidence without running Lean, Git,
an old build driver or cleanup:

```
python3 verification/completion-development/verify_seal.py
```

The final seal is checked after creation without adding a self-referential
final-run log inside the sealed directory. `HANDOFF.json` and `audit-result.json`
bind the final source, complete report and actual results.

Original mathematical proof credit remains Matthew J. Colbrook, Department of
Applied Mathematics and Theoretical Physics, University of Cambridge. Formalization
credit is George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA, with substantial
AI assistance. No previous helper source/evidence, frozen contract, metadata,
permanent ID, canonical status or Git state was changed. The coordinator still
owns the final 24-export wrappers and remaining independent review, Linux,
Comparator and publication gates. This contributor cannot serve as an independent
final KE-04 mathematical referee.
