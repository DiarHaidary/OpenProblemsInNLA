"""Reconstructed exploratory NumPy/SciPy solver from the interrupted attempt.

NOT a certified existence test. Retains the exploratory parameterization and
root-finding strategy. The coefficient-order comment and output paths were
corrected during reconstruction. See ../src/ie28.py for the proved n=2,3 route.
"""
import numpy as np
from scipy.optimize import root
from math import comb, factorial


def invsimilar(c):
    c = np.array(c, float)
    dx = c[:, None] - c[None, :]
    np.fill_diagonal(dx, np.inf)
    M = 1 / dx
    np.fill_diagonal(M, 1 / c + M.sum(axis=1))
    return M


def coeffs(M):
    """Ascending coefficients [e_0,...,e_n] of det(I+tM)."""
    n = len(M)
    Q, es = np.eye(n), [1.]
    for k in range(1, n + 1):
        Q = M @ Q
        e = np.trace(Q) / k
        es.append(e)
        Q = e * np.eye(n) - Q
    return np.array(es)


def fun(x, c, M):
    n = len(c)
    d = c * np.exp(x)
    es = coeffs(M * d)
    return np.r_[[es[k] / comb(n, k) - 1 for k in range(1, n)],
                 sum(x) + np.log(factorial(n))]


def find(c, ntrial=20, rng=None):
    c = np.array(c, float)
    n, M = len(c), invsimilar(c)
    if rng is None:
        rng = np.random.default_rng(19)
    for j in range(ntrial):
        if j == 0:
            x = -np.log(factorial(n)) / n + .2 * (np.mean(np.log(c)) - np.log(c))
        else:
            x = -np.log(factorial(n)) / n + rng.normal(0, .5, n)
        with np.errstate(over='ignore', invalid='ignore'):
            rr = root(fun, x, args=(c, M), tol=1e-10)
            error = np.linalg.norm(fun(rr.x, c, M), ord=np.inf)
        if np.isfinite(error) and error < 1e-8:
            d = c * np.exp(rr.x)
            mat = np.stack([c**k - d*k*c**(k-1) for k in range(1,n+1)],axis=1)
            _, _, v = np.linalg.svd(mat)
            if abs(v[-1,-1]) < np.finfo(float).eps:
                continue
            p = v[-1] / v[-1,-1]
            yield d, p, np.roots(p[::-1])


if __name__ == '__main__':
    for c in [[.1,.3,.6,1], [.2,.4,.6,.8,1]]:
        print('nodes', c)
        for d, p, rp in find(c, ntrial=3):
            print('candidate d', d, 'eigenpolynomial nonzero roots', rp)
    print('All reported values are uncertified numerical candidates.')
