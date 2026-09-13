# PR #249: independent provenance audit

Reviewed head `9e11821e2e999afb1699272005a167da7ee42861` read-only in `/private/tmp/nla-audit-249`. **No actionable provenance finding.**

All five original ZIPs match the SHA-256 values recorded in `original-sha256.json`. Reading the ZIP members also checked their CRCs. Their 240 extracted file payloads are byte-for-byte identical to all 240 tracked files under `submitted/`, with no missing, altered or additional tracked payloads:

| Original ZIP | Files matched |
|---|---:|
| IE11_recovered_work.zip | 37 |
| IE20_extended_results.zip | 25 |
| IE28_extended_results.zip | 50 |
| IE-28_verified_extensions.zip | 9 |
| IE-27_research_update.zip | 119 |

All seven manifests present in the extracted packages match their delivered files (340 manifest entries, including repeated nested-package entries). The original ZIPs' identities are checked against the committed recorded hashes; this task did not obtain a separate authenticated copy of the original user attachments.

For each of the four attributed manuscripts, I first inspected the full unified diff and then required equality after exactly two enumerated substitutions in the original source: PDF author metadata and the visible author/affiliation/AI-assistance block. Those exact transformations reproduce the attributed TeX byte-for-byte. All mathematical text, theorem statements, proof text, citations and supporting-path references are unchanged. IE-11's copied `candidate_matrix.tex` and `multiplier_table.tex` are also byte-identical. PDF rendering and theorem correctness are covered by the separate subject reviews.

Archive safety checks cover all top-level ZIP members and the one nested IE-20 ZIP (17 historical files). No absolute/traversal/Windows-drive/backslash paths, duplicate or case-colliding paths, symlinks, nonregular objects, encryption or excessive expansion were found. Maximum member expansion ratio was 16.9; largest package unpacked size was about 2.75 MB. No extraction or submitted-code execution was needed for this audit.

Static inspection parsed all 50 Python source files across the five archives and nested archive. I inspected all detected subprocess call sites: they call local Python verification programs or PDFLaTeX using argument lists. No destructive deletion commands, network access, executable dynamic evaluation, unsafe archive extraction, TeX shell escapes or arbitrary-output TeX operations were found. Verification runners do intentionally regenerate local result files, and the PDF builders intentionally copy the rebuilt PDF over the package-local PDF after compiling in a temporary directory. The submission README correctly tells readers to reproduce in disposable copies. This is a source inspection, not a general sandbox guarantee.

The IE-28 structural ZIP contains only nine files. Its `recovered_work/` contains a historical `report.pdf` without the advertised editable recovery source, and the advertised `continued_work/` and `additional_checks/` directories are absent. The reference README explicitly discloses these omissions and does not treat that historical PDF as an additional audited theorem source. The independently complete IE-28 extended package provides the editable report and reviewed proofs. No undisclosed missing committed payload was found.

Six ignored Python bytecode files already present in the audit worktree are not ZIP payloads or tracked PR additions. They are listed separately in the JSON. This auditor created no files in the source worktree; tracked `git status --short` remained clean.

Reproduction and evidence:

- Script: `/private/tmp/nla-249-provenance.py`
- Complete machine-readable archive-member hashes and checks: `/private/tmp/nla-249-provenance.json`
- All four attribution diffs: `/private/tmp/nla-249-provenance-attribution.diff`
- Command: `/private/tmp/nla-batch-python/bin/python /private/tmp/nla-249-provenance.py`

No source or GitHub mutations were performed. This report addresses provenance and archive safety only; the other reviewers own the mathematical claims and integration decision.
