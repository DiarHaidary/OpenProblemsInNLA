"""Independent exact coefficient reconstruction for the statement draft.

These identities do not establish algebraic smoothness, genericity, a cardinal
count, or a Lean theorem. No external symbolic or numerical package is used.
"""
from fractions import Fraction
from itertools import permutations
import json

N = 9

class Poly:
    def __init__(self, value=0):
        self.c = ({e: Fraction(v) for e, v in value.items() if v}
                  if isinstance(value, dict) else
                  ({(0,) * N: Fraction(value)} if value else {}))

    @staticmethod
    def var(i):
        e = [0] * N
        e[i] = 1
        return Poly({tuple(e): 1})

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        c = self.c.copy()
        for e, v in other.c.items():
            c[e] = c.get(e, 0) + v
        return Poly(c)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -v for e, v in self.c.items()})

    def __sub__(self, other):
        return self + -(other if isinstance(other, Poly) else Poly(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        c = {}
        for e, v in self.c.items():
            for f, w in other.c.items():
                k = tuple(x + y for x, y in zip(e, f))
                c[k] = c.get(k, 0) + v * w
        return Poly(c)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        value = Poly(1)
        for _ in range(n):
            value = value * self
        return value

    def __eq__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        return self.c == other.c

    def derivative(self, i):
        out = {}
        for e, c in self.c.items():
            if e[i]:
                f = list(e)
                f[i] -= 1
                out[tuple(f)] = c * e[i]
        return Poly(out)

    def substitute(self, replacements):
        out = Poly()
        for e, c in self.c.items():
            term = Poly(c)
            for i, degree in enumerate(e):
                term *= replacements.get(i, Poly.var(i)) ** degree
            out += term
        return out

    def record(self):
        return [{'exponents': list(e), 'coefficient': str(c)} for e, c in sorted(self.c.items())]


v = [Poly.var(i) for i in range(N)]
a, b, c, alpha, beta, gamma, d0, d1, d2 = v
X = [[0, a, b], [a, 0, c], [b, c, 0]]
U = [[d0, alpha, beta], [alpha, d1, gamma], [beta, gamma, d2]]
det = Poly()
for p in permutations(range(3)):
    term = Poly((-1) ** sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3)))
    for i in range(3):
        term *= X[i][p[i]]
    det += term
assert det == 2 * a * b * c
objective = sum((X[i][j] - U[i][j]) ** 2 for i in range(3) for j in range(3))
assert objective == d0 ** 2 + d1 ** 2 + d2 ** 2 + 2 * ((a-alpha) ** 2 + (b-beta) ** 2 + (c-gamma) ** 2)
gradient = [(a * b * c).derivative(i) for i in range(3)]
assert gradient == [b * c, a * c, a * b]
assert [objective.derivative(i) for i in range(3)] == [4 * (v[i] - v[i+3]) for i in range(3)]
components = []
for zero in range(3):
    free = [i for i in range(3) if i != zero]
    component_objective = objective.substitute({zero: Poly(0)})
    candidate = {i: (Poly(0) if i == zero else v[i+3]) for i in range(3)}
    for i in free:
        assert component_objective.derivative(i).substitute(candidate) == 0
        for j in free:
            assert component_objective.derivative(i).derivative(j) == (4 if i == j else 0)
    point = [0 if i == zero else [1, 2, 3][i] for i in range(3)]
    substitutions = {i: Poly(x) for i, x in enumerate(point + [1, 2, 3, 1, 2, 3])}
    distance = objective.substitute(substitutions)
    assert distance == [16, 22, 32][zero]
    components.append({'zero_coordinate': zero, 'free_coordinates': free,
                       'restricted_Hessian': [[4, 0], [0, 4]],
                       'restricted_Hessian_determinant': 16,
                       'rational_coordinates': point,
                       'rational_distance': [16, 22, 32][zero]})

# Exact leading coefficients motivating a future smoothness obstruction.
# This does not construct the required localization maps or lifting diagram.
e, A, B, C, c0 = v[:5]
axis_product = (e + A * e**2) * (e + B * e**2) * (c0 + C * e**2)
assert Poly({k: q for k, q in axis_product.c.items() if k[0] < 3}) == c0 * e**2
origin_product = (e + A * e**3) * (e + B * e**3) * (e + C * e**3)
assert Poly({k: q for k, q in origin_product.c.items() if k[0] < 4}) == e**3

print(json.dumps({'status': 'PASS',
                  'scope': 'Exact symbolic/numerical statement diagnostics only, not a smoothness or generic-count proof and not a Lean certificate',
                  'variables': ['a','b','c','alpha','beta','gamma','d0','d1','d2'],
                  'determinant': det.record(), 'distance': objective.record(),
                  'constraint_gradient': [g.record() for g in gradient],
                  'component_checks': components,
                  'future_lift_obstruction_leading_coefficients': {'axis_mod_e3': 'c0*e^2', 'origin_mod_e4': 'e^3'},
                  'actual_geometric_claims_proved': False,
                  'lean_proof_implemented': False}, indent=2))
