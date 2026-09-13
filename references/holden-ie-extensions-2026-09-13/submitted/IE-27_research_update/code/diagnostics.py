#!/usr/bin/env python3
"""Optional floating-point exploration. This script does NOT certify any stage.

Run from the extracted archive. Requires NumPy/SciPy; all proof verifiers in
this archive use only Python's standard library. Shift maxima below are only
maxima over the explicitly recorded grid, not maximization over a continuum.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import solve_triangular

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'prior_results' / 'code'))
from generate import stages


def diagnostic(q: int) -> dict:
    c, _, l, n = stages(q)
    b = solve_triangular(l, np.eye(q), lower=True)
    r = float(np.linalg.norm(n, 2))
    k = l @ (np.eye(q)-n@n.T/(r*r)) @ l.T
    k = (k+k.T)/2
    values, vectors = np.linalg.eigh(k)
    # Exact K is positive semidefinite. Clipping is ONLY a numerical device.
    root_k = (vectors*np.sqrt(np.maximum(values, 0)))@vectors.T
    criterion_min = float(np.linalg.eigvalsh(l+l.T+2*root_k)[0])
    peak_rho = peak_norm = peak_resolvent = 0.
    peak_mu = None
    shifts = q*np.logspace(-5, 3, 101)
    for mu in shifts:
        resolvent = solve_triangular(np.eye(q)+mu*b, np.eye(q), lower=True)
        y = resolvent@n
        rho_ratio = float(max(abs(np.linalg.eigvals(y)))/r)
        norm_ratio = float(np.linalg.norm(y, 2)/r)
        peak_resolvent = max(peak_resolvent, float(np.linalg.norm(resolvent, 2)))
        peak_norm = max(peak_norm, norm_ratio)
        if rho_ratio > peak_rho:
            peak_rho, peak_mu = rho_ratio, float(mu)
    return {'q':q, 'status':'NUMERICAL_ONLY', 'r':r,
            'sqrt_criterion_min_eigenvalue':criterion_min,
            'K_min_eigenvalue_before_roundoff_clipping':float(values[0]),
            'sampled_max_rho_over_r':peak_rho, 'sampled_peak_mu':peak_mu,
            'sampled_max_norm_over_r':peak_norm,
            'sampled_max_resolvent_norm':peak_resolvent,
            'shift_grid':{'formula':'q*logspace(-5,3,101)', 'count':len(shifts)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stages', nargs='+', type=int,
                        default=[2,3,4,8,16,32,64,80,96,128])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    records = []
    for q in args.stages:
        records.append(diagnostic(q))
        print(json.dumps(records[-1]), flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
