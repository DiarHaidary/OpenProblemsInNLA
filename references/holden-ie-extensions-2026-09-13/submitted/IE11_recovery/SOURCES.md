# Sources and attribution

1. James Chen, Alan Edelman, John Urschel, **The largest 5th pivot may be the
   root of a 61st degree polynomial**, arXiv:2602.20390v1, 23 February 2026.
   https://arxiv.org/html/2602.20390v1
   The page states a CC BY 4.0 license. Candidate pattern: equation (2.1).
   Target polynomial: equation (2.15). Published upper bound: Theorem 3.5.
   The candidate and its known lower bound are attributed to these authors.

2. **IE-11 — The exact fifth complete-pivoting growth factor**, in
   OpenProblemsInNLA, `linear-systems-and-elimination/IE-11`.
   https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/linear-systems-and-elimination/IE-11
   Raw statement consulted:
   https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/linear-systems-and-elimination/IE-11/README.md

The website and statement were read directly, without a GitHub plugin.
Access date for this reconstruction: 13 September 2026.

`data/reference_P5_ascending.txt` is a separate transcription of the 62 integer
coefficients in source 1, equation (2.15), in ascending powers of g. The verifier
compares each coefficient against the polynomial obtained independently by
exact rational elimination and discriminant factorization. The full source
paper is not redistributed.

The report's proofs spell out the needed contraction, implicit-coordinate,
Schur-complement and convex-hull reasoning. The code is an executable exact-
arithmetic check, not a proof-assistant formalization. No novelty or priority
claim is made for the mathematical observations in this recovery package.

Version note: the unversioned arXiv landing page lists v2 dated 15 March 2026.
This coefficient audit deliberately pins v1, which is the version linked by
the IE-11 statement. The landing-page abstract continues to distinguish the
candidate lower bound from the conjectured global optimum.
