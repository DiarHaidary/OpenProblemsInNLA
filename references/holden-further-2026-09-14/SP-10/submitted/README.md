# SP-10 fourth-continuation delivery

**Not a complete solution.** The arbitrary-graph inequality remains unproved and undisproved by this package.

Read `report/REPORT.md` for the self-contained polynomial and support-obstruction proofs and the degree-four bipartite theorem. The proof dependencies are stated at the start. These results must not be promoted to a solved status for SP-10.

## Reproduction

From this directory, run:

```sh
python -m unittest discover -s tests -v
python src/exact_supplement.py
```

Only Python's standard library is required for these commands. With SymPy installed, run `python src/crosscheck_sympy.py` to independently verify the saved records and exhaustive 3-by-3 pattern coverage without regenerating them. The saved result file distinguishes complement-only witnesses from full rank-pair certificates and explicitly records the expected rejection of the defective SDP pair. The optional second implementation used SymPy when installed.

`provenance/recovery.json` lists any recovered working directory from the interrupted continuation. Such files and their existing execution logs are preserved, not silently declared rerun by the supplemental tests. `prior/` retains the preceding archives when available. The third archive corrects the false degeneracy premise in the second.

The polynomial construction accepts every valid bipartite input with its specified bound; it is not a search heuristic. It supplies the complement factor. The all-order bound for both ranks uses the mathematical argument in the report, not finite enumeration.

`MANIFEST_SHA256.json` contains the hashes of all delivered files except itself. No repository was modified.
