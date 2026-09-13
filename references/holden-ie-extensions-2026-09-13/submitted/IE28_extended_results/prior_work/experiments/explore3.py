"""Reconstructed three-variable elimination experiment; not exact root counting.

Real-root filters, denominators, and residual tolerances are heuristic. This
script is retained for reproducibility of the interrupted exploration, not as
the proof for all triples. Use ../src/ie28.py for the constructive method.
"""
import numpy as np
from numpy.polynomial import Polynomial as P
from solve import invsimilar, coeffs


def data(c):
    c = np.asarray(c, dtype=float)
    M = invsimilar(c)
    A = np.linalg.inv(M)
    return np.diag(M), np.diag(A), np.prod(c)/6


def solutions(c):
    h, a, g = data(c)
    h1, h2, h3 = h
    a1, a2, a3 = a
    Q = P([h2*a1*g, -3*h2*g, 3*a3, -a3*h1])
    R = P([-h3*a1*g, 3*h3*g, -3*a2, a2*h1])
    polynomial = Q*R-P([0,0,0,g*(h2*a2-h3*a3)**2])
    sol = []
    for x in polynomial.roots():
        if abs(x.imag) > 1e-6*max(1,abs(x.real)):
            continue
        x = x.real
        if x <= 0:
            continue
        denom = Q(x)
        if abs(denom) > 1e-14:
            y = -g*x*(h2*a2-h3*a3)/denom
            if y <= 0:
                continue
            z = g/(x*y)
            d = np.array([x,y,z])
            err = max(abs(h@d-3),abs(a@(1/d)-3))
            if err < 1e-3:
                sol.append(d)
        else:
            for y in np.roots([h2*x,h1*x*x-3*x,h3*g]):
                if abs(y.imag) < 1e-7 and y.real > 0:
                    y = y.real
                    z = g/(x*y)
                    d = np.array([x,y,z])
                    err = max(abs(h@d-3),abs(a@(1/d)-3))
                    if err < 1e-3:
                        sol.append(d)
    return sol, polynomial


if __name__ == '__main__':
    for c in [[.1,.5,1],[.8,.9,1],[.01,.02,1],[.001,.999,1]]:
        ss, _ = solutions(c)
        print('nodes',c,'accepted candidates',len(ss),'(not an exact count)')
        for d in ss:
            err = max(abs(coeffs(invsimilar(c)*d)-[1,3,3,1]))
            print('d',d,'coefficient residual',err)
