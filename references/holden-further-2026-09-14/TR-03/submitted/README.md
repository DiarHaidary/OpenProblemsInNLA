# TR-03: an all-spectrum upper bound

**Completion status: partial. This package is not a full solution of TR-03.**

The report gives a self-contained argument for

\[
R_{n,k}\le\min\{k+1,n-k,2^{34}e^{2560}\sqrt{k}\}
\quad(2\le k\le n-2),
\]

valid for every positive finite spectrum. It proves the previously conditional oversampled-profile estimate, in the stronger form

\[
\mathcal X_{n,k,q}(\sigma)\ge
2^{-30}e^{-2560}\frac{k+1}{q+\sqrt{\min(k,n-k)}}
\sum_{i>q}\sigma_i,
\qquad 0\le q<k/4.
\]

The constants are deliberately conservative. They establish an asymptotic upper bound, not a useful numerical constant for practical matrix sizes.

## What remains unproved

The sharp joint dependence on n and k is not determined. In particular, this package supplies neither a matching growing lower bound for the original ratio nor an all-finite-spectrum O(sqrt(n-k)) upper bound in the strongly unbalanced regime. It does not claim Theta(sqrt(min(k,n-k))). A lower bound on an adversary's attainable error must not be mistaken for a lower bound on the ratio.

## Files

`TR03_all_spectra_bound.pdf` is the typeset report when PDF compilation succeeds. Its complete editable source is `TR03_all_spectra_bound.tex`. `notes/proof_audit.md` records logical dependencies and the distinctions most susceptible to sign or quantifier mistakes. `results/verification.json` and `results/verification.log` record the executed finite checks; `results/execution.json` records their process status. `results/layout_audit.json` records automated PDF checks when a PDF is available.

The three supplied prior ZIP archives are in `prior/`, unchanged. `SHA256SUMS` covers the packaged files. This continuation's mathematical claims are proved in the new report; no new theorem is inferred solely from a previous summary or a numerical search.

## Reproduce the checks

Use Python 3.10 or newer. In a suitable environment:

```sh
python -m pip install -r code/requirements.txt
OPENBLAS_NUM_THREADS=1 python code/verify.py
```

The seed is fixed in the script. Some inequalities use exact rational arithmetic; matrix tests use explicitly stated numerical tolerances. These are finite checks, not proof-assistant certification of the universal statements. The analytic probability estimates are checked through their deterministic margins rather than through simulations of extremely rare events.

## Rebuild the PDF

With a standard TeX installation containing the packages listed at the start of the source:

```sh
pdflatex -interaction=nonstopmode -halt-on-error TR03_all_spectra_bound.tex
pdflatex -interaction=nonstopmode -halt-on-error TR03_all_spectra_bound.tex
```

The proofs have not been independently peer reviewed or formally certified. The completion status remains partial regardless of whether all finite tests pass.
