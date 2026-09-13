# IE-16 publication audit

**Reviewer:** `/root/lean_iv01_next` (AI agent)  
**Date:** 2026-09-13  
**Scope:** independent publication audit of the current IE-16 canonical README, `RESOLVED.md` entry, Lean guide, `formalization.yaml`, archived metadata map, final acceptance records, raw canonical receipts, links and rendered PDF. This is not an additional mathematical proof referee report. I made no proof-source edits and ran no local Lean or Lake command.

## Verdict

**CONDITIONAL PASS.** The publication content is accurate and ready after one offline-integrity verifier correction described below. The mathematical/configuration files at the accepted canonical revision remain hash-bound, and the current metadata correctly credits George Stepaniants with the Department of Computing and Mathematical Sciences, California Institute of Technology, Pasadena, California, USA. No email address is published. Sidney Holden remains credited for the mathematical resolution and exact certificate.

## Checks

- `697a2a1d88337a6747aa5c82fb6e554d3ff1b356`, run `34774629327`, job `103770408910` and artifact `10322764134` agree across the final acceptance JSON, raw receipts and Linux evidence. The raw `result.json` contains 281 input hashes; current files and the two archived metadata mappings match those hashes.
- The current `formalization.yaml` parses, declares George’s affiliation, has 15 `main_results`, and sets `whole_problem_verified: true`. The current `comparator.json` has the same 15 exports and no definition exports. The final acceptance boundary hashes match all current mathematical/configuration files; its approved statement `formalization.yaml` bytes are retained at the documented transition/review paths. The target correction is recorded separately and the canonical result uses its current hash.
- The raw Comparator log has the recorded SHA-256 and 15 closures, each exactly `propext`, `Classical.choice`, and `Quot.sound`; it contains the default-kernel acceptance marker and successful exit. Sandbox, kernel, Comparator-regression, sorry and native-decide controls have the expected terminal outcomes. The two negative fixtures fail by illegal-axiom detection, as intended.
- I checked 39 relative links in the canonical problem README, Lean guide, Linux evidence README and the IE-16 section of `RESOLVED.md`. All resolve against the current files or tracked Git `HEAD`. Three reference payloads are omitted only by this sparse checkout; their paths are tracked in Git and are valid repository links. The immutable proof, LeanCert, Mathlib, action, evidence, review and reproduction links use the intended revisions/paths.
- The current two-page `problem.pdf` contains the Lean-verified status, formalizer affiliation, Holden attribution and retained original target. `render-final.log` reports `IE-16: OK`; visual inspection of both pages found no clipping, missing characters or broken section flow. The original problem begins intact on page 2.
- Current publication-facing files contain no stale `pending` status. Dated historical candidate metadata and the 2026-09-08 historical status check are clearly labeled as history and do not alter the final status.

## Required correction

`verification/verify_publication.py` currently executes:

```python
for name, expected in acceptance['boundary_files'].items():
    assert digest(local(PROJECT, name)) == expected, name
```

The final acceptance’s `formalization.yaml` boundary hash is `3a7003db...`, the pre-canonical approved statement file retained under `verification/candidate-presentation-transition/before/formalization.yaml`. The current publication metadata has hash `729eb668...`; the canonical raw result maps its accepted candidate input to `verification/candidate-metadata/formalization.yaml`, hash `1b88c997...`. Therefore the verifier will fail at this loop after `package-inputs.json` is added, even though the metadata transition is intentional and documented.

Before committing the publication package, make the verifier compare this acceptance boundary through its retained historical path (or an explicit boundary-path map), keep the current metadata/raw-input map check separate, generate the complete `verification/package-inputs.json`, and rerun the offline verifier in the pinned environment. Do not change the accepted proof or approved target boundary.

## Evidence hashes

- Current Lean guide: `639a56c4994e667923c871439c901972dd565977ab7c4238d25d2cb907f1b09a`
- Current `formalization.yaml`: `729eb6681f6e7a6b9b35a53cbd8fd90a25e4aaaef4591f155b9c7bb7dd6fd0ea`
- Archived candidate `formalization.yaml`: `1b88c99711031a42d4c7c4bff3a5e7dd064f42d1b6c215ade9d64d96d25c3335`
- Approved statement `formalization.yaml`: `3a7003dbd9010ee1ed0f8be032e7265815405ebf706a66effbe801a884c2a2f4`
- Raw `result.json`: `3fa4b80021abb07a0df3921d33e1bd3c16d07df732578453bf312250f06fc9dd`
- Raw `comparator.log`: `f226bbdaf0c47e4dff3127d1711b00819ccf0e7d275b320521191e2fc0087d9f`
- Final acceptance JSON: `2eeff0e54ee9a1f8fd9e690c4bb2aaf446c9d0433e0fd719dc65684899510703`
- Final PDF: `07df1fa761d9cf55e7f50bef3ec139127ffe7c5e2bd3ea0a75bca083cbb71b6e`
