# References and bounded literature check

Direct website access was used; no GitHub plugin was used. The search did not locate a full positive-real fixed-diagonal existence proof or a counterexample to the exact IE-28 target. This is a bounded search, not a claim that all literature has been exhausted.

1. **IE-28 problem statement**, OpenProblemsInNLA. Accessed 12 September 2026; the page records a status check dated 11 September 2026. It explicitly quantifies over positive distinct node sets, imposes no diagonal ordering, and distinguishes the stiff target from nilpotence of A-D and from variable-sweep constructions.
   https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/linear-systems-and-elimination/IE-28/README.md

2. **P. J. van der Houwen and J. J. B. de Swart**, “Triangularly implicit iteration methods for ODE-IVP solvers,” SIAM Journal on Scientific Computing 18(1) (1997), 41–55. DOI: 10.1137/S1064827595287456. Section 3.2.1, p. 46, is the original conjecture context.
   https://ir.cwi.nl/pub/2191/2191D.pdf

3. **G. Čaklović, T. Lunet, S. Götschel, and D. Ruprecht**, “Improving efficiency of parallel across the method spectral deferred corrections,” SIAM Journal on Scientific Computing 47(1) (2025), A430–A453. DOI: 10.1137/24M1649800. Section 2.2.3 explicitly does not guarantee stiff-limit nilpotent diagonal coefficients for every stage count. Theorem 2.8 concerns A-D, and Theorem 2.12 concerns successive different diagonals; neither is the fixed-D target.
   https://epubs.siam.org/doi/10.1137/24M1649800
   Open PDF: https://d-nb.info/1363153935/34

4. **W. M. Lioen**, “On the diagonal approximation of full matrices,” CWI NM-R9518 (1995); journal version, Journal of Computational and Applied Mathematics 75(1) (1996), 35–42. The report gives low-order algebraic computations and higher-order numerical evidence, not the all-node all-stage theorem.
   https://ir.cwi.nl/pub/4925
   https://ir.cwi.nl/pub/4925/04925D.pdf

5. **J. Rosenthal and X. Wang**, “The multiplicative inverse eigenvalue problem over an algebraically closed field,” SIAM Journal on Matrix Analysis and Applications 23(2) (2001), 517–523. Generic or principal-minor-based complex existence is not positive-real existence for this problem.
   https://arxiv.org/abs/math/0009163
   https://www.math.uzh.ch/d.php/publication/421

6. **M. Bolten and L. Wimmer**, “On the Analysis of Spectral Deferred Corrections for Differential-Algebraic Equations of Index One,” Journal of Scientific Computing 108, 67 (2026), DOI: 10.1007/s10915-026-03385-7. Checked as a recent SDC follow-up; its discussion of the analytical preconditioner approach points back to the 2025 work rather than supplying the arbitrary-positive-node fixed-diagonal theorem.
   https://link.springer.com/article/10.1007/s10915-026-03385-7

The new local existence, scalar Laguerre, and eigenpolynomial-obstruction arguments are supplied in full in the writeup. They are not attributed to the above sources and are not presented as a verified claim of priority.
