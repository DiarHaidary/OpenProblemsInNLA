#!/usr/bin/env python3
"""Propose finite-stage energy certificates. Acceptance by verify.py is required.

NumPy/SciPy calculations and the optimizer are only untrusted candidate-finders.
Root brackets are refined using integer sign evaluations. There is no guarantee
of finding a certificate for arbitrary q, nor any claim of an all-stage proof.
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.linalg import solve, solve_triangular
from scipy.optimize import minimize
from scipy.special import roots_jacobi, eval_legendre
from verify import jacobi_coefficients, polynomial_numerator


def stages(q: int):
    if q < 2:
        raise ValueError("q must be at least 2")
    c = np.r_[(roots_jacobi(q-1, 1, 0)[0]+1)/2, 1.]
    v = np.column_stack([eval_legendre(j, 2*c-1) for j in range(q)])
    jmat = np.column_stack([c] + [
        (eval_legendre(j+1, 2*c-1)-eval_legendre(j-1, 2*c-1))/(2*(2*j+1))
        for j in range(1, q)])
    a = solve(v.T, jmat.T).T
    d = solve(a, np.eye(q))
    l, u = np.zeros_like(d), np.eye(q)
    for j in range(q):
        l[j:, j] = d[j:, j]-l[j:, :j]@u[:j, j]
        if l[j, j] <= 0:
            raise ArithmeticError("Nonpositive numerical pivot")
        u[j, j+1:] = (d[j, j+1:]-l[j, :j]@u[:j, j+1:])/l[j, j]
    return c, a, l, u-np.eye(q)


def root_brackets(q: int, c: np.ndarray, bits: int = 256):
    coeff, s = jacobi_coefficients(q), 1 << bits
    out = []
    for i in range(q-1):
        previous = 0. if i == 0 else c[i-1]
        lo = int(float((previous+c[i])/2)*s)
        hi = int(float((c[i]+c[i+1])/2)*s)
        fl = polynomial_numerator(coeff, lo, bits)
        fh = polynomial_numerator(coeff, hi, bits)
        if fl == 0:
            out.append([str(lo), str(lo)])
            continue
        if fh == 0:
            out.append([str(hi), str(hi)])
            continue
        if fl*fh >= 0:
            raise ArithmeticError("Numerical guesses failed to bracket a root")
        while hi-lo > 1:
            mid = (lo+hi)//2
            fm = polynomial_numerator(coeff, mid, bits)
            if fm == 0:
                lo = hi = mid
                break
            if fl*fm < 0:
                hi, fh = mid, fm
            else:
                lo, fl = mid, fm
        out.append([str(lo), str(hi)])
    return out


def energy_candidate(q: int, l: np.ndarray, n: np.ndarray,
                     t: float, maxiter: int = 6000):
    b = q*solve_triangular(l, np.eye(q), lower=True)
    ii, jj = np.triu_indices(q)
    keep = jj-ii <= 1
    ii, jj = ii[keep], jj[keep]
    eye, margin = np.eye(q), 1e-3

    def unpack(z):
        h = np.zeros((q, q))
        h[ii, jj], h[jj, ii] = z, z
        return h

    def objective(z):
        h = unpack(z)
        ss = [h-eye, b.T@h+h@b-margin*eye, t*h-n.T@h@n-margin*eye]
        mats, value = [], 0.
        for s in ss:
            ev, vv = np.linalg.eigh(s)
            negative = np.minimum(ev, 0.)
            mats.append((vv*negative)@vv.T)
            value += float(negative@negative)
        g = 2*(mats[0]+b@mats[1]+mats[1]@b.T+t*mats[2]-n@mats[2]@n.T)
        return value, g[ii, jj]*np.where(ii == jj, 1., 2.)

    result = minimize(objective, eye[ii, jj], method="L-BFGS-B", jac=True,
                      options={"maxiter": maxiter, "ftol": 1e-16,
                               "gtol": 1e-10, "maxcor": 100})
    h = unpack(result.x)
    low = [float(np.linalg.eigvalsh(s)[0]) for s in
           [h, h@b+b.T@h, t*h-n.T@h@n]]
    if min(low) <= 1e-6:
        raise ArithmeticError(f"No usable candidate: {result.message}; margins={low}")
    return h, {"iterations": int(result.nit), "objective": float(result.fun),
               "numerical_margins_H_qBH_Stein": low}


def generate(q: int, output: Path, root_bits: int = 256):
    start = time.monotonic()
    c, _, l, n = stages(q)
    _, singular, vt = np.linalg.svd(n)
    r = float(singular[0])
    h_den, v_den = 10**8, 10**8
    if q == 2:
        h = np.diag([1., 1.1])
        t_num, t_den, vector = 21, 200, np.array([0., 1.])
        info = {"kind": "explicit rational certificate"}
    elif q == 3:
        h = np.array([[1., 0., 0.], [0., 1.2, -7/40], [0., -7/40, 23/20]])
        t_num, t_den, vector = 4, 25, np.array([0., 1., -1.])
        info = {"kind": "explicit rational certificate"}
    else:
        t_den = 10**10
        t_num = int(np.floor(.998001*r*r*t_den))
        vector = vt[0]
        h, info = energy_candidate(q, l, n, t_num/t_den)
    data = {"format": "IE27-energy-v1", "q": q, "node_bits": root_bits,
            "node_brackets": root_brackets(q, c, root_bits),
            "H_denominator": h_den,
            "H_numerators": np.rint(h*h_den).astype(np.int64).tolist(),
            "t_numerator": t_num, "t_denominator": t_den,
            "v_denominator": v_den,
            "v_numerators": np.rint(vector*v_den).astype(np.int64).tolist(),
            "proposal_diagnostics_NOT_PROOF": dict(info, numerical_r=r,
                 numerical_radius_bound=(t_num/t_den)**.5)}
    output.mkdir(parents=True, exist_ok=True)
    path = output/f"q{q:03d}.json"
    path.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    return {"q": q, "path": str(path), "r_numerical": r,
            "seconds": round(time.monotonic()-start, 3), **info}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("q", nargs="+", type=int)
    parser.add_argument("--output", type=Path, default=Path("certificates"))
    parser.add_argument("--root-bits", type=int, default=256)
    args = parser.parse_args()
    for q in args.q:
        print(json.dumps(generate(q, args.output, args.root_bits)), flush=True)


if __name__ == "__main__":
    main()
