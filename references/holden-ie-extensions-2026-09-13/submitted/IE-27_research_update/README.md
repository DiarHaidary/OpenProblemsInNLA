# IE-27 — continued analysis and verified extensions

**This is not a complete solution of IE-27.** The arbitrary-stage disk inequality has not been proved here. Neither exact counterexample in this update refutes IE-27 as stated.

Start with **`report.pdf`**, the eight-page continuation. Its LaTeX source is `report.tex`. The earlier nine-page manuscript and all its supporting files are retained in **`prior_results/`**.

## Proved results in this archive

For `B_q = L_q^{-1}`, `N_q = U_q-I`, and `r_q = ||N_q||_2`, the requested inequality is

`rho((I + mu B_q)^{-1} N_q) <= r_q` for every admissible integer `q >= 2` and every **real** `mu > 0`.

The supplied **66 exact-arithmetic certificates** prove it for every positive shift at each of these stage counts:

**2–64 inclusive, 80, 96, and 128.**

This is **not** a claim for every stage through 128. Stages 65–79, 81–95, 97–127, and stages above 128 are not covered by these certificates. Each included certificate covers the whole positive-shift continuum, not a finite grid.

The continuation proves, for every stage count, the enclosure in the two regimes

`0 < mu <= 1 / (q ||B_q||_2)` or `mu >= 2 ||L_q||_2`.

It also proves a rank-two weighted identity and a sufficient single-matrix square-root criterion for the stronger Euclidean norm bound. The latter criterion has **not** been established for all Radau stages.

## What remains missing

For stages outside the supplied finite set, the intermediate-shift inequality is still unproved. No theorem here guarantees that the common-energy certificate generator succeeds for every stage. Numerical evidence is not used to fill this gap.

The exact counterexamples in `code/exact_obstructions.py` rule out two broader assertions:

* Positive triangular pivots and weighted accretivity of a generic matrix do not imply the desired radius bound. The example is **not Radau**.
* Allowing **complex** shifts with positive real part breaks the enclosure already at the genuine three-stage Radau matrix. The example has `mu = 1/100 + 3i`, so it is **outside IE-27's real-positive-shift hypothesis**.

## Recheck the mathematical certificates

Python 3.10 or newer is required. Verification uses only the standard library; it does not require NumPy, SciPy, an optimizer, or a numerical eigensolver.

From the extracted directory:

```sh
python code/run_all.py
```

This checks all 66 supplied certificates, the exact three-stage calculation, the two rejected extensions, and 20 regression tests. Results go into `recheck/`, leaving the delivered results unchanged. A mathematical check failure returns a nonzero exit status.

A smaller run:

```sh
python code/run_all.py --stages 96 128 --output recheck_new
python code/exact_obstructions.py
```

The completed verification from this investigation is recorded in `results/full_recheck/`. The checker reconstructs Radau factors from verified root intervals and exact formulas. It checks the energy inequalities by outward-rounded integer-interval LDL factorization. The optimizer's output is only a proposal until those checks pass.

## Optional numerical exploration

This is separate from proof verification:

```sh
python -m pip install -r prior_results/requirements-generation.txt
python code/diagnostics.py --output numerical_run.json
```

The diagnostic script and its bundled output are explicitly marked **NUMERICAL_ONLY**. A maximum over its 101-point grid is only a sampled maximum. Roundoff-clipped square roots are used only in these diagnostics, never in a certificate check.

Additional certificate candidates can be generated with the retained code, but no success guarantee is claimed:

```sh
python prior_results/code/generate.py 65 --output proposed_certificates
python prior_results/code/verify.py proposed_certificates/q065.json
```

The command above is a usage example; no stage-65 certificate is included in this archive.

## Rebuild the report

With a standard LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

`PROVENANCE.md` identifies retained and new material. `references/sources.md` records the website check. `MANIFEST.sha256` records file hashes; integrity checks are not mathematical proofs.
