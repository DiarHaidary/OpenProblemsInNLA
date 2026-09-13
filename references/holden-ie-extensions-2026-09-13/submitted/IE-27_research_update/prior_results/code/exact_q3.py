#!/usr/bin/env python3
"""Independent exact three-stage proof in Q(sqrt(6)); standard library only."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import permutations
import json

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


# Both strict inequalities are checked by squaring rational numbers.
ROOT_LO, ROOT_HI = F(2449489, 10**6), F(2449490, 10**6)
require(0 < ROOT_LO*ROOT_LO < 6 < ROOT_HI*ROOT_HI, "Invalid sqrt(6) bracket")


@dataclass(frozen=True)
class Q6:
    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def of(value):
        return value if isinstance(value, Q6) else Q6(F(value))

    def __add__(self, other):
        other = Q6.of(other)
        return Q6(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q6(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-Q6.of(other))

    def __rsub__(self, other):
        return Q6.of(other) - self

    def __mul__(self, other):
        other = Q6.of(other)
        return Q6(self.a*other.a+6*self.b*other.b,
                  self.a*other.b+self.b*other.a)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a-6*self.b*self.b
        if norm == 0:
            raise ZeroDivisionError("Zero in Q(sqrt(6))")
        return Q6(self.a/norm, -self.b/norm)

    def __truediv__(self, other):
        return self*Q6.of(other).inverse()

    def __rtruediv__(self, other):
        return Q6.of(other)*self.inverse()

    def bounds(self):
        ends = (self.a+self.b*ROOT_LO, self.a+self.b*ROOT_HI)
        return min(ends), max(ends)

    def record(self):
        lo, hi = self.bounds()
        return {"rational_part": str(self.a), "sqrt6_coefficient": str(self.b),
                "lower_rational_bound": str(lo), "upper_rational_bound": str(hi)}


def mat(rows):
    return [[Q6.of(x) for x in row] for row in rows]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), Q6())
             for col in zip(*b)] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(t, a):
    return [[t*x for x in row] for row in a]


def determinant(a):
    n, total = len(a), Q6()
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = Q6.of((-1)**inv)
        for i in range(n):
            term = term*a[i][p[i]]
        total = total+term
    return total


def main():
    s = Q6(F(0), F(1))
    c = [(4-s)/10, (4+s)/10, Q6.of(1)]
    v = []
    for i in range(3):
        z = c[i]
        for j in range(3):
            if i != j:
                z = z*(c[i]-c[j])
        v.append(z)
    d = [[v[i]/(v[j]*(c[i]-c[j])) if i != j
          else (1/(2*c[i]) if i < 2 else Q6.of(5))
          for j in range(3)] for i in range(3)]
    b = mat([[F(4,5)-s/5, 0, 0],
             [F(9,50)+29*s/200, F(3,10)+3*s/40, 0],
             [F(4,9)-s/36, F(4,9)+s/36, F(1,9)]])
    n = mat([[0, -F(53,25)+76*s/75, F(16,25)-22*s/75],
             [0, 0, F(2,25)+3*s/25], [0, 0, 0]])
    eye = mat([[int(i == j) for j in range(3)] for i in range(3)])
    require(mul(b, d) == add(eye, n), "Factor identity B D = I+N failed")
    require(all(b[i][i].bounds()[0] > 0 for i in range(3)), "Nonpositive B diagonal")
    h = mat([[1, 0, 0], [0, F(6,5), -F(7,40)], [0, -F(7,40), F(23,20)]])
    t = F(4,25)
    hb = mul(h, b)
    matrices = {
        "H": h,
        "HB+B^T H": add(hb, transpose(hb)),
        "tH-N^T HN": add(scale(t,h), scale(-1,mul(transpose(n),mul(h,n)))),
        "I-N^T N": add(eye, scale(-1,mul(transpose(n),n)))
    }
    checks = {}
    for label, a in matrices.items():
        require(a == transpose(a), "Exact symmetry failed")
        checks[label] = []
        for k in range(1,4):
            z = determinant([row[:k] for row in a[:k]])
            require(z.bounds()[0] > 0, f"Nonpositive minor {label}, {k}")
            checks[label].append(z.record())
    vr = mat([[0], [1], [-1]])
    nv = mul(n, vr)
    gap = mul(transpose(nv), nv)[0][0] - t*mul(transpose(vr), vr)[0][0]
    require(gap.bounds()[0] > 0, "Rayleigh gap is not positive")
    w = mat([[0], [1], [-2]])
    bad = mul(transpose(w), mul(b, w))[0][0]
    require(bad.bounds()[1] < 0, "Accretivity counterexample failed")
    print(json.dumps({
        "status": "VERIFIED", "field": "Q(sqrt(6))",
        "sqrt6_bracket": [str(ROOT_LO), str(ROOT_HI)],
        "factor_identity": "B D = I+N verified exactly",
        "leading_principal_minors": checks,
        "Rayleigh_gap": gap.record(),
        "Euclidean_accretivity_counterexample": bad.record(),
        "conclusion": "For q=3 and every mu>0: rho((I+mu B)^-1 N) <= 2/5 < ||N||_2 < 1"
    }, indent=2))


if __name__ == "__main__":
    main()
