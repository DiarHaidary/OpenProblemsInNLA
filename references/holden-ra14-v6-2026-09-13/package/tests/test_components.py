"""Finite component checks, not a proof of any all-adaptive lower bound."""
from __future__ import annotations
import math
import unittest
import mpmath as mp
import numpy as np
from scipy.linalg import null_space
from src.weighted_krylov import (
    chebyshev_geometry, hard_spectrum, split_gaussian, interpolation_budget,
    chebyshev_feature_blocks, numerical_cone_optimum, graph_residual_and_cone,
    global_scales, full_block_upper_parameters, CountingTwoSidedOracle,
    full_normal_prefix, log_cosh,
)

class GeometryTests(unittest.TestCase):
    def test_lagrange_signs_and_sum(self):
        for d in (1,2,5,10):
            e=.023; g=chebyshev_geometry(d,e); a=1+2*e
            direct=[]
            for j,x in enumerate(g.nodes):
                other=np.delete(g.nodes,j)
                direct.append(np.prod((a-other)/(x-other)))
            direct=np.array(direct)
            self.assertTrue(np.all(direct*(-1.)**np.arange(d+1)>0))
            td=math.cosh(2*d*math.asinh(math.sqrt(e)))
            np.testing.assert_allclose(abs(direct)/td,g.normalized_lagrange_abs,rtol=2e-12)
            self.assertAlmostEqual(sum(abs(direct))/td,1,places=12)

    def test_polynomial_interpolation(self):
        rng=np.random.default_rng(51)
        for d in (1,3,9):
            e=.04; g=chebyshev_geometry(d,e); a=1+2*e
            coeff=rng.normal(size=(d+1,4))
            vals=np.polynomial.polynomial.polyval(g.nodes,coeff).T
            at=np.polynomial.polynomial.polyval(a,coeff)
            signed=g.normalized_lagrange_abs*(-1.)**np.arange(d+1)*math.exp(g.log_chebyshev_at_spike)
            np.testing.assert_allclose(signed@vals,at,rtol=1e-11,atol=1e-11)

    def test_nodal_denominator_identity(self):
        for d in (1,2,13,101):
            for e in (.0003,.12,.49):
                g=chebyshev_geometry(d,e); h=2*math.asinh(math.sqrt(e))
                delta=np.ones(d+1); delta[[0,-1]]=.5
                j=np.arange(d+1)
                direct=np.sum(delta/(2*e+2*np.sin(np.pi*j/(2*d))**2))
                rhs=d/math.tanh(d*h)/math.sinh(h)
                self.assertAlmostEqual(direct/rhs,1,places=11)

    def test_small_accuracy_geometry_high_precision(self):
        mp.mp.dps=100
        for e in (1e-15,1e-35,1e-65):
            d=37; g=chebyshev_geometry(d,e); ee=mp.mpf(str(e)); a=1+2*ee; tau=1+ee
            raw=[]; weighted=[]
            for j in range(d+1):
                x=mp.cos(mp.pi*j/d); delta=mp.mpf('.5') if j in (0,d) else 1
                raw.append(delta/(a-x)); weighted.append(mp.sqrt(tau*tau-x*x))
            expected=mp.fsum(r*w for r,w in zip(raw,weighted))/mp.fsum(raw)
            self.assertAlmostEqual(g.weighted_lagrange_over_chebyshev/float(expected),1,places=12)

    def test_weighted_lagrange_bound(self):
        for d in (1,2,10,100,1000):
            for e in (1e-25,1e-8,.0002,.07,.49):
                g=chebyshev_geometry(d,e)
                self.assertLessEqual(g.weighted_lagrange_over_chebyshev,10*math.sqrt(e)*g.harmonic_number*(1+1e-13))

    def test_harmonic_and_growth_bounds(self):
        for d in (1,3,11,1000):
            for e in (1e-20,.001,.49):
                g=chebyshev_geometry(d,e)
                self.assertLessEqual(g.harmonic_number,math.log(math.e*d)+1e-14)
                self.assertLessEqual(g.log_chebyshev_at_spike,2*d*math.sqrt(e)+1e-12)

    def test_allocation_probability(self):
        for d in (1,17,100):
            g=chebyshev_geometry(d,.008)
            self.assertTrue(np.all(g.allocation_weights>0))
            self.assertAlmostEqual(sum(g.allocation_weights),1,places=14)

    def test_log_cosh_stability(self):
        for x in (0,1e-12,1,100,10000):
            self.assertTrue(math.isfinite(log_cosh(x)))
            if x<100:
                self.assertAlmostEqual(log_cosh(x),math.log(math.cosh(x)),places=13)

class GaussianAndAllocationTests(unittest.TestCase):
    def test_reciprocal_moment_integration_constant(self):
        for m in range(8,100):
            bound=2500+5000*2**(-m/2)/(m/2-2)+(128/m)*math.exp(-2500*m/64)
            self.assertLess(bound,3000)

    def test_small_ball_net_constants(self):
        for b in (1,2,10,100):
            for ratio in (8,9,20):
                m=ratio*b
                for t in (1e-10,1e-4,.02):
                    log_net=(m+b)*math.log(3)+(m-2*b)*math.log(t)
                    target=(m/2)*math.log(25*t)
                    self.assertLessEqual(log_net,target)
                    self.assertLessEqual(3*m-m/(32*t*t),-m/(64*t*t))

    def test_top_gaussian_probability_constant(self):
        for a in (2,3,10,100):
            self.assertLess(2*math.exp(a*math.log(9)-100*a/8),.001)

    def test_integer_multiplicity_budget(self):
        for n,k,b,d in ((512,1,2,10),(2048,4,8,10),(4096,1,1,80)):
            spec=hard_spectrum(n,k,b,d,.002)
            self.assertEqual(spec.eigenvalues.shape,(n,))
            self.assertEqual(int(sum(spec.multiplicities)),n-k)
            self.assertTrue(np.all(spec.multiplicities>=8*b))
            self.assertTrue(np.all(spec.multiplicities>=(n-k)/2*spec.geometry.allocation_weights))
            self.assertAlmostEqual(sorted(abs(spec.eigenvalues),reverse=True)[k],1)

    def test_expected_allocation_objective(self):
        spec=hard_spectrum(2048,2,4,20,.003)
        g=spec.geometry
        lhs=float(np.sum(g.normalized_lagrange_abs**2*g.tail_weights/spec.multiplicities))
        rhs=2*g.weighted_lagrange_over_chebyshev**2/(spec.n-spec.k)
        self.assertLessEqual(lhs,rhs)

    def test_block_weighted_cauchy(self):
        rng=np.random.default_rng(73)
        spec=hard_spectrum(1024,2,3,12,.006)
        omega=rng.normal(size=(1024,3)); top,blocks=split_gaussian(omega,spec)
        g=spec.geometry; ell=g.normalized_lagrange_abs*(-1.)**np.arange(13)
        inv=[1/np.linalg.eigvalsh(v.T@v)[0] for v in blocks]
        s=float(np.sum(ell**2*g.tail_weights*np.array(inv)))
        for _ in range(12):
            vals=rng.normal(size=(13,3))
            left=np.linalg.norm(ell@vals)**2
            right=s*sum(np.linalg.norm(blocks[j]@vals[j])**2/g.tail_weights[j] for j in range(13))
            self.assertLessEqual(left,right*(1+1e-13))

    def test_validation_errors(self):
        for d,e in ((0,.1),(1,0),(1,.5),(1,float('nan'))):
            with self.assertRaises(ValueError):chebyshev_geometry(d,e)
        with self.assertRaises(ValueError):hard_spectrum(20,1,2,10,.1)
        with self.assertRaises(ValueError):hard_spectrum(512,1,1,5,1e-40)
        with self.assertRaises(ValueError):global_scales(2,2,.1)

class ConeAndPrefixTests(unittest.TestCase):
    def test_cone_residual_equivalence(self):
        rng=np.random.default_rng(44); nodes=np.linspace(-1,1,11); e=.03
        weights=(1+e)**2-nodes**2; delta=e*(2+3*e)
        f=rng.normal(size=(11,3))
        f/=np.linalg.norm(f/np.sqrt(weights[:,None]),2)*math.sqrt(delta)
        for scale in (.1,.99,1.01,3):
            ans=graph_residual_and_cone(e,nodes,scale*f)
            self.assertEqual(ans['residual']<=1+e,ans['cone_max']<=1)
            self.assertAlmostEqual(ans['cone_max'],scale**2,places=11)

    def test_weak_angle_is_not_a_good_pca_objective(self):
        for e in (1e-3,1e-6):
            a=1+2*e; tau=1+e
            c=math.sqrt(1-(tau/a)**2)
            z=np.array([c,math.sqrt(1-c*c),0.])
            matrix=np.diag([a,0.,1.])
            self.assertAlmostEqual(np.linalg.norm(matrix@(np.eye(3)-np.outer(z,z)),2),tau,places=12)
            self.assertLess(z@matrix@z/a,5*e)

    def test_features_reconstruct_direct_polynomial(self):
        rng=np.random.default_rng(67); spec=hard_spectrum(512,2,3,8,.009)
        omega=rng.normal(size=(512,3)); top,tail=chebyshev_feature_blocks(omega,spec)
        coeff=rng.normal(size=(9,3)); eig=spec.eigenvalues
        polys=np.polynomial.chebyshev.chebval(eig,coeff).T
        z=np.sum(omega*polys,axis=1)
        np.testing.assert_allclose(top@coeff.ravel(),z[:2],rtol=1e-10,atol=1e-9)
        allweights=np.repeat(spec.geometry.tail_weights,spec.multiplicities)
        np.testing.assert_allclose(tail@coeff.ravel(),z[2:]/np.sqrt(allweights),rtol=1e-10,atol=1e-8)

    def test_full_prefix_query_count(self):
        rng=np.random.default_rng(78); a=rng.normal(size=(20,20))/5
        omega=rng.normal(size=(20,4)); oracle=CountingTwoSidedOracle(a)
        blocks=full_normal_prefix(oracle,omega,3)
        self.assertEqual(oracle.queries,24)
        for i in range(4):
            np.testing.assert_allclose(blocks[i],np.linalg.matrix_power(a.T@a,i)@omega,rtol=1e-11,atol=1e-9)

    def test_polynomial_twice_uses_degree_twice(self):
        rng=np.random.default_rng(38); n=12; m=rng.normal(size=(n,n)); m=m.T@m/30
        omega=rng.normal(size=(n,3)); c=np.array([.3,-.5,.07,1.2])
        h=sum(c[i]*np.linalg.matrix_power(m,i) for i in range(4))
        cc=np.polynomial.polynomial.polymul(c,c)
        from_prefix=sum(cc[i]*np.linalg.matrix_power(m,i)@omega for i in range(7))
        np.testing.assert_allclose(from_prefix,h@h@omega,rtol=1e-11,atol=1e-11)

    def test_prefix_stabilizer_rotation(self):
        rng=np.random.default_rng(42); n=30
        r=np.linalg.qr(rng.normal(size=(n,n)))[0]; a=r@np.diag(np.linspace(-1,1.2,n))@r.T
        om=rng.normal(size=(n,2)); p=[om,a@om,a@a@om]
        w=np.linalg.qr(np.concatenate(p,axis=1),mode='reduced')[0]
        c=null_space(w.T); h=np.linalg.qr(rng.normal(size=(c.shape[1],c.shape[1])))[0]
        u=w@w.T+c@h@c.T; transformed=u@a@u.T
        for i in range(3):
            np.testing.assert_allclose(np.linalg.matrix_power(transformed,i)@om,p[i],atol=5e-13)
        z=np.linalg.qr(rng.normal(size=(n,2)),mode='reduced')[0]
        original=np.linalg.norm(a@(np.eye(n)-z@z.T),2)
        equiv=np.linalg.norm(transformed@(np.eye(n)-(u@z)@(u@z).T),2)
        self.assertAlmostEqual(original,equiv,places=12)

    def test_output_completion_geometry(self):
        rng=np.random.default_rng(77); n=40; k=3
        w=np.linalg.qr(rng.normal(size=(n,8)),mode='reduced')[0]
        z=np.linalg.qr(rng.normal(size=(n,k)),mode='reduced')[0]
        ext=z-w@(w.T@z); old,c=np.linalg.qr(ext,mode='reduced')
        g=rng.normal(size=(n,k)); fresh=np.linalg.qr(g-w@(w.T@g),mode='reduced')[0]
        zp=w@(w.T@z)+fresh@c
        np.testing.assert_allclose(zp.T@zp,np.eye(k),atol=1e-12)
        augmented=np.linalg.qr(np.concatenate([w,g],axis=1),mode='reduced')[0]
        self.assertLess(np.linalg.norm(zp-augmented@(augmented.T@zp)),1e-12)

    def test_projector_cannot_reveal_extra_range_directions(self):
        rng=np.random.default_rng(512); n=30; k=9; b=3
        u=np.linalg.qr(rng.normal(size=(n,k)),mode='reduced')[0]; p=u@u.T
        om=rng.normal(size=(n,b)); w=np.linalg.qr(np.concatenate([om,p@om],axis=1),mode='reduced')[0]
        self.assertEqual(np.linalg.matrix_rank(np.concatenate([om,p@om],axis=1)),2*b)
        self.assertLess(np.linalg.norm(p@w-w@(w.T@p@w)),1e-12)
        self.assertEqual(round(np.trace(p)-np.trace(w.T@p@w)),k-b)

    def test_small_finite_no_cone_diagnostic(self):
        rng=np.random.default_rng(20); n=512; e=(math.log(n)/n)**2
        spec=hard_spectrum(n,1,1,20,e); om=rng.normal(size=(n,1))
        ans=numerical_cone_optimum(om,spec); budget=interpolation_budget(om,spec)
        self.assertLess(ans['optimum_over_delta'],1)
        self.assertLessEqual(math.log(ans['max_top_over_weighted_tail']),budget['log_pathwise_cone_upper']+1e-10)
        # The practical example is deliberately NOT certified by the theorem's conservative constants.
        self.assertGreater(spec.log_analytic_condition,0)

class ParameterTests(unittest.TestCase):
    def test_threshold_at_48(self):
        def f(z):return math.log(6e9)+2*math.log(1+z)-.75*z
        self.assertLess(f(48),0)
        for z in (48,60,100,1000):
            self.assertLess(2/(1+z)-.75,0)
            self.assertLess(f(z),0)

    def test_depth_and_rounding_absorption(self):
        for z in (48,60,100):
            x=math.exp(z)
            for s in (1e-30,1e-10,.01,.7):
                d=math.floor(min(x/288,z/(16*s)))
                self.assertGreaterEqual(d,1)
                self.assertLessEqual(68*d,x/2)
                lhs=d; rhs=min(x,math.log(math.e*x)/s)/600
                self.assertGreaterEqual(lhs,rhs)
                logcond=math.log(6e9)-z+2*math.log(math.log(math.e*d))+4*d*s
                self.assertLessEqual(logcond,0)

    def test_width_monotonicity(self):
        for n in (10,100,10000):
            previous=0.
            for b in range(1,n+1):
                value=b*math.log(math.e*n/b)
                self.assertGreaterEqual(value+1e-11,previous); previous=value

    def test_upper_parameters_budget_bound(self):
        for n in (2,1000,10**7,10**12):
            for k in (1,min(5,n-1),max(1,n//3)):
                for e in (.49,.01,1e-8):
                    p=full_block_upper_parameters(n,k,e)
                    bound=24000*k/math.sqrt(e)*math.log(math.e*n/k)
                    self.assertLessEqual(p['queries'],n)
                    self.assertLessEqual(p['queries'],math.ceil(bound))
                    if p['branch']=='exact_columns':self.assertEqual(p['width'],n)
                    else:self.assertEqual(p['queries'],2*p['width']*p['degree'])

    def test_exact_scale_gap_formula(self):
        for n,k,e in ((1000,1,.01),(1000000,1,(math.log(1e6)/1e6)**2),(5000,3,1e-12)):
            f,u=global_scales(n,k,e); x=n/k; y=x*math.sqrt(e); ell=math.log(math.e*x)
            self.assertAlmostEqual(u/f,min(y,ell)/math.log1p(y),places=12)
            self.assertLessEqual(u/f,ell/math.log1p(ell)+1e-11)

    def test_counter_input_errors(self):
        with self.assertRaises(ValueError):CountingTwoSidedOracle(np.zeros((2,3)))
        oracle=CountingTwoSidedOracle(np.eye(3))
        with self.assertRaises(ValueError):oracle.product(np.zeros(3))
        with self.assertRaises(ValueError):full_normal_prefix(oracle,np.ones((3,1)),-1)
        self.assertEqual(oracle.queries,0)

if __name__=='__main__':unittest.main()
