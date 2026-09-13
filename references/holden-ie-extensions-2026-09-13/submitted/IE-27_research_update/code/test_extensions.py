#!/usr/bin/env python3
"""Regression tests for the new exact arithmetic checks; not an all-q proof."""
from fractions import Fraction as F
import unittest
from exact_obstructions import C6, Q6, complex_shift_obstruction, generic_matrix_obstruction


class ExtensionTests(unittest.TestCase):
    def test_complex_inverse(self):
        z = C6(Q6(F(2), F(1,3)), Q6(F(-1), F(2,5)))
        self.assertEqual(z/z, C6.of(1))

    def test_conjugation(self):
        z = C6(Q6(F(2), F(1,3)), Q6(F(-1), F(2,5)))
        self.assertEqual(z*z.conjugate(), C6.of(z.abs2()))

    def test_schur_necessary_condition_inside(self):
        z1 = C6(Q6.of(F(1,2)), Q6.of(F(1,4)))
        z2 = C6(Q6.of(F(-1,3)), Q6.of(F(1,5)))
        a, b = -z1-z2, z1*z2
        gap = (1-b.abs2())*(1-b.abs2())-(a-a.conjugate()*b).abs2()
        self.assertGreaterEqual(gap.bounds()[0], 0)

    def test_schur_necessary_condition_violation(self):
        z1, z2 = C6.of(F(3,2)), C6.of(F(1,3))
        a, b = -z1-z2, z1*z2
        gap = (a-a.conjugate()*b).abs2()-(1-b.abs2())*(1-b.abs2())
        self.assertGreater(gap.bounds()[0], 0)

    def test_generic_counterexample(self):
        out = generic_matrix_obstruction()
        self.assertEqual(out['status'], 'VERIFIED')
        self.assertIn('NOT a Radau counterexample', out['scope'])

    def test_complex_shift_counterexample(self):
        out = complex_shift_obstruction()
        self.assertEqual(out['status'], 'VERIFIED')
        self.assertEqual(out['mu'], '1/100+3i')
        self.assertIn('NOT an IE-27 counterexample', out['scope'])

    def test_zero_division_rejected(self):
        with self.assertRaises(ZeroDivisionError):
            _ = C6.of(1)/C6()

    def test_sqrt6_bracket(self):
        s = Q6(F(0), F(1))
        lo, hi = s.bounds()
        self.assertLess(lo*lo, 6)
        self.assertGreater(hi*hi, 6)


if __name__ == '__main__':
    unittest.main(verbosity=2)
