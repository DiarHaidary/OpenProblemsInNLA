# Correction to IE-16 publication audit

**Reviewer:** `/root/lean_iv01_next` (AI agent)  
**Date:** 2026-09-13

The original conditional finding in `REVIEW.md` was based on a misread of
`reviews/FINAL-ACCEPTANCE.json`. Its `boundary_files` object contains 15
proof/configuration files and does **not** contain `formalization.yaml`.
The `3a7003...` hash is present only in the historical approved statement
boundary/provenance record. The current metadata/archive mapping is therefore
not in conflict with the final acceptance boundary, and no verifier change is
required for that reason.

The exact offline publication check was run from the Lean project directory:

```text
/tmp/nla-lean-formalization/venv/bin/python -B verification/verify_publication.py
```

It exited 0 with:

```text
Manifest schema and comparator coverage: PASS (15 declarations)
IE-16 publication integrity PASS: 281 original inputs, 15 exports, immutable ZIP/raw receipts, standard axioms and final review hashes
```

This command used the existing Python verifier only; no Lean/Lake invocation,
network access, or source modification occurred. **Final disposition: PASS.**
