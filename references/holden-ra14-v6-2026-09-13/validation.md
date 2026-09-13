# Validation — 13 September 2026

- Independent informal mathematical review: new v6 restricted and distribution-specific results passed; full RA-14 resolution did not pass. All 45 new tests and independent supplemental algebra checks passed; see independent-review.md for runtime and limitations. No Lean verification.
- Original package manifest: all 39 listed payload hashes passed. Original archive SHA-256 recorded separately. Every extracted archive file is retained byte-for-byte.
- `python3 tools/validate_problem_ids.py --base-ref origin/main`: 217 permanent IDs passed.
- `python3 tools/update_catalog.py --base-ref origin/main`: passed; no generated index or count changes. Status remains Partially resolved.
- `python3 -m unittest discover -s tests -p 'test_problem_ids.py' -v`: all 17 tests passed.
- `python3 tools/format_math.py --check`: passed, zero pages need formatting.
- `python3 tools/render_problems.py RA-14`: passed using PDF renderer dependencies; canonical TeX and PDF regenerated.
- Attributed report compiled with PDFLaTeX until cross-references stabilized, with no undefined references or overfull boxes. Its 21 pages and the 3 canonical problem pages were rendered with Poppler and visually inspected for layout; no clipping or overlap found.
- `git diff --check`: passed for edited text. Original package payloads preserve submitted CSV line endings and output logs.

The new report source is mathematically identical to the reviewed source. Changes are limited to authorship, affiliation, date, PDF author metadata, title spacing, relative prior-directory references and the factual review notice. No existing target, ID, path or prior credit was changed.
