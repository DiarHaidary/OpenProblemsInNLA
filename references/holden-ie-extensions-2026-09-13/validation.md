# Submission validation — 13 September 2026

The isolated branch starts at upstream main `752218e5417998b7f4d2aee9c447ca5d256fe530`. All 217 permanent ID/path mappings are unchanged. Original mathematical target text, assumptions, quantifiers and ratings for IE-11, IE-20, IE-27 and IE-28 are unchanged; only dated supporting/partial-result notices and metadata were added.

## Repository checks

- `python3 tools/validate_problem_ids.py --base-ref origin/main`: PASS, 217 IDs.
- `python3 tools/validate_problem_ids.py --base-ref upstream/main`: PASS, 217 IDs.
- `python3 tools/update_catalog.py --base-ref origin/main`: PASS. Catalog: 43 Open, 73 Partially resolved, 73 Solved and 28 Lean verified. The active open count remains 116; IE-20 moves from Open to Partially resolved.
- `python3 -m unittest discover -s tests -p 'test_problem_ids.py' -v`: 17/17 PASS.
- `python3 tools/format_math.py --check`: PASS, zero pages requiring formatting.
- Canonical IE-11, IE-20, IE-27 and IE-28 TeX/PDF rebuilt with the repository renderer, Pandoc 3.x from the available local runtime and XeLaTeX. Each final PDF has two pages.
- Attributed manuscripts compiled twice with PDFLaTeX. Final page counts: IE-11 10, IE-20 18, IE-27 8, IE-28 13.
- All 57 pages across these eight final PDFs were rendered and visually inspected for clipping, overflow, broken equations, title/author placement and page layout. No visual defect was found.
- The original five ZIPs match their recorded SHA-256 hashes. All 240 extracted payload files match the supplied archives byte-for-byte.
- The two reviewer-written scripts pass after converting only their input paths to portable paths relative to this submission record.

Markdown's intentional two-space metadata line breaks are retained; they account for the trailing-whitespace notices from ordinary `git diff --check`. No mathematical target or numbering safeguard was weakened. The unchanged archived source material retains its original formatting and historical status statements.

## Independent mathematical review

Three separate Codex AI agents passed the precise limited scopes, with detailed reports and fresh computational evidence in [verification/](verification/). IE-11 remains Open, and IE-20/IE-27/IE-28 are Partially resolved. No result was promoted to Solved. The final integration audit additionally checked that the catalog summaries did not overstate the accepted scopes, that original statements were retained and that archive provenance was accurate.

No Lean verification was performed. Existing unrelated Lean-verified entries and artifacts were left unchanged.
