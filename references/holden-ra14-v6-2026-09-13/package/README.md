# RA-14 continuation v6

**Status: PARTIAL. The unrestricted RA-14 problem is not fully solved by this package.**

The new manuscript is `report.pdf`, with editable source `report.tex`. It gives a finite-parameter characterization of a precisely specified restricted algorithm class, an exact adaptive posterior for a shifted singular-Wishart law, and a distribution-specific rank-one algorithm showing why that law does not supply the missing linear transition lower bound. The unrestricted bounds inherited from v5 are unchanged.

## The three different statements

The public RA-14 problem concerns arbitrary measurable adaptive real-vector queries, in either oracle direction, with a pointwise success probability of at least 0.99 for every input matrix. Each individual product costs one query. No statement about a particular algorithm class or an average over one input distribution is automatically a statement about this unrestricted minimax complexity.

Write `s = sqrt(epsilon)`, `x = n/k`, and

```
F(n,k,epsilon) = (k/s) log(1 + x*s)
U(n,k,epsilon) = min(n, (k/s) log(e*x)).
```

### Restricted full-block characterization — Theorem 2.2

For the deterministic-width, full-block span-query class of Definition 2.1,

```
exp(-48) U <= q_fb <= min(n, ceil(24000 (k/s) log(e*n/k))).
```

The width is chosen deterministically before the input is queried. Every round is charged its whole width; query vectors belong to the initial span and earlier replies, and there is no within-round adaptation. The output itself may be arbitrary and need not belong to that span. Fresh directions, selectively charged updates, randomized widths, and changing widths are not included.

The proof therefore establishes `q_fb = Theta(U)` for all finite parameters, not `q_sp = Theta(U)`. In particular, it settles the critical rank-one transition inside this class. A method attaining `F` on every input would have to leave this class.

### Shifted-Wishart posterior — Theorem 10.1 and Corollary 10.2

For the singular matrix

```
H = Q0 (h I + G G^T) Q0^T,
G of size (n-k) by (n-k+1),
```

with a Haar frame `Q0`, the note derives an exact residual-kernel posterior after arbitrary adaptive orthonormal queries, while the queried compression `J` satisfies `J > h I`. It also gives the exact conditional law of the next Schur pivot.

This is a conditional-distribution theorem with an explicit domain, not an all-adaptive query lower bound. In particular, it does not control all stopping times or establish the missing rank factor.

### Averaged rank-one algorithm — Theorem 11.2

For `k=1`, `n>=8`, `0<epsilon<=1/16`, `h=400 n epsilon`, and `A=I-H/(100n)`, the note gives an oracle algorithm using at most

```
min(n, ceil(5 epsilon^(-1/2) log(1+n sqrt(epsilon))))
```

queries and succeeding with probability at least 0.99 **averaged over this particular input law and the algorithm's start**. The proof uses a Gaussian integration-by-parts resolvent identity, not a large-dimension asymptotic theorem. The polynomial coefficients use the known form of this law; no hidden eigenvectors or eigenvalues are consulted.

This averaged result is not a pointwise all-input `F` upper bound. It does show that this shifted rank-one law cannot witness a linear lower bound at `epsilon=(log n/n)^2`: it is too easy even for a single-vector polynomial method. Conditioning it on a different, rare hard event would require a new analysis.

## What remains open in this package

The inherited, unreviewed v5 arguments give universal constants with

```
max(k, c F) <= q_sp <= min(n, ceil(12000 (k/s) log(e*n/k))).
```

At `k=1` and `epsilon=(log n/n)^2`, these still leave

```
Omega(n log log n / log n) <= q_sp <= n.
```

The ratio is unbounded. This continuation does not narrow that unrestricted interval. `REMAINING_GAP.md` identifies exactly which transfers are missing or invalid. `STATUS.json` and `CLAIMS.json` preserve the model and probability qualifiers in machine-readable form.

The PDF and ZIP from v5 are preserved byte-for-byte in `prior/`. They contain the preceding versions and their original qualifications. No external repository was modified.

## Files

`report.pdf` and `report.tex` contain the mathematical statements and proofs. `PROOF_AUDIT.md` maps the nonstandard proof steps and their limitations. `COMPARISON.md` separates the v5 results from the v6 additions. `sources/` contains source metadata and the roles of the primary references, without redistributing their papers.

`src/weighted_krylov.py` implements the weighted polynomial geometry, integer multiplicities, query counters, posterior identities, resolvent diagnostics, and the distribution-specific rank-one algorithm. `tests/` contains the new component tests. `run_checks.py` also extracts and reruns the unchanged prior suites into temporary directories. It does not overwrite the preserved archives.

`results/` contains the actual logs and raw diagnostic outcomes, including countervailing outcomes. `MANIFEST.json`, `build_manifest.py`, and `verify_manifest.py` provide byte-integrity checks, not mathematical certification or authentication.

## Reproduce

First verify the untouched extraction:

```sh
python verify_manifest.py
```

Then, preferably in a separate working copy:

```sh
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 python run_checks.py
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

Rerunning the checks changes timestamps and result files. The original manifest will correctly report those changed bytes. A deliberately regenerated working copy can receive a new local manifest with `python build_manifest.py`; this does not certify the mathematics.

The recorded environment was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and mpmath 1.3.0. The mathematical oracle uses exact real arithmetic; implementations use floating point or high-precision numerical arithmetic where stated. A LaTeX installation with the packages named in `report.tex` is needed only to rebuild the PDF.

## Actual checks and their limits

All **45 new component tests**, **28 unchanged v5 tests**, **20 unchanged v4 tests**, and **17 unchanged v3 tests** passed: **110 tests total**. These check identities, constants, and implementations. They do not enumerate arbitrary adaptive algorithms or constitute a formal proof.

The 72 whole-prefix weighted-cone diagnostics include 42 numerical no-cone outcomes and 30 outcomes in which the cone was not excluded. None of these small examples meets the theorem's deliberately conservative sufficient constant condition; they are algebra and behavior checks, not experimental verification of that universal threshold.

All 96 shifted rank-one algorithm trials met their actual-target diagnostic: 64 polynomial runs and 32 exact-column runs. This is an experiment on one input law, not a worst-case guarantee.

The resolvent diagnostics preserve an initial small-sample discrepancy: at `r=4, t=0.004`, 2,000 draws gave 2.55 against the exact expectation 4. A separately seeded, fixed-size 250,000-draw holdout gave 4.006 with a sample standard error of 0.051. Both are retained; neither is labeled a statistical proof. The expectation identity is established analytically in Lemma 11.1.

No mathematical priority, independent peer review, or proof-assistant verification is claimed. The package supplies inspectable research arguments with their exact scope, not a completed RA-14 solution.
