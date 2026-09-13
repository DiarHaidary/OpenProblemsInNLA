"""Reconstructed experimental complex homotopy tracker.

The start system has the n! permutations of (1,...,n). Tracking is NOT
certified and can jump, merge, miss endpoints, or suffer conditioning errors.
A rounded uniqueness count is not the number of mathematical solutions.
This script cannot certify nonexistence or exhaustiveness.
"""
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import json
import time
import numpy as np
from solve import invsimilar


class Poly:
    def __init__(self, c, target=None):
        self.c = np.array(c,float)
        self.n = n = len(c)
        K = invsimilar(c)*self.c
        self.subsets = [np.array(list(combinations(range(n),k)),int) for k in range(1,n+1)]
        self.coeff = [np.array([np.linalg.det(K[np.ix_(ii,ii)]) for ii in ss])/comb(n,k)
                      for k,ss in enumerate(self.subsets,1)]
        self.rhs = (np.ones(n) if target is None else
                    np.array([sum(np.prod(np.array(target)[ii]) for ii in ss)/comb(n,k)
                              for k,ss in enumerate(self.subsets,1)]))

    def fj(self, x, coeff=None, rhs=None):
        if coeff is None:
            coeff = self.coeff
        if rhs is None:
            rhs = self.rhs
        n = self.n
        f, J = -rhs.astype(complex), np.zeros((n,n),complex)
        for k,(ss,aa) in enumerate(zip(self.subsets,coeff)):
            terms = aa*np.prod(x[ss],axis=1)
            f[k] += np.sum(terms)
            for j in range(n):
                hit = np.any(ss==j,axis=1)
                if abs(x[j]) > 1e-100:
                    J[k,j] = np.sum(terms[hit])/x[j]
                else:
                    for ii,a in zip(ss[hit],aa[hit]):
                        J[k,j] += a*np.prod(x[ii[ii!=j]])
        return f,J


def track(p, x, start_coeff, start_rhs, gamma=np.exp(.7j), mint=1e-10, maxstep=.05):
    x, t, step, count = x.astype(complex), 0., .005, 0
    def calc(t,x):
        coeff = [t*a+(1-t)*gamma*b for a,b in zip(p.coeff,start_coeff)]
        rhs = t*p.rhs+(1-t)*gamma*start_rhs
        return p.fj(x,coeff,rhs)
    while t < 1:
        count += 1
        if count > 20000:
            return None,('too many steps',t)
        step = min(step,1-t)
        f,J = calc(t,x)
        cd = [a-gamma*b for a,b in zip(p.coeff,start_coeff)]
        rd = p.rhs-gamma*start_rhs
        dH,_ = p.fj(x,cd,rd)
        try:
            v = np.linalg.solve(J,-dH)
        except np.linalg.LinAlgError:
            return None,('singular predictor',t)
        xx, tt, ok = x+step*v, t+step, False
        for it in range(15):
            f,J = calc(tt,xx)
            try:
                dx = np.linalg.solve(J,-f)
            except np.linalg.LinAlgError:
                break
            xx += dx
            if np.linalg.norm(dx,ord=np.inf) < 2e-11*(1+np.linalg.norm(xx,ord=np.inf)):
                ok = True
                break
            if np.linalg.norm(xx,ord=np.inf) > 1e14:
                break
        if ok and np.linalg.norm(xx-x,ord=np.inf) < 2*(1+np.linalg.norm(x,ord=np.inf)):
            x,t = xx,tt
            if it < 5:
                step = min(maxstep,step*1.4)
            elif it > 10:
                step *= .7
        else:
            step *= .5
            if step < mint:
                return None,('minimum step reached',t,float(step))
    return x,('numerical endpoint',count)


def all_solutions(c):
    """Legacy name; returns tracked endpoints, NOT a certified complete set."""
    p = Poly(c)
    n = p.n
    sc = [np.ones(len(ss))/comb(n,k) for k,ss in enumerate(p.subsets,1)]
    sr = np.array([sum(np.prod(np.arange(1,n+1)[ii]) for ii in ss)/comb(n,k)
                   for k,ss in enumerate(p.subsets,1)])
    sols, fails = [], []
    for perm in permutations(range(1,n+1)):
        x,msg = track(p,np.array(perm),sc,sr)
        if x is None:
            fails.append((perm,msg))
        else:
            sols.append(x)
    return p,sols,fails


if __name__ == '__main__':
    c = [.1,.3,.6,1]
    started = time.perf_counter()
    p,sols,fails = all_solutions(c)
    residuals = [float(np.max(abs(p.fj(x)[0]))) for x in sols]
    unique = len({tuple(np.round(x,6)) for x in sols})
    print('Elapsed seconds:',time.perf_counter()-started)
    print('Tracked endpoints:',len(sols),'reported failures:',len(fails))
    print('Rounded distinct endpoints:',unique,'(NOT an exact solution count)')
    print('Maximum computed endpoint residual:',max(residuals,default=None))
    print('Failures:',fails)
    for x in sols:
        if max(abs(x.imag)) < 1e-7 and min(x.real) > 0:
            print('Nearly real positive candidate d:',x.real*np.array(c))
    print('Uncertified tracking only. No exhaustiveness or existence theorem follows.')
    report = {'scope':'uncertified complex path tracking; not complete root counting',
              'nodes':c,'endpoints_x_equals_d_over_c':[[[float(z.real),float(z.imag)] for z in x] for x in sols],
              'failures':fails,'computed_endpoint_residuals':residuals,
              'rounded_distinct_endpoint_count':unique}
    target = Path(__file__).resolve().parents[1]/'results'/'homotopy_example.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
