# RA-01 — Fourth-round tail analysis

**Status: partial results, not a complete resolution of unrestricted RA-01.**

The report is [paper/ra01_round4.pdf](paper/ra01_round4.pdf); the editable source is
[paper/ra01_round4.tex](paper/ra01_round4.tex).

## Results proved in the report

For the original residual-diagonal RPCholesky pivot law, with
`tau_r(A) = sum_{i>r} lambda_i(A)` and `a = lambda_{r+1}(A) > 0`:

- **C = 3** when `lambda_{r+j}(A) <= a * 2^{-(j-1)}` for every tail index.
- **C = 4** when `lambda_{r+j}(A) <= a / j^2` for every tail index.
- An explicit finite **C_p**, depending only on a fixed `p > 1`, when
  `lambda_{r+j}(A) <= a / j^p`.

In each case the conclusion is
`E trace(R_k) <= (1 + epsilon) tau_r(A)` at
`k = min(n, ceil(C r / epsilon))`, for every `0 < epsilon < 1`.
The leading eigenvalue spread and eigenvectors are unrestricted. The tail
hypotheses are essential assumptions, not properties of all PSD matrices.
In particular, a tail index here starts after rank r; a global power-law spectrum
need not satisfy the corresponding tail-normalized envelope at every rank.

Two further results clarify the remaining gap. A finite rank-one-spike family
rules out every bound `E N(t) <= a r + t tau_r(A)` with finite universal `a`.
Separately, the retained determinant-path comparison is shown to deteriorate on
a diffuse-tail diagonal family. That deterioration concerns the **upper
comparison**, not the actual algorithm, which already has a good diagonal bound.

## What is not established

No absolute uniform upper constant for arbitrary PSD inputs is proved or
refuted. The missing statement is still a constant-factor expected trace bound
after a constant multiple of r pivots, without a tail-envelope or head-spread
restriction. No repository files were changed. No independent mathematical
review or proof-assistant verification was performed. No originality claim
relative to all prior literature is made.

## Reproduction

Verify the delivered snapshot **before** regenerating outputs:

```sh
python code/verify_manifest.py
python code/verify_exact.py
# Optional, requires NumPy:
OPENBLAS_NUM_THREADS=1 python code/verify_floating.py
# Optional, requires pdflatex and the packages listed in the TeX source:
sh paper/build.sh
```

The exact program uses only the Python standard library. Its recorded run passes
8,500 explicitly counted rational checks on eight matrix cases and on scalar
coefficient, constant, rounding, clock, and saturation calculations. The JSON
separates the purposes of the checks; they are not 8,500 independent theorems.
Some small matrix tests reach the dimension cap, as recorded explicitly.

The optional numerical program exhausts two order-11 subset distributions and
runs 1,200 Monte Carlo trajectories on six further real/complex cases. These are
floating-point diagnostics, not exact certificates or substitutes for proofs.

Rebuilding the PDF or verification outputs may change timestamps or timing fields,
so their content hashes can change without any mathematical change.

## Contents

`paper/` contains the report, source, and build script. `code/` contains the
verification programs. `verification/` contains the actual executed outputs and
build log. `SOURCE_AUDIT.md` records attribution and proof dependencies.
`provenance/` preserves the third-round ZIP unchanged; its nested provenance
contains rounds two and one. Earlier results are not silently recast as new work.
