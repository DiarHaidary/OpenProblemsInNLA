# Fractional block-packing exploration

These computations are separate from the exact mathematical proofs.

A candidate construction chooses small normal subpairs from the original spectral lists, together with feasible unitary alignments for each subpair. A linear program assigns nonnegative weights to these blocks so that every original eigenvalue has total multiplicity one on each side. Clearing rational denominators gives a finite direct-sum construction for an amplified pair. This searches a different class of candidates from a single large random unitary start.

The saved run contains 32 pairs: 24 in dimension 6 and 8 in dimension 4. It evaluates 64 three-dimensional subpairs per six-dimensional input and 16 per four-dimensional input, together with singleton blocks. The inputs are split or padded perturbations of the reference spectral pattern, with normalized perturbation scales spanning 0.002 to 0.8. Both antisymmetric and independently perturbed pairs occur. The random seeds are fixed in the source.

The recorded constructions have exact rational block multiplicities with amplification factors at most 5. Two raw comparisons (cases 2 and 6) improve on the initially recorded base witnesses by approximately 9.09e-8 and 1.63e-7. Both have exact amplification denominator **k = 1**: their blocks already assemble to an ordinary base-dimensional unitary. The audit constructs those replacement base witnesses explicitly. Consequently neither comparison is an amplification counterexample. After including these available base witnesses, no candidate gap exceeds 1e-8; comparisons with k at least two differ by at most numerical roundoff on the positive side. The original raw search records are preserved rather than overwritten.

## Interpretation

The base optimizer is numerical and does not provide a global lower bound. The block objective values and unitarity checks are floating-point calculations, not interval-certified operator-norm bounds. The incidence-matrix marginal equations and rational block multiplicities are checked exactly. Fields named `upper` in the saved JSON mean numerical feasible objective estimates, not independently certified exact upper bounds.

Absence of a candidate in this finite search is not a proof of general amplification invariance. No numerical result from this directory is used in either new theorem.

## Audit and rerun

The stored-data audit needs only NumPy and the Python standard library:

```bash
python new_results/experiments/verify_saved_data.py
```

It checks the exact multiplicity equations, matrix dimensions, numerical unitarity, and recomputed objective values. Whenever the exact denominator is one, it also assembles the block construction as a base-size unitary and includes that witness in the vetted comparison. An archived audit is in `results/audit.json`.

The optional search requires SciPy in addition to NumPy. The saved run used SciPy 1.17.1. From the package root:

```bash
python -m pip install -r requirements-experiments.txt
python new_results/experiments/search_fractional_blocks.py
```

A rerun writes to `rerun_results/`, preserving the archived results. Numerical optimization outcomes can vary with software and linear-algebra implementations. Re-running the search is not required to verify the theorems.
