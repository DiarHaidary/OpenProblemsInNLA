# SP-06 source correspondence

All canonical source bytes are pinned to upstream commit `50838e37dd793830e2cecd1055cfc7e0349490f1`.

| Role | Repository path | Git blob | SHA-256 |
|---|---|---|---|
| canonical problem | `eigenvalues-and-inverse-problems/SP-06/README.md` | `a125cb469ab972c73f9474a29e87f984e064b47f` | `e2eb891930c96d6a3bdd25c75bfe6bd2798cc8c540ce00ec851f7bf1f0ceb25c` |
| complete original solution | `eigenvalues-and-inverse-problems/SP-06/solution.md` | `05657b7db756b6d425477e9e55a5946bd4e96245` | `c7adb8f97238049b20e82044d8527b70301779ba041169f74fe603a88ea1ae7a` |
| canonical problem TeX | `eigenvalues-and-inverse-problems/SP-06/problem.tex` | `604b101d6c704b6e455d055dd996d1b84fad8a3a` | `183127180596a36c108ed8575420e3845ca890f3048a32ec1252d61cf60d5311` |
| complete solution TeX | `eigenvalues-and-inverse-problems/SP-06/solution.tex` | `94a417b5043ba298ed614bbf419dc2a260c01af8` | `b7340bf85e0b776ed49a4303af64820b72708eb249fbdc885b9179945e60ffc9` |

The original mathematical proof is attributed to Matthew J. Colbrook, Department
of Applied Mathematics and Theoretical Physics, University of Cambridge. The
formalization is credited to George Stepaniants, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. No email is added for George.

The finite Laurent-coefficient function retains every complex coefficient.
Natural positive bandwidths represent precisely the original positive integers.
The index shift from `1,...,n` to `Fin n` leaves `i-j` unchanged. The actual
Mathlib unit circle and algebra spectrum implement the original Jordan-curve
and finite-section spectrum definitions.

The source proof uses a periodic trigonometric radius; this development instead
uses the unit-circle real coordinate and a uniform algebraic root-separation
bound. This changes the proof method without changing the original target.
A negative resolution needs one nonreal spectral point of one admissible section;
the stronger source statement giving both points and enclosure of zero is not
claimed as a separate complete formalization.

To recheck an original source hash from a checkout containing the pinned commit,
run `git show COMMIT:PATH | shasum -a 256` with the exact COMMIT and PATH above.
