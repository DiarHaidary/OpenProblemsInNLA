#!/usr/bin/env python3
"""Exact checks for the analytic round-five report. No optimizer is imported.

The quantified theorems are proved in report.tex. These checks verify all finite
linear identities on a spanning set, rational examples, and symbolic algebra.
They are not a proof-assistant verification of the unrestricted conjecture.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import sympy as S

PERMS = list(itertools.permutations(range(4)))
SUBS = [tuple(I) for k in range(5) for I in itertools.combinations(range(4), k)]
PAIRS = [(I, J) for I in SUBS for J in SUBS if len(I) == len(J)]
IDX = {p: j for j, p in enumerate(PERMS)}
ID = tuple(range(4))
K = [(1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0)]
CPLUS = [(0, 3, 1, 2), (2, 1, 3, 0), (3, 0, 2, 1), (1, 2, 0, 3)]
BETA = [
    ((2, 0, 3, 1), (0, 1), (0, 2)),
    ((1, 3, 0, 2), (0, 1), (1, 3)),
    ((3, 2, 0, 1), (0, 2), (0, 3)),
    ((2, 3, 1, 0), (0, 2), (1, 2)),
    ((1, 2, 3, 0), (0, 3), (0, 1)),
    ((3, 0, 1, 2), (0, 3), (2, 3)),
]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def indicator(p, I, J):
    return int(tuple(sorted(p[i] for i in I)) == tuple(J))


def feature_perm(p):
    return {(I, J): S.Integer(indicator(p, I, J)) for I, J in PAIRS}


def feature_unitary(U):
    need(U.shape == (4, 4), 'Matrix must be 4 by 4')
    need((U.conjugate().T * U - S.eye(4)).applyfunc(S.simplify) == S.zeros(4), 'Not exactly unitary')
    result = {}
    for I, J in PAIRS:
        d = U.extract(I, J).det() if I else S.Integer(1)
        result[I, J] = S.simplify(d * S.conjugate(d))
    return result


def tc(Q):
    t = sum(Q[(i,), (i,)] for i in range(4))
    c = Q[(0, 1), (0, 2)] + Q[(0, 1), (1, 3)] - Q[(0, 2), (0, 1)] - Q[(0, 2), (2, 3)]
    return S.simplify(t), S.simplify(c)


def weights(Q):
    t, c = tc(Q)
    h = -(t + c) / 4
    w = {p: S.Integer(0) for p in PERMS}
    w[ID] = -h
    for p, I in zip(K, [(0, 1), (0, 2), (0, 3)]):
        w[p] = Q[I, I] + h
    for i, p in enumerate(CPLUS):
        w[p] = Q[(i,), (i,)] + h
    for p, I, J in BETA:
        w[p] = Q[I, J]
    return {p: S.simplify(v) for p, v in w.items()}, S.simplify(h)


def check_representation(Q, w):
    for I, J in PAIRS:
        got = sum(w[p] * indicator(p, I, J) for p in PERMS)
        need(S.simplify(got - Q[I, J]) == 0, f'Minor coefficient mismatch: {I}, {J}')


def sign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))


def L(q):
    a, b, c, d = q
    return S.Matrix([[a,b,c,d],[-b,a,-d,c],[-c,d,a,-b],[-d,-c,b,a]])


def R(q):
    a, b, c, d = q
    return S.Matrix([[a,b,c,d],[-b,a,d,-c],[-c,-d,a,b],[-d,c,-b,a]])


def f(p):
    Q = feature_perm(p)
    t, c = tc(Q)
    return S.simplify((t + c) / 2)


def all_f_values():
    result = []
    for pi in PERMS:
        inverse = [pi.index(j) for j in range(4)]
        for eps in (-1, 1):
            row = []
            for p in PERMS:
                rel = tuple(inverse[p[i]] for i in range(4))
                t, c = tc(feature_perm(rel))
                row.append(S.simplify((t + eps * c) / 2))
            need(row.count(2) == 1 and row[IDX[pi]] == 2, 'Incorrect unique maximum')
            need(row.count(1) == 10 and row.count(0) == 13, 'Incorrect exceptional support')
            result.append(row)
    need(len({tuple(r) for r in result}) == 48, 'Duplicate exceptional functions')
    return result


def check_finite_identity():
    T = S.Matrix([[indicator(p, I, J) for p in PERMS] for I, J in PAIRS])
    B = S.Matrix([[sign(p) for p in PERMS]] +
                 [[sign(p) * int(p[i] == j) for p in PERMS] for i in range(3) for j in range(3)])
    need(T.shape == (70, 24), 'Wrong T shape')
    need(B.shape == (10, 24), 'Wrong B shape')
    need(B.rank() == 10 and T.rank() == 14, 'Unexpected ranks')
    need(T * B.T == S.zeros(70, 10), 'Kernel relation failed')
    for p in PERMS:
        Q = feature_perm(p)
        w, _ = weights(Q)
        check_representation(Q, w)
    basis = [ID] + K + CPLUS + [p for p, _, _ in BETA]
    need(len(set(basis)) == 14, 'Repeated basis permutation')
    rows = [((), ())] + [((i,), (i,)) for i in range(4)] + [(I, I) for I in [(0,1),(0,2),(0,3)]] + [(I, J) for _, I, J in BETA]
    M = S.Matrix([[indicator(p, I, J) for p in basis] for I, J in rows])
    need(abs(M.det()) == 6, 'Feature-basis determinant is not 6')
    all_f_values()
    return {'rank_T': 14, 'rank_B': 10, 'linear_coefficient_checks': 1680,
            'basis_determinant_absolute_value': 6, 'exceptional_functions': 48}


def check_examples():
    U0 = L([S.Rational(x, 7) for x in (1,4,4,4)])
    H = L([S.Rational(1,2)] * 4)
    c = S.Rational(9999,10001)
    s = S.Rational(200,10001)
    G = S.eye(4)
    G[0,0] = G[1,1] = c
    G[0,1] = G[1,0] = S.I*s
    V = G*U0
    output = []
    for name, U in [('quaternion_U0', U0), ('Hadamard_H', H), ('complex_V', V)]:
        Q = feature_unitary(U)
        w, h = weights(Q)
        check_representation(Q, w)
        need(sum(w.values()) == 1, 'Weights do not sum to one')
        if h > 0:
            need([p for p in PERMS if w[p] < 0] == [ID], 'More than the prescribed negative weight')
        if name == 'quaternion_U0':
            need(h == S.Rational(79,2401), 'Wrong U0 obstruction')
        if name == 'Hadamard_H':
            need(all(v >= 0 for v in w.values()), 'Hadamard weights are not convex')
            need(sorted(v for v in w.values() if v) == [S.Rational(1,8)]*8, 'Wrong Hadamard weights')
        if name == 'complex_V':
            need(h == S.Rational(7881760079,240148022401), 'Wrong complex obstruction')
            invariant = S.simplify(S.im(U[0,0]*U[2,1]*S.conjugate(U[0,1])*S.conjugate(U[2,0])))
            need(invariant == S.Rational(543945600,240148022401), 'Wrong phase invariant')
        output.append({'name':name, 'h':str(h),
                       'weights': [{'permutation':[i+1 for i in p], 'weight':str(w[p])} for p in PERMS if w[p]],
                       'minor_equalities':70})
    return output


def check_real_algebra():
    q = S.symbols('q0:4', real=True)
    r = S.symbols('r0:4', real=True)
    U = L(q)*R(r)
    t = S.expand(sum(U[i,i]**2 for i in range(4)))
    need(S.expand(t-4*sum(q[i]**2*r[i]**2 for i in range(4))) == 0, 'Diagonal identity failed')
    chi_terms = [((0,1),(0,2),1),((0,1),(1,3),1),((0,2),(0,1),-1),((0,2),(2,3),-1)]
    c = sum(e*U.extract(I,J).det()**2 for I,J,e in chi_terms)
    target = 8*(sum(x*x for x in q)**2*S.prod(r)-sum(x*x for x in r)**2*S.prod(q))
    need(S.expand(c-target) == 0, 'Orthogonal chirality identity failed')
    x,z,u = S.symbols('x z u')
    g = 16*x**3-24*x**2+36*x-1
    cubic = 32*z**3+48*z**2+28*z-1
    need(S.factor(S.resultant(g,z*(1-4*x)-x-2*x**2,x)-216*cubic) == 0, 'Elimination identity failed')
    lo = S.Rational(33721124434,10**12)
    hi = S.Rational(33721124435,10**12)
    need(cubic.subs(z,lo) < 0 < cubic.subs(z,hi), 'Root bracket failed')
    need(S.expand(u*(u*u+3)-(1+3*u*u)-(u-1)**3) == 0, 'Stationary m=1 algebra failed')
    need(S.expand(u*(3+u*u)-(3*u*u+1)-(u-1)**3) == 0, 'Stationary m=3 algebra failed')
    # Conservative open-ball margins, using only rational inequalities.
    eps = S.Rational(1,100)
    need(S.Rational(1,8)-S.Rational(11,2)*eps >= S.Rational(3,100), 'Identity-weight radius bound failed')
    need(S.Rational(1,8)-7*eps >= S.Rational(3,100), 'Entry-weight radius bound failed')
    need(S.Rational(1,8)-S.Rational(19,2)*eps == S.Rational(3,100), 'Minor-weight radius bound failed')
    return {'symbolic_orthogonal_identities':2,
            'tau_star_bracket':['0.033721124434','0.033721124435'],
            'open_unitary_ball_radius':'1/100', 'eight_weight_lower_bound':'3/100'}


def check_coarse_identity():
    canon = [(0,1),(0,2),(0,3)]
    for p in PERMS:
        Q = feature_perm(p)
        t, _ = tc(Q)
        E = S.Matrix([[Q[I,J]+Q[I,tuple(i for i in range(4) if i not in J)] for J in canon] for I in canon])
        need(all(sum(E[i,j] for j in range(3)) == 1 for i in range(3)), 'Coarse row sum failed')
        need(all(sum(E[i,j] for i in range(3)) == 1 for j in range(3)), 'Coarse column sum failed')
        need(t+S.trace(E)-1 == sum(Q[I,I] for I in itertools.combinations(range(4),2)), 'Coarse trace identity failed')
    return {'coarse_linear_checks':24}


def run():
    return {'status':'PASS', 'full_MI05_resolved':False,
            'scope':'Exact finite and symbolic identities supporting the analytic report; not formal verification of its quantified theorems.',
            'linear':check_finite_identity(), 'examples':check_examples(),
            'real_algebra':check_real_algebra(), 'coarse':check_coarse_identity()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
