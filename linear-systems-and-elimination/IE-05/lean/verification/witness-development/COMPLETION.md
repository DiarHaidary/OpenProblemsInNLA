# IE-05 Witness helper: author completion

Date: 13 September 2026. This is scoped implementation evidence, not an independent mathematical review, a complete IE-05 formalization, or an authoritative Linux Comparator result.

George Stepaniants, Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. The original conjecture is attributed to John Peca-Medlin in the preserved source. Stepaniants's submitted counterexample and its exact integer data remain attributed to their original sources. The `formal_review_standards` AI agent wrote this helper after the accepted statement gate; it also contributed the statements, Pivot/GEPP/LU helpers, and the exact-certificate decidability fix. The coordinator authored the separate QR, scaling and integer-QR helpers. These implementation roles are not additional referee approvals.

## Result and exact scope

`NLA/IE05/Witness.lean` is complete and frozen at SHA256 `4fa2cfeef00d80f28475bf221082a786f2b035f1e77e47b1bfd70bc13f2e57b6`. It proves the two unchanged Challenge contracts under `NLA.IE05._proved`:

- `canonical_integer_identification`: `candidateQ 8 = normalizedInteger false` and the actual first-available scan path of that canonical QR matrix is `noSwapPath 8`.
- `witness_orthogonal_path`: the actual real `witnessQ` is orthogonal, its actual scan path is `noSwapPath 8`, that path is first-available at every pivot, and it is admissible.

Neither theorem introduces assumptions. The proof imports the actual QR, scaled-LU and integer-certificate implementations, and does not import Challenge. The expected types in the inspector are Prop-valued definitions copied exactly from the frozen headers, without reference proofs or admissions. Lean's actual type comparison checked both exports.

The new file contains fifteen ordinary theorem declarations. Its supporting interfaces include genuine integer-to-real matrix multiplication, transpose, diagonal and tail-product casts; unit-lower/upper/absolute-value transfers; `real_factor_certificates`; `normalizedInteger_orthogonal`; `normalizedInteger_path_trajectory`; `normalizedInteger_trajectory_entry`; `normalizedInteger_firstGrowth`; and `integerLower_false_prescribed`.

`normalizedInteger_path_trajectory b` holds for both Boolean data sets. It proves first-available path correctness, equality with the implemented scan, and the entire actual trajectory for every natural `k ≤ 8`, including its zero terminal stage. The scalar-entry helper expresses each entry as the corresponding integer tail-product entry divided by the positive column square root. No desired trajectory or nonsingularity fact is assumed in place of the proved generic bridge.

## Mathematical and computational route

The seven-part integer factor certificate is transported through the real cast, with finite sums and products justified by exact cast lemmas. The real Gram identity and positivity feed the existing scaled-column orthogonality theorem. The actual real factorization, triangularity, lower-entry bound and positive diagonal/scales feed the existing universal scaled-LU trajectory theorem. First-available pivot correctness implies admissibility directly.

For the canonical candidate, its integer lower factor equals the prescribed `L₈` by the defining index cases; this does not add a 64-entry numerical QR check. The genuine normalized-Gram–Schmidt definition is identified with the scaled integer columns using the coordinator's `normalizedQRQ_of_gram_lu`, which in turn uses positive-diagonal QR uniqueness. Thus the canonical matrix is not defined by its desired integer formula.

All new arguments are exact. No numerical interval or new finite entry certificate is needed here. The existing integer certificates are re-elaborated in the final check and their actual `of_decide_eq_true`/integer-equality consumers occur in the inspected dependency graph. LeanCert is used for explicit kernel trust checking, without native execution trust.

## Actual final validation

The selected immutable attempt is `attempt-wo2xjo06`; its `result.json` has SHA256 `e3cd33e82f3fa937d2afadc347f117a3668d8681c0fb842a85ff947a32178241`. All nine direct-source commands passed in a new empty private output prefix, with no reused project objects and no warnings. The measured sum of command times is 43.111243207065854 seconds on macOS 14.6.1 arm64, Lean 4.33.1, core commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.

The commands compile Definitions, Scaling, QR, IntegerQR, Pivot, LUTrajectory, ExactCertificates, Witness, and the inspector. Across those commands, 60 explicit LeanCert kernel assertions and matching standard-three axiom reports pass; 26 are in Witness and its inspector, and 34 recheck imported helper assertions. The inspector explicitly audits all fifteen new roots, reaches 93 actual project declarations, and verifies 56 named dependencies in their actual type/body graph. It rejects unsafe/partial project declarations, unexplained bodyless declarations, reference-type dependencies, an incomplete traversal, `sorryAx`, native/compiler trust, and every transitive axiom outside `propext`, `Classical.choice`, `Quot.sound`.

The transpose cast theorem is a separately checked `rfl` root. Its named rewrite is definitionally erased from downstream terms, so the final report does not claim that this name survives as a downstream dependency. Every retained-dependency claim is supported by the actual successful inspection log.

The final command was:

```
python3 verification/witness-development/compile.py --fresh --inspect
```

The runner uses the ten pinned source dependencies in the existing shared MI-22 checkout, with nine existing read-only Lean object directories. `Cli` has no built directory and is not imported. No Lake invocation, cache copy, dependency download, or shared build/Git mutation occurs. Earlier bounded development reused only this helper's own source- and object-hash-verified immutable imports; the final check rebuilt all nine project/inspection modules. Both owned output prefixes were hashed and removed, recording 16 development objects and 18 final objects. Their sources and logs remain preserved; no absent failed-module object is claimed to have existed.

## Retained failures and diagnostic corrections

- A Python runner preflight syntax error occurred before any Lean command. Its original source and the correction receipt are retained separately.
- `attempt-fki_xyit`: all seven imports passed; Witness failed only because a generic integer tail-product expression needed an explicit inner `ℤ` annotation before its real cast. One unused simplifier argument was also removed. Both final target proofs had already checked, but no complete Witness success was claimed at that attempt.
- `attempt-6dcjp1tp`: Witness passed with zero warnings after the local correction. Its mathematical bytes equal the final frozen source.
- `attempt-s2dd7fzt`: Witness passed; the first dependency inspector incorrectly expected the name of the definitionally trivial transpose cast to survive downstream.
- `attempt-ruj_u531`: the diagnostic was made to collect all missing dependencies at once. It confirmed that the transpose name was the only absent expected name. No mathematical source changed.
- `attempt-wo2xjo06`: the unsupported named-dependency expectation alone was removed; all fifteen roots remain audited. The complete fresh check then passed.

All five attempts, copied source inputs, actual commands and complete logs are retained. The exact type comparison and all mathematical implementation bytes were not weakened to satisfy the diagnostic.

## Preservation and limits

`audit_result.py` rechecks all 733 statement-freeze inputs, the 27 original source snapshots against their immutable Git blobs, all six fixed imported helper hashes, ten clean source pins, final input/log hashes, and the complete existing GEPP, LU, QR/scaling and exact-certificate diagnostic seals. Their manifest inventories contain 150, 68, 847 and 54 bound files respectively; those overlapping inventories are not claimed to be disjoint. The local audit writes only this scope's `audit-result.json`.

The seal covers Witness, its own complete evidence, and explicitly listed immutable boundaries. It deliberately excludes concurrently developed GrowthBounds/Growth files. No frozen statement, source target, prior seal, canonical metadata, problem identifier, Git branch or publication state was changed. Remaining complete-project proof work, two independent final mathematical reviews and actual authoritative Linux verification belong to later stages. The read-only `verify_seal.py` checks this handoff without rebuilding Lean or rewriting the audit result.
