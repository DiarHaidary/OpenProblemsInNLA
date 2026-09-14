# Sources and attribution

1. **SP-03 statement.** OpenProblemsInNLA, “The Euclidean distance degree of the real symplectic group.” The ordinary transpose, fixed embedding, and all-rank proposed formula are part of the target. Accessed September 13–14, 2026.
   https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/eigenvalues-and-inverse-problems/SP-03

2. **Primary proposed formula and small-rank counts.** J. A. Baaijens and J. Draisma, *Euclidean distance degrees of real algebraic groups*, Linear Algebra and its Applications 467 (2015), 174–187, Section 5, p. 187. DOI 10.1016/j.laa.2014.11.012. This source reports 4, 24, 544 and proposes, but does not prove, the all-rank pattern. The Q-metric coordinate change is also in its symplectic discussion.
   https://arxiv.org/abs/1405.0422
   https://pure.tue.nl/ws/files/3846347/391917266748824.pdf

3. **Earlier multiplier reduction.** S. Holden, SP-03 supporting proof note, September 12, 2026. Saturated skew-multiplier quartics and generic regularity; not an exact new generic degree computation.
   https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/references/holden-spectral-2026-09-12/SP-03/proof.md

4. **Supplied predecessor.** *SP-03: reduction, bounds, and certificates*, eleven-page report in `prior/SP03_verified_partial.zip`. It proves the regular m^2-variable reduction, supermultiplicativity, the degree upper bound, and a rank-one quartic. It includes exact lower-bound certificates 4,24,542. This is a supplied report, not asserted to be a peer-reviewed publication.

5. **Ordinary symplectic group degree.** M. Brandt, D. J. Bruce, T. Brysiewicz, R. Krone, and E. Robeva, *The degree of SO(n)*, arXiv:1701.03200v2 (2017), Section 3. Its symplectic determinant formula is an ordinary algebraic degree, not an ED degree.
   https://arxiv.org/abs/1701.03200

6. **Morse theory used for parity.** J. Milnor, *Morse Theory*, Annals of Mathematics Studies 51, Princeton University Press (1963), Theorem 3.5, p. 20. Proper Morse functions produce the CW decomposition used in the parity proof; the report verifies properness and finiteness and supplies the polar-deformation and conjugation arguments.
   https://webhomes.maths.ed.ac.uk/~v1ranick/papers/milnmors.pdf

7. **Repository reporting rules.** OpenProblemsInNLA, CONTRIBUTING.md, “Reporting a resolution” and the distinction between supporting/partial work and a complete resolution. No status edit was performed.
   https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/CONTRIBUTING.md

## Scope checks that did not settle SP-03

R. Wu, R. Chakrabarti, and H. Rabitz, *Critical topology for optimization on the symplectic group*, arXiv:0708.3822v2, analyzes a real symplectic setting with symplectic targets. Its positivity-based classification cannot be substituted for the generic complex critical count in SP-03. No count from it is used as an ED-degree input here.
https://arxiv.org/abs/0708.3822

The denominator factorization, Stein-domain normal form, projective-boundary and zero-coupling arguments, Euler-characteristic calculation, parity argument, and new exact certificate results are argued or checked in this package. No literature novelty claim is made merely because these were developed in this continuation.
