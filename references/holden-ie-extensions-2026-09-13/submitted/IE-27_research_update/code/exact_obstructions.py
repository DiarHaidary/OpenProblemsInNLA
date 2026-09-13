#!/usr/bin/env python3
"""Exact counterexamples to two EXTENSIONS of IE-27, not to IE-27 itself.

Standard library only. Uses Q(sqrt(6)) arithmetic from the recovered independent
q=3 checker. Mathematical decisions use rational bounds, not floating point.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'prior_results' / 'code'))
from exact_q3 import Q6, mat, mul, transpose, add, scale, determinant, require

@dataclass(frozen=True)
class C6:
    re: Q6 = Q6()
    im: Q6 = Q6()

    @staticmethod
    def of(x):
        return x if isinstance(x, C6) else C6(Q6.of(x))

    def __add__(self, other):
        other = C6.of(other)
        return C6(self.re + other.re, self.im + other.im)
    __radd__ = __add__

    def __neg__(self):
        return C6(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-C6.of(other))

    def __rsub__(self, other):
        return C6.of(other) - self

    def __mul__(self, other):
        other = C6.of(other)
        return C6(self.re*other.re-self.im*other.im,
                  self.re*other.im+self.im*other.re)
    __rmul__ = __mul__

    def conjugate(self):
        return C6(self.re, -self.im)

    def abs2(self):
        return self.re*self.re + self.im*self.im

    def __truediv__(self, other):
        other = C6.of(other)
        p = self*other.conjugate()
        d = other.abs2()
        return C6(p.re/d, p.im/d)

    def record(self):
        return {'real': self.re.record(), 'imaginary': self.im.record()}


def complex_shift_obstruction():
    s = Q6(F(0), F(1))
    b = mat([[F(4,5)-s/5, 0, 0],
             [F(9,50)+29*s/200, F(3,10)+3*s/40, 0],
             [F(4,9)-s/36, F(4,9)+s/36, F(1,9)]])
    n = mat([[0, -F(53,25)+76*s/75, F(16,25)-22*s/75],
             [0, 0, F(2,25)+3*s/25], [0,0,0]])
    eye = mat([[int(i==j) for j in range(3)] for i in range(3)])
    r = F(41,100)
    norm_margin = add(scale(r*r, eye), scale(-1, mul(transpose(n), n)))
    minors = []
    for k in range(1,4):
        d = determinant([row[:k] for row in norm_margin[:k]])
        require(d.bounds()[0] > 0, 'Could not prove ||N||_2 < 41/100')
        minors.append(d.record())
    mu = C6(Q6.of(F(1,100)), Q6.of(3))
    p = [[C6.of(int(i==j))+mu*b[i][j] for j in range(3)] for i in range(3)]
    y = [[C6() for _ in range(3)] for _ in range(3)]
    for j in range(3):
        for i in range(3):
            y[i][j] = (C6.of(n[i][j]) - sum((p[i][k]*y[k][j] for k in range(i)), C6())) / p[i][i]
    # First column is zero. Nonzero eigenvalues are roots of lambda^2+a lambda+b0.
    require(all(y[i][0] == C6() for i in range(3)), 'Zero column failed')
    a = -y[1][1]-y[2][2]
    b0 = y[1][1]*y[2][2]-y[1][2]*y[2][1]
    aa, bb = a/r, b0/(r*r)
    rhs = 1-bb.abs2()
    gap = (aa-aa.conjugate()*bb).abs2() - rhs*rhs
    require(rhs.bounds()[0] > 0, 'Schur necessary-condition branch failed')
    require(gap.bounds()[0] > F(27,100), 'Squared Schur violation did not exceed 27/100')
    return {'status':'VERIFIED', 'scope':'Complex-shift extension only; NOT an IE-27 counterexample',
            'q':3, 'mu':'1/100+3i', 'comparison_radius':'41/100',
            'claim':'rho((I+(1/100+3i) B)^-1 N) > 41/100 > ||N||_2',
            'norm_upper_bound_leading_minors':minors,
            'quadratic_a':a.record(), 'quadratic_b':b0.record(),
            'one_minus_abs_B_squared':rhs.record(),
            'squared_Schur_inequality_violation':gap.record()}


def generic_matrix_obstruction():
    b = [[F(1),F(0)],[F(5),F(1)]]
    l = [[F(1),F(0)],[F(-5),F(1)]]
    n = [[F(0),F(1,10)],[F(0),F(0)]]
    y = [[F(0),F(1,20)],[F(0),F(-1,8)]]
    p = [[F(int(i==j))+b[i][j] for j in range(2)] for i in range(2)]
    require([[sum(p[i][k]*y[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == n,
            '(I+B)Y=N failed')
    d = [[F(1),F(1,10)],[F(-5),F(1,2)]]
    u = [[F(int(i==j))+n[i][j] for j in range(2)] for i in range(2)]
    require([[sum(l[i][k]*u[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == d, 'D=L(I+N) failed')
    require([[sum(b[i][k]*l[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == [[F(1),F(0)],[F(0),F(1)]], 'B=L^-1 failed')
    h = [F(50),F(1)]
    sym = [[h[i]*d[i][j]+d[j][i]*h[j] for j in range(2)] for i in range(2)]
    require(sym == [[F(100),F(0)],[F(0),F(1)]], 'Weighted accretivity failed')
    require(F(1,8)>F(1,10), 'Radius violation failed')
    return {'status':'VERIFIED', 'scope':'Generic matrix extension only; NOT a Radau counterexample',
            'mu':'1', 'radius':'1/10', 'spectral_radius':'1/8',
            'B':[[str(v) for v in row] for row in b],
            'L':[[str(v) for v in row] for row in l],
            'N':[[str(v) for v in row] for row in n],
            'D':[[str(v) for v in row] for row in d],
            'Y':[[str(v) for v in row] for row in y],
            'positive_diagonal_metric':['50','1'], 'HD_plus_DT_H':['100','1']}


def main():
    print(json.dumps({'status':'VERIFIED', 'complex_shift':complex_shift_obstruction(),
                      'generic_matrix':generic_matrix_obstruction()}, indent=2))

if __name__ == '__main__':
    main()
