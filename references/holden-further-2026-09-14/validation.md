# Validation record — 14 September 2026

## Mathematical and publication review

Three separate Codex AI reviewers passed the scopes recorded in the five linked reports. Only RA-05 passes the complete original target; TR-03, RA-11, SP-10 and RA-14 remain Partially resolved. The reviewers also checked final canonical/archive notices and publication-source integrity. This is informal automated review, not external human peer review or formal verification. No Lean verification was performed.

Fresh finite checks and exclusions are recorded in each independent report: RA-05 exact cubic certificate; TR-03 16 check groups; RA-11 exact diagonal/interpolation and floating moment-grid checks; SP-10 16 tests and 524 complement witnesses; RA-14 24 tests and the exact rank certificate. Optional unavailable suites are not represented as rerun, and inherited proofs are outside the fresh audit except RA-05's explicitly reviewed complete Part II.

## Repository and provenance checks

- `python3 tools/validate_problem_ids.py --base-ref origin/main`: PASS, 217 IDs.
- `python3 tools/validate_problem_ids.py --base-ref upstream/main`: PASS, 217 IDs.
- `python3 tools/update_catalog.py --base-ref origin/main`: PASS. Final counts: 43 Open, 72 Partially resolved, 72 Solved, 30 Lean verified. The open count decreases by exactly one, from 116 to 115.
- `python3 -m unittest discover -s tests -p 'test_problem_ids.py' -v`: all 17 tests PASS.
- `python3 tools/format_math.py --check`: PASS, no pages need formatting.
- Renderer tests were run with `PANDOC` set to the available executable; all tests PASS. The renderer adjustment only removes obsolete forced reference-page breaks for RA-11 and RA-14.
- All 122 files in the five `submitted/` snapshots match their ZIP manifest hashes; no extra generated files occur inside those snapshots.
- Original canonical page content, apart from dated metadata and RA-05's status, is retained in order. Permanent registry mappings are unchanged. RA-01 is untouched and its identical source hash is recorded in `eligibility.json`.
- New publication/review Markdown links resolve locally. Original archive contents remain documentary snapshots and may contain historical paths or links.

## PDF preparation and visual inspection

All five attributed manuscripts and five affected canonical problem documents were rebuilt. Manuscript PDF metadata credits Sidney Holden. Author and verified affiliation appear in the publication copies, alongside dated review dispositions and assistance disclosures. URL and literal-filename wrapping prevents margin overflow; no mathematical body was rewritten. RA-14's included historical verification summary is inlined unchanged into its exported standalone TeX.

Every page of the final PDFs was rendered with Poppler and visually inspected in contact sheets, with separate full-size cover/title inspections for RA-05. No clipping, overlap or missing glyphs was observed. Awkward forced page breaks in canonical RA-11 and RA-14 and the RA-14 manuscript contents were corrected and the affected outputs rechecked. RA-05's combined PDF exactly concatenates its 17-page Part I and 27-page Part II publication copies; its original package PDF and bridge remain intact in the snapshot.

The supplied files' historical statements about pending review or unreviewed earlier material remain unchanged in the archive. Current disposition is given by the dated front matter, independent reports and canonical entries.
