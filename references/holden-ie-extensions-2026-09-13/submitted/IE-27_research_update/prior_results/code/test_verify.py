#!/usr/bin/env python3
"""Regression and enclosure tests. The tests supplement, not replace, the proof."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import copy
import json
import random
import tempfile
import unittest
import verify as v

ROOT = Path(__file__).resolve().parents[1]


def contains(interval, value):
    return F(interval.lo, v.SCALE) <= value <= F(interval.hi, v.SCALE)


class IntervalTests(unittest.TestCase):
    def test_point_arithmetic(self):
        rng = random.Random(2703)
        for _ in range(200):
            a = F(rng.randint(-1000,1000), rng.randint(1,1000))
            b = F(rng.randint(-1000,1000), rng.randint(1,1000))
            x, y = v.I.rational(a.numerator,a.denominator), v.I.rational(b.numerator,b.denominator)
            self.assertTrue(contains(x, a))
            self.assertTrue(contains(x+y, a+b))
            self.assertTrue(contains(x-y, a-b))
            self.assertTrue(contains(x*y, a*b))
            self.assertTrue(contains(x.square(), a*a))
            if b:
                self.assertTrue(contains(x/y, a/b))

    def test_interval_extrema(self):
        pairs = [(-3,-1), (-2,4), (1,3), (0,0)]
        for a,b in pairs:
            x = v.I(a*v.SCALE,b*v.SCALE)
            square_vals = [F(a*a), F(b*b)] + ([F(0)] if a <= 0 <= b else [])
            self.assertTrue(all(contains(x.square(), z) for z in square_vals))
            if a > 0 or b < 0:
                self.assertTrue(contains(x.reciprocal(),F(1,a)))
                self.assertTrue(contains(x.reciprocal(),F(1,b)))
            for c,d in pairs:
                y = v.I(c*v.SCALE,d*v.SCALE)
                self.assertTrue(all(contains(x*y,F(z)) for z in [a*c,a*d,b*c,b*d]))

    def test_zero_division(self):
        with self.assertRaises(ArithmeticError):
            v.I(-1,1).reciprocal()
        with self.assertRaises(ZeroDivisionError):
            v.I.rational(1,0)

    def test_negative_denominator(self):
        self.assertTrue(contains(v.I.rational(2,-3), F(-2,3)))

    def test_polynomial_horner(self):
        for q in range(2,12):
            coeff = v.jacobi_coefficients(q)
            for m in range(1,8):
                x = F(m,8)
                expected = sum(F(a)*x**k for k,a in enumerate(coeff))
                actual = F(v.polynomial_numerator(coeff,m,3), 2**(3*(q-1)))
                self.assertEqual(expected,actual)
        self.assertEqual(v.jacobi_coefficients(2),[-1,3])
        self.assertEqual(v.jacobi_coefficients(3),[1,-8,10])

    def test_ldlt(self):
        positive = [[v.I.rational(x) for x in row] for row in [[2,1],[1,2]]]
        self.assertTrue(all(x.lo>0 for x in v.positive_ldlt(positive,"test")))
        for bad in [[[1,2],[2,1]],[[1,1],[1,1]]]:
            with self.assertRaises(ArithmeticError):
                v.positive_ldlt([[v.I.rational(x) for x in row] for row in bad],"bad")

    def test_two_stage_exact_entries(self):
        b,n,_ = v.radau_factors([v.I.rational(1,3),v.ONE])
        expected_b = [[F(2,3),F(0)],[F(3,4),F(1,4)]]
        expected_n = [[F(0),F(1,3)],[F(0),F(0)]]
        for i in range(2):
            for j in range(2):
                self.assertTrue(contains(b[i][j],expected_b[i][j]))
                self.assertTrue(contains(n[i][j],expected_n[i][j]))


class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'certificates/q003.json').read_text())

    def test_supplied_three_stage(self):
        self.assertEqual(v.verify(ROOT/'certificates/q003.json')['status'],'VERIFIED')

    def check_bad(self,data):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'bad.json'; path.write_text(json.dumps(data))
            with self.assertRaises((ValueError,ArithmeticError)):
                v.verify(path)

    def test_tampered_metric(self):
        d=copy.deepcopy(self.data);d['H_numerators'][0][0]=-10**8;self.check_bad(d)

    def test_tampered_rayleigh(self):
        d=copy.deepcopy(self.data);d['v_numerators']=[0,0,0];self.check_bad(d)

    def test_tampered_root(self):
        d=copy.deepcopy(self.data);d['node_brackets'][0]=['0','1'];self.check_bad(d)

    def test_nonsymmetric_metric(self):
        d=copy.deepcopy(self.data);d['H_numerators'][0][1]=1;self.check_bad(d)


if __name__=='__main__':
    unittest.main(verbosity=2)
