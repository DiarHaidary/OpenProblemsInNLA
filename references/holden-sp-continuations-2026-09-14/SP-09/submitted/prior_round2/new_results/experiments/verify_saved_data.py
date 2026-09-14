"""Audit saved block constructions; no numerical base value is a lower bound.

A construction whose exact denominator is one is already a base-size witness.
Such a construction is compared with, and may improve, the saved base witness;
it cannot be evidence of an amplification advantage.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import argparse
import json
import math
import numpy as np


def check(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def run(report: Path | None = None) -> dict:
    root = Path(__file__).resolve().parent
    rows = [json.loads(s) for s in (root / 'results/results.jsonl').read_text().splitlines()]
    reports = []
    for row in rows:
        case, n = row['case'], row['n']
        with np.load(root / f'results/case_{case:03d}.npz') as z:
            a, b, M, weights, baseU = (z[name] for name in ('a', 'b', 'M', 'weights', 'baseU'))
            check(a.shape == b.shape == (n,) and baseU.shape == (n, n), 'Base dimensions mismatch.')
            check(np.array_equal(M, M.astype(int)), 'Incidence matrix is not integral.')
            fractions = [Fraction(float(x)).limit_denominator(10**6) for x in weights[:, 1]]
            ids = [int(x) for x in weights[:, 0]]
            check(len(ids) == len(set(ids)) == len(row['fractional_support']), 'Support inventory mismatch.')
            check(all(x > 0 for x in fractions), 'Nonpositive support weight.')
            k = math.lcm(*(x.denominator for x in fractions))
            multiplicities = [int(k*x) for x in fractions]
            for r in range(2*n):
                check(sum(int(M[r, j])*x for j, x in zip(ids, fractions)) == 1,
                      f'Exact marginal failed in case {case}.')
            check(np.linalg.norm(baseU.conj().T @ baseU - np.eye(n), 2) < 1e-10,
                  'Base unitarity failed.')
            base = float(np.linalg.norm((a[:, None] - b[None, :])*baseU, 2))
            check(abs(base-row['base_upper']) < 1e-10, 'Saved base objective mismatch.')
            values, dimension = [], 0
            replacement = np.zeros((n, n), complex) if k == 1 else None
            for j, weight, copies, description in zip(ids, fractions, multiplicities, row['fractional_support']):
                I, J, described_weight, described_value = description
                U = z['block_'+str(j)]
                d = len(I)
                check(abs(float(weight)-described_weight) < 1e-10, 'Support weight mismatch.')
                check(U.shape == (d, d) and len(J) == d, 'Block dimension mismatch.')
                check(np.linalg.norm(U.conj().T @ U - np.eye(d), 2) < 1e-10, 'Block unitarity failed.')
                incidence = np.zeros(2*n, dtype=int)
                for i in I:
                    incidence[i] += 1
                for i in J:
                    incidence[n+i] += 1
                check(np.array_equal(incidence, M[:, j]), 'Block labels and incidence matrix disagree.')
                value = float(np.linalg.norm((a[I, None]-b[None, J])*U, 2))
                check(abs(value-described_value) < 1e-9, 'Described block value mismatch.')
                values.append(value)
                dimension += d*copies
                if replacement is not None:
                    check(copies == 1, 'Unexpected repeated block in a denominator-one construction.')
                    replacement[np.ix_(I, J)] = U
            check(dimension == n*k, 'Amplified direct-sum dimension mismatch.')
            amplified = max(values)
            check(abs(amplified-row['fractional_amplified_upper']) < 1e-9, 'Saved block objective mismatch.')
            raw_gap = base-amplified
            check(abs(raw_gap-row['candidate_gap']) < 1e-9, 'Saved candidate-gap mismatch.')
            replacement_value = None
            best_base = base
            if replacement is not None:
                check(np.linalg.norm(replacement.conj().T @ replacement - np.eye(n), 2) < 1e-10,
                      'Assembled base-dimension witness is not numerically unitary.')
                replacement_value = float(np.linalg.norm((a[:, None]-b[None, :])*replacement, 2))
                check(abs(replacement_value-amplified) < 1e-9, 'Assembled base objective mismatch.')
                best_base = min(base, replacement_value)
            reports.append({
                'case': case, 'n': n,
                'amplification_k_from_exact_multiplicities': k,
                'comparison_type': 'base-dimension construction' if k == 1 else 'amplified construction',
                'saved_base_feasible_value': base,
                'block_construction_value': amplified,
                'raw_candidate_gap': raw_gap,
                'base_dimensional_replacement_value': replacement_value,
                'best_available_base_feasible_value': best_base,
                'vetted_candidate_gap': best_base-amplified,
            })
    positive_raw = [r for r in reports if r['raw_candidate_gap'] > 1e-8]
    amplified_reports = [r for r in reports if r['amplification_k_from_exact_multiplicities'] >= 2]
    result = {
        'status': 'PASS: exact multiplicities and numerical matrix audits',
        'scope': 'Feasible constructions and numerical optimization outputs, not base lower-bound proofs.',
        'cases': len(reports),
        'base_dimensions': sorted({r['n'] for r in reports}),
        'largest_construction_k': max(r['amplification_k_from_exact_multiplicities'] for r in reports),
        'max_raw_candidate_gap': max(r['raw_candidate_gap'] for r in reports),
        'raw_positive_cases_above_1e-8': [r['case'] for r in positive_raw],
        'all_raw_positive_cases_are_base_dimensional': all(r['amplification_k_from_exact_multiplicities'] == 1 for r in positive_raw),
        'max_vetted_candidate_gap': max(r['vetted_candidate_gap'] for r in reports),
        'max_gap_for_k_at_least_two': max((r['raw_candidate_gap'] for r in amplified_reports), default=None),
        'vetted_positive_candidates_above_1e-8': sum(r['vetted_candidate_gap'] > 1e-8 for r in reports),
        'reports': reports,
    }
    if report:
        Path(report).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'reports'}, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json-report', type=Path)
    args = parser.parse_args()
    run(args.json_report)
