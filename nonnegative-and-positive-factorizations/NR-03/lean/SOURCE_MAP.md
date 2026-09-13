# NR-03 source correspondence

This statement package was prepared against the immutable upstream base
`50838e37dd793830e2cecd1055cfc7e0349490f1` in
`ajt60gaibb/OpenProblemsInNLA`. Git object IDs below are the source blob IDs;
SHA-256 values are hashes of the exact file bytes obtained with `git show`.

| role | source | git blob | SHA-256 |
|---|---|---|---|
| canonical problem page | `nonnegative-and-positive-factorizations/NR-03/README.md` | `74bcb3a394dd61558b8065601dbe255b2b2aff7a` | `a699bd54bda485d843739a5448f3e1ff4d77feb8761ea8944e767000d2b3955e` |
| canonical problem TeX | `nonnegative-and-positive-factorizations/NR-03/problem.tex` | `7f0773d1608769436a08f8cf45a1a45632b2a05c` | `0d0daf158679430a6f46bf2867ee63ad321cb89f64c65807dbd4a0750a084628` |
| Holden proof | `references/holden-nr03-2026-09-13/NR03_counterexample.tex` | `b16634dd1a10b4e90c5709db0b56d25d2c7f79b4` | `26cac3ed5aa30226530bbf8562a626b6582444abcc8ef8e8e69ebde6160565a3` |
| Holden exact certificate | `references/holden-nr03-2026-09-13/data/factors_n7.json` | `bfc585597b190e78746248e5b6c41dab938a74ce` | `fa515775f9c77e5dfe85109125d3f730c4b36684894730096247cd67fcc60bb9` |
| Holden source README | `references/holden-nr03-2026-09-13/README.md` | `856f7dd7302ee2fec95d5dad8a6f7b653ef2f959` | `d622b1dc313b62db9b17ae840b240b4d8f78196f72094e2ee644d914b64fae97` |
| Holden proof notes | `references/holden-nr03-2026-09-13/PROOF.md` | `506d56c42ae8e2d53ddda574b2c17a57391d53c0` | `5221b0064fc97486f2a1cf438bfc7278f7747bf3e3505ddbea26351e5818b067` |
| retained Colbrook partial proof | `references/colbrook-factorization-2026-09-11/manuscripts/NR-03_n3_exact_rank.tex` | `e1efd9af446caee92ba7984ac1e2a4da1bab9a90` | `d218517c99168ef7ce59fa666ce93b0b0a9cd2ccf5533d2c2caa8bb2eca7efe6` |

The mathematical author of the complete counterexample is Sidney Holden,
whose source gives the Flatiron Institute / Simons Foundation affiliation.
The formalization author is George Stepaniants with the Caltech CMS
affiliation recorded in `formalization.yaml`; no email address is included.

## Target fidelity

The source target quantifies every `n ≥ 3` and every Boolean row and column.
The Lean target uses `Fin n → Bool` directly, so it does not silently replace
the matrix by masks, a restricted submatrix, or truncated natural subtraction.
The n = 7 contract has 128 rows and columns and 127 factor atoms. It asserts
the source-scaled identity over `ℝ` for all index pairs and requires positive
integer denominators. Dividing those denominators is a separately named
bridge to genuine real nonnegative factors.

The retained JSON and TeX are source inputs and audit material. They are not
imported as Lean axioms or accepted as a trusted checker result.


## Modular candidate packaging

At canonical commit `523c5aeaddd8bf7c2dc01afb053bb0dea8811335`,
the candidate contained 58 active implementation modules copied
byte-identically from `development/NR03` at commit
`3b3eb8f3fa384e4b3bf640d48bca87cf40db9565`. That commit includes the reviewed
certificate-bridge overlay on `fe4140cced3fc4b4efdd4ef4e202d27156a1cd4f`;
individual source hashes are in `ACTIVE-MODULE-MANIFEST.json`.

The bridge-only Linux diagnostic passed for its six lightweight modules,
including LeanCert support. Its receipt is in `reviews/bridge-diagnostic/`.
The full 58-module graph, ten public exports, Comparator/default-kernel replay,
and canonical sandbox/rejection controls passed in canonical run 34785341662
at candidate commit `f664d07e82aaa60bc9c78dd1946e763168c5c530`. The development driver, row generator, historical
probes, optional drafts, and diagnostic records remain provenance material and are
not imported by the canonical Lean proof. The earlier bridge-only result and failed
Rank run are retained as historical receipts; the terminal acceptance evidence is
bound by the raw-evidence hash `e7bd039fb9e4dcc7f46a4930b9f4dc2eb79a9977a80c0cbb4299d8edcb4eb0ed`.


## Statement-preserving canonical Rank cast repair

After canonical run 34783909558 reported a cast elaboration error, the current
Rank.lean inserts only `change (0 : ℝ) ≤ (W i k : ℝ)` before the existing
left-factor nonnegativity tactic. The target is definitionally unchanged.
`reviews/rank-cast-repair/` retains the exact old/new hashes, diff, and two
independent source-delta approvals. All other 57 active modules, every frozen
statement and all pins remain unchanged from the preceding package. Full canonical acceptance is recorded below in run 34785341662 at the
candidate commit `f664d07e82aaa60bc9c78dd1946e763168c5c530`.

## Canonical verification acceptance

The repaired 58-module package passed the complete canonical Linux verification in
run 34785341662 (job 103799711659) at commit `f664d07e82aaa60bc9c78dd1946e763168c5c530`.
The run covered the full row graph, all ten public exports, LeanCert kernel trust
assertions, the default kernel, Comparator identity and the recorded sandbox and
negative controls. The public run is [the canonical evidence](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34785341662);
the artifact digest is `91f80abcbbb0f10fbf614ab259fbf5121a8dabd5c600969a260e3b8b2c8e267c` and the retained raw
evidence digest is `e7bd039fb9e4dcc7f46a4930b9f4dc2eb79a9977a80c0cbb4299d8edcb4eb0ed`.

Per-export axiom lists and final review identities are recorded in the accepted
formalization metadata. This section does not replace the historical bridge or
failed-run receipts above.
