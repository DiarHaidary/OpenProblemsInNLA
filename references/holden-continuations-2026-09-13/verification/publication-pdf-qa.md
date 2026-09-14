# Independent publication PDF visual QA

Reviewer: separate Codex AI agent `/root/review_sp14`, 2026-09-14 UTC.
Scope: the five authored `report.pdf` files under `references/holden-continuations-2026-09-13/`; no mathematical re-review or artifact edits in this QA task.

All pages were rendered with Poppler at 1400-pixel long edge and inspected using 17 contact sheets. Dense content was additionally inspected as full-page images (NR-02 p.12 table, MI-20 p.2 displays, SP-14 p.4 equations and footer). A supplementary text bounding-box scan found no text within 14 points of either horizontal paper edge or 8 points of either vertical edge.

| Report | Pages | Visual finding |
| --- | ---: | --- |
| NR-02 | 14 | Attribution, headings, mathematics, tables and references readable; no clipping or overlap found. |
| SP-07 | 13 | Attribution, numerical certificates, matrices, tables and references readable; no clipping or overlap found. |
| MI-20 | 11 | Attribution, corrected source's displays and references readable; no clipping or overlap found. |
| SP-08 | 8 | Attribution, polynomial displays, domain table and references readable; no clipping or overlap found. |
| SP-14 | 16 | Attribution, mathematics, table and references readable; no clipping or overlap found. Initial TOC had Appendix A at p.15 while heading appeared on p.14; final convergence recheck recorded below. |

Total: 62 pages. All five title pages visibly credit Sidney Holden, Center for Computational Biology, Flatiron Institute, Simons Foundation. This QA confirms rendered wording, not an independent affiliation investigation.

SP-14 contents convergence: PASS after the submitting agent recompiled. I re-rendered and inspected the final contents page (p.2) and Appendix A heading page (p.14); both now correctly show p.14. Final verdict: all five publication PDFs pass this visual QA; no outstanding visual correction.

## Reviewed final PDF SHA-256 hashes

- MI-20: `315a134432840fdd5aa74e4dd7fd6a57f33cb68dd1fb599e52df49512dda544a`
- NR-02: `a8a6dfcad52c7f38bd8c72ff06b96e316befee27d2ab550a33e63344a3596feb`
- SP-07: `24d04ecafe4134085c93c997a1c37825aafebddf37470f7b79967f278e6b67da`
- SP-08: `24469f6b02b55ab30ce3bd331ce67ab63d8a84db02679fdfebcf69cb8dfe2f23`
- SP-14: `a28effe611fea44fa4e083bafaba2abecf4b47d63d63518694e7b5fa9f8c66a0`
