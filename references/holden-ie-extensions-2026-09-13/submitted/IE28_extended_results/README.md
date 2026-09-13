# IE-28 — extended rigorous results

**This is not a full solution of IE-28.** The assertion for every stage count and every admissible positive node set is neither proved nor disproved in this archive. The main document states that limitation on its first page and identifies the exact remaining gap in Section 8.3.

## Read first

`writeup.pdf` is the new 13-page mathematical writeup; `writeup.tex` is its editable source. `PROOF_AUDIT.md` maps the claims to their proofs and computation dependencies. The preceding nine-page partial writeup, its implementation, and its results are preserved in `prior_work/`; statements there about the then-current scope describe the earlier version.

## What is established

For the collocation matrix A on 0 < c_1 < ... < c_n <= 1, the target is a single positive diagonal D with (I - D^{-1} A)^n = 0.

- Every node pair and every node triple: complete analytic constructions, retained from the previous work and reproduced in Section 2.
- Every fixed stage count n: existence for all nodes sufficiently close to a common positive point, proved in Theorem 5.3 by a regularized confluent determinant, an algebraic triangular seed, and a nonsingular Jacobian. This is a LOCAL theorem in the node variables, not a general-node theorem.
- Every stage count n, for scaled ordinary Laguerre zeros: D = delta I is an exact solution. These are also exactly the node sets admitting a scalar positive D (Theorem 3.2).
- Six specified node sets and six explicit node neighborhoods in dimensions 4–7: positive solutions proved by exact integer interval certificates. Uniqueness is only within the listed diagonal box.
- Eleven stages near coincident nodes: no polynomial p with all nonnegative coefficients can yield a solution through d_i = p(c_i)/p'(c_i). This follows from an exact interval sign proof and a compactness argument (Theorem 6.2). It disproves a stronger auxiliary construction, NOT IE-28. Positive D still exists there by the local theorem.

The equally spaced n = 8, 11, 15 continuation examples are NUMERICAL ONLY. They are not among the interval-certified cases. Their JSON `pass` flags mean numerical stopping tests passed.

## Verify without third-party packages

Use Python 3.10 or newer. Run from the extracted archive root:

```sh
python scripts/verify_manifest.py
python certification/verify.py certification/point_certificates.json certification/neighborhood_certificates.json
python cluster/certify_seed.py
```

The certificate verifier uses only integer arithmetic and exact rational input conversion for its acceptance decisions. Floating-point conversion is used solely to print readable summaries. The eleven-stage sign proof also uses only the standard library. It checks strict bounds on the coefficient of t^11:

    -1.664575e-10 < coefficient < -1.664574e-10 < 0.

Full rational bounds, centers, boxes, preconditioners, and result files are included. A passing certificate proves existence, not merely proximity to an unverified numerical candidate.

## Additional regression and numerical tests

Install the optional computational dependencies, then run:

```sh
python -m pip install -r requirements.txt
python tests/test_exact.py
python tests/test_numerics.py
python prior_work/scripts/check_symbolic.py
```

`tests/test_exact.py` checks 1,500 rational interval trials, 50 exact determinant comparisons, formal seed Jacobians, exact confluent and collocation identities, the Laguerre identities, all twelve certificates, and deliberate input corruptions. `tests/test_numerics.py` independently checks both regularized pencils and the analytic Jacobian and reruns an eight-stage continuation example. The analytical all-stage proofs do not rely on finite regression tests.

Saved outputs are under `results/`. `results/environment.json` records the actual tested environment; this is not a claim about the newest available package versions.

## Reproduce candidate generation

The generation path is not part of the exact verifier's trusted computation:

```sh
python certification/generate.py --out-dir /tmp/ie28-regenerated
python certification/verify.py /tmp/ie28-regenerated/point_certificates.json /tmp/ie28-regenerated/neighborhood_certificates.json
```

It refines the previous numerical candidates and searches for node boxes which the independent verifier accepts. It uses the preserved numerical data and code in `prior_work/` and no external downloads.

Reproduce an equally spaced continuation run with:

```sh
python numerics/continue_cluster.py --stages 8 --dps 60 --out /tmp/ie28-n8.json
python numerics/continue_cluster.py --stages 11 --dps 80 --out /tmp/ie28-n11.json
python numerics/continue_cluster.py --stages 15 --dps 90 --out /tmp/ie28-n15.json
```

There is no claimed termination guarantee for arbitrary targets. A failure is not a counterexample, and a small residual is not an exact existence certificate.

## Rebuild the document

A standard LaTeX installation with the packages named in `writeup.tex` suffices:

```sh
pdflatex -interaction=nonstopmode -halt-on-error writeup.tex
pdflatex -interaction=nonstopmode -halt-on-error writeup.tex
```

The supplied PDF was rendered and visually checked. Build logs and page-rendering images are not included in the archive. No font files are distributed.

## Full-solution gap

The missing statement is existence for an arbitrary prescribed node vector at every n >= 4. Local existence near coincidence and finitely many certified boxes do not cover the full node domain. In particular, no proof is given that the analytic seed branch can always be continued while preserving positivity and avoiding an obstructing singularity or escape. No positive-real conclusion is inferred merely from a complex inverse-eigenvalue existence theorem.

## Sources and attribution

References are in the PDF and `REFERENCES.md`. The cited website and papers were read directly; no GitHub connector was used. The mathematical arguments in the main document are presented for checking and are not claimed to have been independently peer reviewed or proven novel relative to all literature.
