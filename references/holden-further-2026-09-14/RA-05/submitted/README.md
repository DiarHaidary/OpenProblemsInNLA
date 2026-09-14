# RA-05: a complete resolution claim

**Strong row coresets and the even/non-even dichotomy**  
Prepared for Sidney Holden with ChatGPT, September 13, 2026.

## Main result

Let `S_p(k, epsilon)` be the worst-case minimum number of original rows in a nonnegative strong coreset for Euclidean subspace costs of power `p`, with fitted-subspace dimension at most `k`. Input rank and ambient dimension are unrestricted.

For every fixed real `p > 2`, up to logarithmic factors in `2k/epsilon`:

- If `p` is not an even integer, `S_p(k, epsilon) = Theta_tilde_p(k^(p/2) / epsilon^2)`.
- If `p = 2s` is even, `S_p(k, epsilon) = Theta_tilde_p(min(k^s / epsilon^2, k^(s+1/2) / epsilon + k^(s-1) / epsilon^2))`.

Every integer `k >= 1` and every `0 < epsilon < 1/2` is covered. Constants depend only on the fixed exponent. Part I, Theorem 1.1 states explicit logarithmic losses. The displayed subsidiary proposal in RA-05 is false for every fixed real `p > 2`.

**Status: complete resolution claimed, pending independent review.** This is not peer-review acceptance, formal verification, or an assertion of first-discovery priority. No repository files were changed.

## Read first

`RA05_full_resolution.pdf` is the complete 43-page document.

Its first 16 pages contain the full theorem, new non-even proof, an exact cubic universal-support certificate, and a proof audit. Page 17 explains the provenance and numbering of Part II. The final 26 pages reproduce the complete preceding even-power proof unchanged.

Part II's historical notices that non-even exponents remain open describe that earlier manuscript only. Part I proves the missing case. The two parts are separate proofs; no interpolation in the exponent is assumed.

## The new argument

A spherical core has about `r^(p/2)` original vectors, a stable rectangular absolute-power evaluation matrix, and bounded cost on every chosen test. A selected Boolean-cube family has about `2^h / h` original vectors and a stable middle-Walsh evaluation matrix for every non-even `p`.

Tensor the input vectors. The complete error matrix over product test normals is `G (W - 1) F^T`. Its Frobenius norm is bounded below by the product of the two least singular values. Every omitted input row contributes one to the squared norm of `W - 1`. Choosing `h = O(log(1/epsilon))` forces the multiplicative rank/accuracy lower bound. A separate explicit arbitrary-rank input covers ranks too small for the tensor construction, within the stated logarithmic loss.

The Boolean middle-spectrum mechanism is explicitly credited to Li–Wang–Woodruff, *Tight Bounds for the Subspace Sketch Problem with Applications*, Section 3.1. This package reproves the needed Fourier estimate and uses a direct support argument, not a bit-complexity-to-support inference.

## Reproduce the checks

The exact cubic certificate uses Python's standard library only:

```sh
python code/check_certificate.py
```

For the new numerical diagnostics and archive-integrity check:

```sh
python -m pip install -r requirements.txt
sh run_checks.sh
```

The script uses temporary output paths, so it does not overwrite the packaged verification records. There are 240 new numerical/algebraic diagnostics. The separate exact checker reports 17,575 assertions, most being repeated tensor identities or direct residuals; this is not a count of independent proof audits.

The cubic certificate proves, for a specified 204-row integer matrix in 32 dimensions and query rank 31,

`support >= 204 - 548592 * epsilon^2`

for **every real reweighting** that preserves the specified legal tests. Thus accuracy `1/100` requires at least 150 rows, and accuracy `1/1000` requires all 204. A supplied 12-row positive reweighting has direct cubic residual costs `396*sqrt(2)` and `4352*sqrt(2)` at its violating query, for relative error `989/99`.

The finite checks do not implement or formally verify restricted invertibility, the asymptotic random-core existence proof, the imported general upper bound, or Part II's partial-coloring construction.

## Build the PDF

The prebuilt PDFs are included. To rebuild Part I, the bridge page, and the combined PDF (requires a LaTeX installation and `pypdf`):

```sh
sh build_pdf.sh
```

The even-power PDF is reused unchanged; its source is also included. The exact original predecessor ZIP is under `prior_work/`, containing all its tests and nested history. Its checks were rerun separately and are not counted as new evidence.

## Directory guide

`manuscript/` contains the new LaTeX/PDF and the unchanged even proof.  
`code/` contains generators, diagnostics, exact certificate and hash checkers.  
`results/` contains reproducible finite records, PDF assembly information, and validation.  
`prior_work/` contains the unchanged previous package.  
`PROOF_AUDIT.md`, `SOURCES.md`, and `STATUS.md` record mathematical dependencies and evidence boundaries.  
`SHA256SUMS` covers all deliverable files except itself.
