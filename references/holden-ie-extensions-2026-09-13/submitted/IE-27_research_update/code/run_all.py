#!/usr/bin/env python3
"""Recheck this archive's exact finite-stage claims; standard library only.

This is a finite verifier, NOT a solver/proof for arbitrary stage count.
Optional --stages selects a subset of the 66 supplied certificates.
"""
from __future__ import annotations
import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'prior_results'/'code'))
from verify import verify
import exact_q3
from exact_obstructions import complex_shift_obstruction, generic_matrix_obstruction


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stages', nargs='+', type=int)
    parser.add_argument('--output', type=Path, default=ROOT/'recheck')
    parser.add_argument('--skip-tests', action='store_true',
                        help='For split verification runs only; the default runs all tests.')
    args = parser.parse_args()
    paths = sorted(list((ROOT/'prior_results'/'certificates').glob('q*.json')) +
                   list((ROOT/'new_certificates').glob('q*.json')),
                   key=lambda p:int(p.stem[1:]))
    if args.stages:
        selected = set(args.stages)
        paths = [p for p in paths if int(p.stem[1:]) in selected]
        if {int(p.stem[1:]) for p in paths} != selected:
            parser.error('An explicitly requested stage has no supplied certificate.')
    args.output.mkdir(parents=True, exist_ok=True)
    if not args.skip_tests:
        suite = unittest.TestSuite([
            unittest.defaultTestLoader.loadTestsFromName('test_verify'),
            unittest.defaultTestLoader.loadTestsFromName('test_extensions')])
        with (args.output/'tests.txt').open('w', encoding='utf-8') as stream:
            result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        if not result.wasSuccessful():
            print('FAILED: regression tests; see tests.txt', file=sys.stderr)
            return 1
        text = io.StringIO()
        with contextlib.redirect_stdout(text):
            exact_q3.main()
        (args.output/'exact_q3.json').write_text(text.getvalue(), encoding='utf-8')
        other = {'status':'VERIFIED', 'complex_shift':complex_shift_obstruction(),
                 'generic_matrix':generic_matrix_obstruction()}
        (args.output/'exact_obstructions.json').write_text(json.dumps(other, indent=2)+'\n', encoding='utf-8')
    results, failed = [], False
    with (args.output/'verification.jsonl').open('w', encoding='utf-8') as log:
        for path in paths:
            try:
                result = verify(path)
            except (ValueError, ArithmeticError, KeyError, OSError, TypeError) as exc:
                result = {'q':int(path.stem[1:]), 'status':'FAILED', 'error':str(exc)}
                failed = True
            results.append(result)
            line = json.dumps(result, sort_keys=True)
            log.write(line+'\n')
            log.flush()
            print(line, flush=True)
    (args.output/'verified.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    summary = {'all_selected_certificates_passed':not failed,
               'selected_stages':[int(p.stem[1:]) for p in paths],
               'selected_certificate_count':len(paths),
               'complete_solution_of_IE27':False,
               'scope':'Only the explicitly listed stages; each covers every real mu>0.'}
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    return 1 if failed else 0

if __name__ == '__main__':
    raise SystemExit(main())
