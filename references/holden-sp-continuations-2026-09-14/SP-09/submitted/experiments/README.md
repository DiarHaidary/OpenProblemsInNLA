# Numerical illustrations, separate from the proof

`first_order_witness_demo.py` constructs a six-dimensional upper-bound witness for the manuscript's example with exact first-order coefficient 603/364. It uses a closed four-vector polygon, a finite face-map solve, and a matrix exponential. Its Taylor table illustrates a feasible construction only.

`candidate34/` stores one n=7, k=2 numerical search. The best retained amplified witness is the tensor repetition of the best retained base witness; both values are about 1.4126107335852258. `verify_candidate34.py` checks shapes, spectra, unitarity tolerances, and objective values. It does not certify optimality in either dimension.

`search_candidate34.py` and `search_orbits.py` reproduce the numerical search, writing new results to `candidate34_rerun/` rather than overwriting the archived witnesses. Nonconvex optimization results are upper bounds, even when many starts agree. These computations are not used in the analytic lower proof.
