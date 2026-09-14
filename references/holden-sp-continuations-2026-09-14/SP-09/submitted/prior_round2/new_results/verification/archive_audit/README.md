# Recorded extraction audit

The eight exact-check logs were produced by `python -O verify_all.py` on a clean extracted copy of the included proof files. The `all_checks.json` summary records successful return codes and elapsed execution times. No mathematical check is disabled by Python optimization.

The separate `experiments.json` summary audits the saved numerical constructions, including reconstruction of the two initially improved witnesses in the base dimension itself. It is not a lower-bound certificate and is not used in the proofs.

The delivered ZIP was also re-extracted after these records were added, and its file hashes and all proof-critical programs were checked again. The verifiers recompute acceptance conditions rather than trusting these logs.
