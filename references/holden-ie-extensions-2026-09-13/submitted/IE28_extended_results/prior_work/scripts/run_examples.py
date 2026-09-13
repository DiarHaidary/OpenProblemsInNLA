#!/usr/bin/env python3
"""Recompute the numerical checks delivered with the IE-28 recovery package.

No numerical residual below is an interval certificate. The universal n=2,3
existence statements are proved analytically in writeup.pdf, not by this grid.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import mpmath as mp
import sympy
from ie28 import solve_two, solve_three, refine_ansatz, diagnostics, nodes


def serial(obj):
    if isinstance(obj, mp.mpf):
        return mp.nstr(obj, 200)
    if isinstance(obj, dict):
        return {str(k): serial(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serial(v) for v in obj]
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-grid', action='store_true', help='Skip the 66-triple rational grid.')
    args = parser.parse_args()
    mp.mp.dps = 200
    started = time.perf_counter()
    records = []
    logs = []
    def say(s):
        print(s, flush=True)
        logs.append(s)

    two_cases = [(['0.1', '1'], 'two regular'),
                 (['0.999999999999', '1'], 'two clustered')]
    for c, label in two_cases:
        d = solve_two(c, dps=120)
        check = diagnostics(c, d)
        assert check['coefficient_error'] < mp.mpf('1e-100')
        records.append({'label': label, 'nodes': nodes(c), 'diagonal': d,
                        'classification': 'analytic two-stage construction; decimal approximation',
                        'diagnostics': check})
        say(f"PASS {label}: coefficient error {mp.nstr(check['coefficient_error'], 6)}")

    three_cases = [
        (['0.1', '0.5', '1'], 'three separated'),
        (['0.8', '0.9', '1'], 'three right clustered'),
        (['0.01', '0.02', '1'], 'three two small nodes'),
        (['0.001', '0.999', '1'], 'three mixed scales'),
        ([Fraction(1,3), Fraction(2,3), 1], 'three equally spaced'),
        (['0.999999999998', '0.999999999999', '1'], 'three extreme cluster'),
        (['1e-12', '0.999999999999', '1'], 'three extreme mixed scales'),
    ]
    for c, label in three_cases:
        sol = solve_three(c, dps=115)
        check = diagnostics(c, sol.diagonal)
        assert check['coefficient_error'] < mp.mpf('1e-70'), label
        assert check['nilpotency_power_relative'] < mp.mpf('1e-65'), label
        assert check['positive'] and check['ordered'] and check['inside_ansatz_box']
        records.append({'label': label, 'nodes': nodes(c), 'diagonal': sol.diagonal,
                        'theta': sol.theta, 'radius': sol.radius,
                        'endpoint_traces_minus_three': sol.endpoint_traces_minus_three,
                        'trace_residual': sol.trace_residual, 'iterations': sol.iterations,
                        'classification': 'analytic three-stage construction; decimal approximation',
                        'diagnostics': check})
        say(f"PASS {label}: coefficient error {mp.nstr(check['coefficient_error'],6)}, "
            f"relative N^3 norm {mp.nstr(check['nilpotency_power_relative'],6)}")

    # Seeds reconstructed from numerical output in the interrupted attempt.
    higher_cases = [
        (['0.1','0.3','0.6','1'], ['0.07075034','0.66044289','8.43032949'], 'four irregular'),
        ([Fraction(k,4) for k in range(1,5)], ['0.118960083725378','0.999891312629842','12.2621677714715'], 'four equally spaced'),
        ([Fraction(k,5) for k in range(1,6)], ['0.0643193398418871','0.444655125021281','2.49054763410725','32.5945395395211'], 'five equally spaced'),
        ([Fraction(k,6) for k in range(1,7)], ['0.0392282875970034','0.248177420216234','1.04217626133573','5.24854124673124','83.123100740365'], 'six equally spaced'),
        ([Fraction(k,7) for k in range(1,8)], ['0.0258915356','0.156673082','0.571372794','2.02033245','10.2616624','195.816605'], 'seven equally spaced'),
        (['0.01','0.02','0.03','0.04','1'], ['0.00403917','0.03124164','0.23373043','3.94560359'], 'five separated'),
    ]
    for c, seeds, label in higher_cases:
        sol = refine_ansatz(c, seeds, dps=100)
        check = diagnostics(c, sol['diagonal'])
        assert check['coefficient_error'] < mp.mpf('1e-80'), label
        records.append({'label': label, 'nodes': nodes(c), **sol,
                        'classification': 'UNCERTIFIED higher-stage numerical candidate',
                        'initial_alphas': seeds, 'diagnostics': check})
        say(f"PASS numerical candidate {label}: coefficient error "
            f"{mp.nstr(check['coefficient_error'],6)} (not an existence certificate)")

    grid = {'executed': not args.skip_grid}
    if not args.skip_grid:
        worst = mp.mpf(0)
        count = 0
        for a,b in combinations(range(1,13),2):
            c = [Fraction(a,13), Fraction(b,13), 1]
            sol = solve_three(c, dps=50)
            check = diagnostics(c, sol.diagonal)
            assert check['coefficient_error'] < mp.mpf('1e-40')
            assert check['ordered'] and check['inside_ansatz_box']
            worst = max(worst, check['coefficient_error'])
            count += 1
        grid.update({'node_rule': '(a/13,b/13,1), 1<=a<b<=12', 'count': count,
                     'worst_coefficient_error': worst, 'solver_requested_dps': 50,
                     'interpretation': 'regression testing, not a proof by sampling'})
        say(f"PASS rational grid: {count} triples; maximum coefficient error {mp.nstr(worst,6)}")

    # Basic rejection behavior is part of the reproducibility checks.
    bad_inputs = [[0, .5, 1], [.1, .1, 1], [1, .5, .1], [-1, .5, 1]]
    for c in bad_inputs:
        try:
            solve_three(c, dps=40)
        except ValueError:
            continue
        raise AssertionError(f'Invalid nodes accepted: {c}')
    say('PASS input validation: zero, repeated, unordered, and negative nodes rejected')

    # Cross-check the independent general ansatz Newton system against the
    # constructive solution, rather than just testing it on n>=4.
    reference = records[2]
    rr, th = reference['radius'], reference['theta']
    refined = refine_ansatz(reference['nodes'], [rr, rr/th], dps=100)
    distance = max(abs(a-b) for a,b in zip(refined['diagonal'], reference['diagonal']))
    assert distance < mp.mpf('1e-95')
    say(f'PASS independent n=3 ansatz refinement: diagonal difference {mp.nstr(distance,6)}')

    output = {'scope': 'n=2,3 proofs in writeup; n>=4 entries are numerical candidates only',
              'diagnostic_working_dps': mp.mp.dps, 'examples': records, 'three_stage_grid': grid,
              'elapsed_seconds': time.perf_counter()-started}
    (ROOT/'results'/'numerical_checks.json').write_text(json.dumps(serial(output),indent=2)+'\n')
    env = {'python': platform.python_version(), 'mpmath': mp.__version__, 'sympy': sympy.__version__,
           'platform': platform.platform()}
    try:
        import numpy, scipy
        env.update({'numpy': numpy.__version__, 'scipy': scipy.__version__})
    except ImportError:
        pass
    (ROOT/'results'/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    say(f"ALL NUMERICAL CHECKS PASSED in {output['elapsed_seconds']:.2f} seconds")
    (ROOT/'results'/'numerical_checks.txt').write_text('\n'.join(logs)+'\n')


if __name__ == '__main__':
    main()
