# Recorded exact checks

The JSON files here record successful runs of the exact verifiers. The mathematical acceptance criteria are implemented in the source programs; the programs do not trust a stored `PASS` label or a stored descriptive margin.

`local_geometry.json` records the exact ranks, stationary-density weights, and nonzero flat-tangent moment. `local_rank.json` records the modular minor check. `exact_minor.json` records the fraction-free integer determinant and modular cross-check. `quantitative_rigidity.json` retains all exact rational constants in the stability bound. `regression_tests.json` records successful valid-input checks and rejection of six deliberate corruptions.

The final archive audit runs `verify_all.py` on a fresh extraction with Python optimization enabled. That flag does not disable the explicit verification conditions.

`archive_audit/` contains the recorded combined exact-check logs and a separate summary of the numerical-data audit.
