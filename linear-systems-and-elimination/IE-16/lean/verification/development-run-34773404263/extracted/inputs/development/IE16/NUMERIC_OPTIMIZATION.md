# IE-16 finite-coordinate compiler optimization

Written before the following helper implementation, after Linux draft run 34771972369.
The frozen Definitions, Challenge, and all 15 public contracts remain unchanged.

For a in Fin 3 define R(a) = 1 if a=0 and -1/2 otherwise; define J(a) = 0,
1/2, -1/2 at a=0,1,2 respectively. The exact identities to prove are

- Re(omega^a) = R(a);
- Im(omega^a) = sqrt(3) J(a);
- Re(clusterPoint a b) = R(a) + R(b)/1000;
- Im(clusterPoint a b) = sqrt(3) (J(a) + J(b)/1000).

Since sqrt(3) is positive, equality of two cluster points implies equality of
the two rational coordinates R(a)+R(b)/1000 and J(a)+J(b)/1000. The nine rational
coordinate pairs are distinct. The finite injectivity check can therefore run
on these rational coordinates, after only six cubic-root component cases,
rather than expanding complex powers independently in 81 comparisons.

Substituting these complex coordinate pairs first limits squared witness norms
to degree 6 in sqrt(3), and weighted moments to degree 7. For the remaining
exact field identities, expose explicit natural exponents
2 through 7 with sqrt(3)^(2n)=3^n and sqrt(3)^(2n+1)=3^n sqrt(3). This preserves
the symbolic algebra strategy and introduces no interval subdivision. Expand
Fin 3 sums by the direct three-term identity, then normalize Fin equality with
simp only before numerical simplification; do not combine Fin.ext_iff with
the default reverse value-equality simplifier. No memory or wall-clock bound
is raised. All new source remains uncompiled until the next Linux run.
