# IE-05 exact certificates and generic QR/LU helper completion

**Completion verdict: ready for growth-proof assembly.** The three exact
certificate theorems and generic QR/LU identification helper passed a joint fresh
source check and admission-free inspection. No mathematical source was edited.
This is a bounded helper completion record, not an independent final mathematical
approval, complete IE-05 proof, Linux run or Comparator result.

Inspector: OpenAI Codex agent `/root/ie05_statement_referee2`. Root owns the helper
implementations. `/root/formal_review_standards` contributed the minimal exact
certificate decidability fix and its separately sealed diagnostic evidence.
George Stepaniants retains the full Department of Computing and Mathematical
Sciences, California Institute of Technology affiliation in both source headers.
The historical statement gate already authorized proof development; this report
does not create or change that gate.

## Source and boundary

| Actual mathematical source | SHA-256 |
| --- | --- |
| `NLA/IE05/ExactCertificates.lean` | `5ee8f9bc7bc79b4e0e80b85c81952ae32689661dac405edd1559f92d6eb643af` |
| `NLA/IE05/IntegerQR.lean` | `fc87524d6aceddf208722daa33c855384e772425d54fd654f5f531250c67cc44` |
| `NLA/IE05/Scaling.lean` | `0422f5ca2ac3cccf1f18a90e64aba5f9ead6f650d830e8813aa07e1541eeb3f5` |
| `NLA/IE05/QR.lean` | `cb9e1d6d91f5e194cd2c50e2f0ae9efc3ebcb55f005078038b6c1d20747fe127` |

The Definitions hash remains
`aa9a18994bb8d1889af8b30290cb71846af5424436d720afaf15a54184164dfa`;
Challenge remains
`0ccd5424f990587b1bb7170c674cba4645d9427286c916e2e19387234ccf250e`.
All **733 frozen inputs** and the existing proof gate are unchanged. The exact
1,210-file stable scope additionally preserves every prior GEPP/LU/QR handoff
input, the sealed 54-file certificate-fix diagnostic, and all root
ExactCertificates/IntegerQR/CertDiagnostic attempts. Every nested manifest is
retained as an ordinary bound input. The live concurrent `Witness.lean` and
`witness-development/` are deliberately outside this fixed helper scope; no
absence of later project additions is presumed.

I read both complete helper modules, the complete Scaling/QR modules, frozen
certificate headers, original executed root runner, actual root result/log
records, prior handoff metadata, and the certificate-fix diagnosis and verifier.
The installed ExactCertificates module equals the diagnostic contributor's
complete tested `PatchedCertificates.lean` byte-for-byte. The preserved
root-authored `ROOT-NOTE.json` has SHA-256
`253a215374601297c216bf1d5afa529771c1d78a6d6bf137ff9e468406545003`.
Its removed live CertDiagnostic file equals the retained failed experiment
snapshot by the recorded hash. No current inspected module imports that
diagnostic, Challenge or Witness.

## Actual fresh check and trust

`attempt-eod4mx91` compiled, in order, **Definitions, Scaling, QR, IntegerQR,
ExactCertificates, then a separate admission-free inspector**. All six commands
returned zero, with no warning or error. The initially empty private prefix,
actual command arguments, source snapshots, stdout/stderr, before/after bindings
and object identities are retained. The complete run records 47 commands:
40 before/after Git pin/cleanliness checks, the Lean version command and six
source commands. All ten exact package revisions stayed clean; only their nine
existing build directories and the pinned toolchain were reused read-only.
Cli has no compiled object directory and was not built. No Lake build, download,
cache copy, old target-object import or shared-cache write occurred.

The actual toolchain is Lean **4.33.1**, native macOS arm64, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; the Lean binary SHA-256 is
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.
This is local helper source elaboration, not authoritative Linux verification.

The inspector uses ordinary Prop definitions extracted from the three frozen
Challenge headers, without importing or admitting a reference theorem. Actual
elaborated type equality passed for all three certificates. A separately
supplied generic type also matches `normalizedQRQ_of_gram_lu`. Source-header
comparison alone is not counted as the elaborated type check.

The four theorem roots have an actual **34-declaration project closure**, plus
the two reached core integer-equality definitions, for **36 inspected
declarations**. The inspector traverses declaration types and bodies and checks
every reached declaration's transitive axioms. It rejects unsafe/partial
declarations, unexplained bodyless constants, forbidden axioms and dependencies
on diagnostic expected-type definitions. All **19 selected material dependencies**
are actually present.

This closure includes the two closed module-level local instances
`integerLowerZeroDecidable` and `integerTZeroDecidable`, their actual
`Int.instDecidableEq → Int.decEq` path, and all three generated kernel decision
auxiliaries:

- `integer_factor_certificates._proof_1_1`;
- `integer_factor_certificates._proof_1_2`;
- `integer_entry_certificates._proof_1_1`.

The two specialized instances are computable definitions with only `propext`
in their transitive axiom sets, inherited from the integer data definitions.
Both core integer-equality definitions are axiom-free. The pinned source shows
the recursive logical implementation of `Int.decEq` and the `doKernel` /
`mkAuxLemma` path used by `decide +kernel`. Its executable override adds no
native-execution premise to these proof terms. The actual printed instance
bodies and source snapshots are retained; the instances are not surrogates for
the certificate assertions.

All **20 source LeanCert kernel assertions** and **8 additional inspector
assertions** passed. The 28 printed reports comprise 24 standard-three reports,
two `propext`-only reports, and two axiom-free reports. No `sorryAx`, custom axiom
or native-execution axiom supports the successful helpers. No numerical square
root, interval subdivision or artificial certificate was introduced: the
finite certificates use actual exact integer data, and the QR bridge uses
generic symbolic square-root identities.

## APIs available to the assembly

All four completed names have prefix `NLA.IE05._proved.`:

- `integer_factor_certificates`: for both Boolean data choices, the exact Gram
  identity, LU factorization, unit-lower/upper structure, multiplier bound,
  positive upper diagonal and positive Gram diagonal. This is exactly frozen
  Challenge contract 9.
- `integer_entry_certificates`: the 64 witness input inequalities, retained
  witness last diagonal, candidate entry/diagonal identity, all 204 admissible
  active candidate tail inequalities, and witness final tail pivot. This is
  exactly frozen contract 10, with the original constants and actual tail product.
- `numerical_gap_positive`: the real rational equality and positivity of
  `117335164 / 1147041`, exactly frozen contract 14.
- `normalizedQRQ_of_gram_lu`: the following generic identification, with no
  dimension restriction, extra certificate or assumed QR conclusion:

```lean
{n : ℕ} (L H T : Mat n) (d : Fin n → ℝ)
(hd : ∀ j, 0 < d j)
(hGram : H.transpose * H = Matrix.diagonal d)
(hLU : H = L * T)
(hT : UpperTriangular T)
(hTp : ∀ i, 0 < T i i) :
normalizedQRQ L = scaledColumns H d
```

The generic helper proves that the triangular factor is invertible with positive
inverse diagonal, constructs the positive-diagonal QR factorization using
`diagonal (sqrt ∘ d) * T⁻¹`, and invokes the existing actual QR uniqueness and
Gram-normalization results. Integer-to-real transport, canonical identification,
witness paths, growth bounds and the supremum conclusion remain assembly work.
This helper record does not count those later conclusions as proved.

## Historical diagnostics, cleanup and sealing

All **13 root attempts** remain intact: eight ExactCertificates attempts, two
IntegerQR attempts and three CertDiagnostic experiments. Three returned success:
the two final proof helpers and one earlier unimported diagnostic. Ten failed.
The original failed logs can contain automatic recovery `sorryAx` reports; those
are explicitly failed development records, not accepted theorem evidence. The
diagnostic contributor's three attempts, including the failed tactic-local
instance experiment and the successful final two-instance fix, remain inside
its unchanged 54-file seal. No old mutating runner or audit was rerun.

Root delegated cleanup only for ExactCertificates, IntegerQR and CertDiagnostic
prefixes. For each of their 13 exact recorded paths I checked every actual file
against that attempt's retained `inputs.json` / complete `objects.json`, rejected
symlinks or unexpected objects, then removed the matching prefix. **20 root
objects** were removed; no other prefix was touched. The **12 objects** produced
by my own successful fresh run were likewise hashed and removed. Raw historical
sources, logs, executed scripts and object records were retained. Two missing
historical filename guesses are recorded as navigation errors; no compilation
or audit failed in this fresh completion task.

The evidence directory contains the actual closure/axiom records, type
extraction, full source/command snapshots, root-attempt audit, exact cleanup
receipts and a complete outer seal. The seal binds the entire fixed input scope,
this report and every file in `verification/certificates-qr-handoff/`, including
the unchanged root note, excluding only its **exact own outer manifest path**.
The read-only verifier checks those hashes and memberships without a Lean build:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  verification/certificates-qr-handoff/verify_handoff.py
```

No formalization metadata, canonical status, Git state or final-proof gate was
created or changed by this helper completion.
