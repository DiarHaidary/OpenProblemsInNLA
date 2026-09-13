# Sources

Read during recovery on 12 September 2026 unless otherwise noted.

1. **IE-27 — Spectral disk for a Radau stage preconditioner.** OpenProblemsInNLA,
   linear-systems-and-elimination/IE-27/README.md.
   https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/linear-systems-and-elimination/IE-27/README.md
   The target is the symmetric positive-definite spatial setting and a disk
   **radius**, not diameter, equal to the Euclidean norm of U-I.

2. **Ivo Dravins, Stefano Serra-Capizzano, Maya Neytcheva.** *Fine spectral
   analysis of preconditioned matrices and matrix-sequences arising from
   stage-parallel implicit Runge-Kutta methods of arbitrarily high order.*
   arXiv:2302.04657v2, 24 February 2023.
   https://arxiv.org/html/2302.04657v2
   Sections 2 and 4 give the preconditioner and detailed low-stage spectral
   analyses. No novelty claim is made for the two- and three-stage cases here.

3. **M. Outrata.** *On the recent advances of spectral analysis for systems
   arising from fully-implicit RK methods.* arXiv:2510.21241v1,
   24 October 2025.
   https://arxiv.org/html/2510.21241v1
   Sections 2.1–2.3 discuss the relationship between polynomial and small-matrix
   spectral reductions. The repository explicitly disambiguates the disk's
   radius from the word “diameter” appearing in this preprint.

4. **O. Axelsson, I. Dravins, M. Neytcheva.** *Stage-parallel preconditioners
   for implicit Runge-Kutta methods of arbitrarily high order, linear problems.*
   Numerical Linear Algebra with Applications 31(1), e2532 (2024),
   DOI: 10.1002/nla.2532.
   https://doi.org/10.1002/nla.2532
   Original conjecture as identified by source 1. Bibliographic information
   and the location of Conjecture 1 are taken from the repository. The
   institutional PDF retrieval timed out during recovery, so this archive
   does not claim a fresh full-text inspection of that PDF.

The proofs and certificate computations in the report are included in full.
These sources identify the problem and its literature context; none is used as
a substitute for proving an unchecked all-stage conclusion.
