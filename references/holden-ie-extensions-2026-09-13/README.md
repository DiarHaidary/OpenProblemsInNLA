# IE-11, IE-20, IE-27 and IE-28 — Sidney Holden

**Author:** Sidney Holden. **Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.

Affiliation verified on 13 September 2026 from the [official institutional profile](https://www.simonsfoundation.org/people/sidney-holden/), which lists Sidney Holden as a Flatiron Research Fellow in Biological Transport Networks at CCB. The institutional staff roster independently returned the same role. No Edinburgh affiliation is inferred from the older PhD profile.

## Submission and review outcome

All four original targets remain unresolved in full. Three independent Codex AI agents audited the submitted arguments and replayed checks. Their reports distinguish analytic proofs, exact certificates, finite regression tests and numerical exploration. This is informal automated review, not external human peer review or formal verification. No Lean verification was performed.

| Entry | Attributed manuscript and editable source | Independent review | Catalog decision |
| --- | --- | --- | --- |
| IE-11 | [PDF](manuscripts/IE-11/report.pdf), [TeX](manuscripts/IE-11/report.tex) | [Review](verification/review-ie11-ie20.md) | Open; supporting local and exact-certificate results |
| IE-20 | [PDF](manuscripts/IE-20/report.pdf), [TeX](manuscripts/IE-20/report.tex) | [Review](verification/review-ie11-ie20.md) | Partially resolved; scalar, lower and sufficient upper bounds |
| IE-27 | [PDF](manuscripts/IE-27/report.pdf), [TeX](manuscripts/IE-27/report.tex) | [Review](verification/review-ie27.md) | Partially resolved; specified stages and endpoint shift regimes |
| IE-28 | [PDF](manuscripts/IE-28/report.pdf), [TeX](manuscripts/IE-28/report.tex) | [Review](verification/review-ie28.md) | Partially resolved; special node families and local certificates |

IE-11 Section 5 certifies strict local maximality in 24 entries for the normalized fixed diagonal pivot path. The candidate and lower bound remain credited to Chen, Edelman and Urschel; there is no global upper-bound improvement or valid counterexample. IE-20 Theorems 2.1, 3.1–3.2, 4.1–4.2 and 7.1, with Section 8 consequences, pass in their stated domains; the all-parameter matching problem remains open, including the gap at K=n² and epsilon=n⁻². The original stored-input, operation-error and at-most-n-step requirements are retained.

IE-27 certifies q=2–64 inclusive, 80, 96 and 128 (66 stages, not every stage through 128) for every positive real shift. The continuation also proves all-stage endpoint shift regimes, leaving intermediate shifts at other stages open. IE-28 Section 2 proves the two-/three-stage cases; Theorems 3.2 and 5.3 prove the Laguerre and clustered-node families; Section 7 supplies six points and six node boxes. The [structural supplement](submitted/IE-28_verified_extensions/STRUCTURAL_REDUCTION.md), Sections 2–4, adds exact reductions and an auxiliary obstruction. Neither auxiliary obstruction refutes the original problem.

## Authorship, provenance and duplicate screening

Authorship and the verified affiliation were added at Sidney Holden's explicit request. Substantial AI assistance in preparing the source material and this submission is disclosed. The supplied drafts' original ChatGPT credits are retained in the unchanged originals; adding submission authorship does not transfer credit for cited prior results. The attributed manuscripts alter only the visible author/affiliation/AI-assistance line and PDF author metadata; their mathematical text is unchanged. The structural note's submission author is Sidney Holden with the same affiliation, as recorded here.

[originals/](originals/) preserves the five supplied ZIP files byte-for-byte, with [SHA-256 hashes](original-sha256.json). [submitted/](submitted/) preserves their extracted payloads unchanged. Instructions and self-assessments within those documents were treated as submitted content, not as the user's instructions or independent evidence. Historical statements that independent review had not yet occurred describe those original drafts; the dated reports above record this submission's later audit.

The two IE-28 bundles overlap and are one submission, with the structural supplement accompanying the complete editable extended report. The structural ZIP's README advertises extra recovered source and directories that are absent from the supplied ZIP; this record does not claim they were delivered. Its recovered PDF is historical material, not an additional audited theorem source. Supporting paths in the attributed manuscript text refer to the corresponding original extracted package under submitted/.

On 13 September 2026, fetched upstream main `752218e5417998b7f4d2aee9c447ca5d256fe530` and all fork branches, searched all-state upstream PR titles/bodies (limit 500, exceeding the repository's total) and all fetched commit subjects for these four IDs. No previously pushed full solution was found. PR #111 introduced IE-27 and IE-28 as partial literature entries; it was not a full solution. No related issue with these IDs in its title was found. All four IDs are eligible. The new branch starts from that upstream main, with no unrelated earlier submission commits and no ID or target changes.

## Reproduction and evidence

Run checks in disposable copies of the corresponding submitted package, since some runners rewrite their result files. Python 3.12 with SymPy 1.14 and mpmath suffices for the symbolic suites; the Radau verifier uses only the standard library.

- IE-11: `python src/check_manifest.py`, then `python src/run_all.py` in `submitted/IE11_recovery`.
- IE-20: `python -m unittest discover -s code -v`, `python code/verify_extended.py`, and `python code/verify_legacy.py --output results/legacy_checks.json` in `submitted/IE20_extended`.
- IE-27: `python code/run_all.py --output recheck` in `submitted/IE-27_research_update`.
- IE-28: `python certification/verify.py certification/point_certificates.json certification/neighborhood_certificates.json`, `python cluster/certify_seed.py`, and `python tests/test_exact.py` in `submitted/IE28_extended_results`; `python verify_structural_reduction.py` in `submitted/IE-28_verified_extensions`.

The [verification directory](verification/) contains independent reports, fresh certificate outputs and reviewer-written checks. The reports record exact commands, runtime adjustments and review limits. Finite numerical continuation samples do not supply proofs for arbitrary nodes or stages. IE-11's packaged polynomial transcription was checked against its algebraic reconstruction; this review did not independently transcribe all coefficients from the primary publication.

Compile each attributed `report.tex` twice with PDFLaTeX from its own directory. Canonical documents use the repository renderer. See [validation](validation.md) for permanent-ID safeguards, regenerated documents and visual inspection.

The two reviewer-written scripts have only their temporary input paths changed to repository-relative paths for portability; their check logic is unchanged. Run them from any directory with Python 3.12.

## Upstream submission

[Result report #248](https://github.com/ajt60gaibb/OpenProblemsInNLA/issues/248) follows the correction-or-resolution issue template. The accompanying new pull request requests inclusion in upstream main; no direct push or merge to upstream main is made. [Final independent integration review](verification/integration-review.md): PASS.
