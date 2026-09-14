# RA-14 — exact capacity and adaptive innovation continuation

**Status: PARTIAL. This archive does not contain a full solution to unrestricted RA-14.**

Start with `report.pdf` and `PROOF_AUDIT.md`. The report proves an exact minimum-energy criterion for a successful rank-k subspace, including singular tail features; an exact Gaussian nodal-capacity formula and probability bound; a linear-size reduction for arbitrary adaptive queries; an innovation-count tradeoff; and an exact saturation statement for the enlarged full-prefix space.

The unrestricted lower/upper interval inherited from v5/v6 is unchanged. In particular, the package does not close the unbounded transition gap at k=1 and epsilon=(log(n)/n)^2. The linear-size reduction retains adaptive dependence; its missing probability estimate is not replaced by an independent-Gaussian assumption.

## Main files

- `report.pdf`, `report.tex`: mathematical report and editable source.
- `PROOF_AUDIT.md`, `claims.json`, `STATUS.json`: proof dependencies and exact scope.
- `src/capacity.py`, `tests/test_capacity.py`, `run_checks.py`: new component checks and diagnostics.
- `exact_rank_certificate.py`: integer-arithmetic construction and verification of a finite actual-span/full-prefix separation.
- `results/`: actual test logs, diagnostic rows, environment record, and exact nonzero-minor certificate.
- `sources/`: primary-source records and any successfully retrieved repository snapshot.
- `prior/`: original v6 ZIP and report, when present, copied unchanged.
- `MANIFEST.json`, `verify_manifest.py`: byte-integrity verification, not a proof certificate.

## Reproduction

```sh
python verify_manifest.py
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 python run_checks.py
python exact_rank_certificate.py --verify
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

The test run is described in `results/verification.json`; inspect its status rather than assuming that a test count proves the mathematics. Earlier test suites are **not claimed to have been rerun** here. Regeneration changes result bytes and requires a new manifest.

## What is not claimed

There is no new unconditional all-parameter query-complexity lower bound, no all-input algorithm matching the smaller lower scale, no equivalence between a q-query transcript and an entire multi-start degree-q prefix, no independent review, and no proof-assistant verification. Hidden singular coordinates are used only in diagnostic analysis, not supplied to an oracle algorithm for free.
