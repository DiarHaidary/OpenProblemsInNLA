"""Regression and intentional-corruption tests for the exact finite checks."""
import unittest
import sympy as S
import verify_analytic as v

class AnalyticChecks(unittest.TestCase):
    def test_linear_spanning_identity(self): self.assertEqual(v.check_finite_identity()['linear_coefficient_checks'],1680)
    def test_examples(self): self.assertEqual(len(v.check_examples()),3)
    def test_symbolic_real_algebra(self): self.assertEqual(v.check_real_algebra()['open_unitary_ball_radius'],'1/100')
    def test_coarse_identity(self): self.assertEqual(v.check_coarse_identity()['coarse_linear_checks'],24)
    def test_wrong_unitary_rejected(self):
        with self.assertRaises(ValueError): v.feature_unitary(S.eye(4)*2)
    def test_corrupt_identity_weight_rejected(self):
        Q=v.feature_perm(v.ID); w,_=v.weights(Q); w[v.ID]+=S.Rational(1,100)
        with self.assertRaises(ValueError): v.check_representation(Q,w)
    def test_corrupt_zero_weight_rejected(self):
        Q=v.feature_perm(v.ID); w,_=v.weights(Q); w[(0,1,3,2)]+=S.Rational(1,100)
        with self.assertRaises(ValueError): v.check_representation(Q,w)
    def test_corrupt_minor_rejected(self):
        Q=v.feature_perm(v.ID); w,_=v.weights(Q); Q[(0,1),(0,1)]+=1
        with self.assertRaises(ValueError): v.check_representation(Q,w)
    def test_f_range(self): self.assertEqual(set(x for row in v.all_f_values() for x in row),{0,1,2})
    def test_explicit_failures_survive_optimized_python(self):
        with self.assertRaises(ValueError): v.need(False,'deliberate failure')

if __name__ == '__main__': unittest.main()
