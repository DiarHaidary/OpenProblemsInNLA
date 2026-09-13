"""Algebra and implementation checks for the averaged rank-one upper bound."""
import math
import unittest
import numpy as np
from scipy.integrate import quad
from src.weighted_krylov import (
    CountingTwoSidedOracle, shifted_rank_one_parameters, shifted_rank_one_filter,
    wishart_resolvent_terms,
)

class ShiftedRankOneTests(unittest.TestCase):
    def test_gaussian_field_divergence(self):
        rng=np.random.default_rng(160613)
        for r in (1,2,4):
            g=rng.normal(size=(r,r+1)); t=.7; ans=wishart_resolvent_terms(g,t)
            derivative=0.; step=1e-6
            for i in range(r):
                for j in range(r+1):
                    plus=g.copy(); minus=g.copy(); plus[i,j]+=step; minus[i,j]-=step
                    fp=np.linalg.solve(plus@plus.T+t*np.eye(r),plus)
                    fm=np.linalg.solve(minus@minus.T+t*np.eye(r),minus)
                    derivative+=(fp[i,j]-fm[i,j])/(2*step)
            self.assertAlmostEqual(derivative,ans['gaussian_field_divergence'],places=7)

    def test_scalar_exact_resolvent_integral(self):
        for t in (.01,.2,1.,10.):
            mean=quad(lambda w:math.exp(-w/2)/(2*(w+t)),0,np.inf,epsabs=1e-11)[0]
            square=quad(lambda w:math.exp(-w/2)/(2*(w+t)**2),0,np.inf,epsabs=1e-11)[0]
            self.assertAlmostEqual(t*mean+2*t*square,1.,places=9)
            self.assertLessEqual(mean,1/math.sqrt(t))

    def test_exponential_wall_translation(self):
        # For determinant exponent zero, translating the full Gram matrix
        # changes the unnormalized density by precisely exp(-r*h/2).
        rng=np.random.default_rng(113)
        for r in (1,2,5):
            g=rng.normal(size=(r,r+1)); w=g@g.T; h=.3
            log_ratio=-np.trace(w+h*np.eye(r))/2+np.trace(w)/2
            self.assertAlmostEqual(log_ratio,-r*h/2,places=12)

    def test_budget_scale_all_grid_branches(self):
        branches=set()
        for n in (8,32,256,1024,10**6,10**12):
            for e in (1e-60,1e-24,1e-12,1e-6,.01,1/16):
                info=shifted_rank_one_parameters(n,e); branches.add(info['branch'])
                self.assertLessEqual(info['queries'],n)
                self.assertLessEqual(info['queries'],5*info['F_scale']+1e-9)
        self.assertEqual(branches,{'exact_columns','shifted_ensemble_polynomial'})

    def test_scalar_cone_comparison(self):
        for e in np.geomspace(1e-10,1/16,30):
            b=1-4*e; tau=(1+e/2)*b; delta=1-tau*tau
            self.assertLessEqual(delta,8*e+1e-14)
            for u in np.linspace(0,b,15):
                mu=b-u; E=tau*tau-mu*mu
                self.assertGreaterEqual(E,(e+u)/4-1e-14)
            self.assertLessEqual(tau,(1+e)*(b-e/4)+1e-14)

    def test_exact_branch_output_and_query_count(self):
        n=8; a=np.diag(np.arange(1,n+1,dtype=float)); oracle=CountingTwoSidedOracle(a)
        z,info=shifted_rank_one_filter(oracle,1e-10,np.random.default_rng(4))
        self.assertEqual(info['branch'],'exact_columns')
        self.assertEqual(oracle.queries,n)
        self.assertAlmostEqual(abs(z[-1,0]),1.,places=13)

    def test_polynomial_branch_query_count(self):
        n=128; e=.05; a=np.diag(np.r_[1.,np.linspace(0,1-4*e,n-1)])
        oracle=CountingTwoSidedOracle(a)
        z,info=shifted_rank_one_filter(oracle,e,np.random.default_rng(14))
        self.assertEqual(info['branch'],'shifted_ensemble_polynomial')
        self.assertEqual(oracle.queries,info['degree'])
        self.assertAlmostEqual(float((z.T@z)[0,0]),1.,places=12)
        self.assertGreater(abs(z[0,0]),.999)

    def test_reject_invalid_parameters(self):
        for n,e in ((7,.01),(8,0),(8,.1),(8,float('nan'))):
            with self.assertRaises(ValueError):shifted_rank_one_parameters(n,e)
        with self.assertRaises(ValueError):wishart_resolvent_terms(np.eye(2),1.)
        with self.assertRaises(ValueError):wishart_resolvent_terms(np.ones((2,3)),0.)

if __name__=='__main__':unittest.main()
