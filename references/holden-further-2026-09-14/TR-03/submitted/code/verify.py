#!/usr/bin/env python3
"""Finite verification suite, not formal certification of the universal proofs."""
from __future__ import annotations
import json, math, platform, time
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
import numpy as np
import scipy
import mpmath as mp
from tr03_tools import *
ROOT=Path(__file__).resolve().parent.parent
RNG=np.random.default_rng(20260913)
CHECKS=[]

def record(name,count,**details):
    CHECKS.append(dict(name=name,passed=True,instances=count,**details))
    print('PASS',name,':',count,flush=True)
def close(a,b,tol=3e-8):
    assert abs(a-b)<=tol*max(1.,abs(a),abs(b)),(a,b)
def ge(a,b,tol=3e-8):
    assert a>=b-tol*max(1.,abs(a),abs(b)),(a,b)

def clipping_checks():
    count=0
    for n in range(1,9):
        for raw in combinations_with_replacement([F(1,4),F(1),F(3),F(9)],n):
            v=tuple(reversed(raw))
            for q in range(n):
                a=clipping_threshold(v,q);tau=sum(v[q:])
                assert sum(max(F(0),z-a) for z in v[q:])<=q*a
                for b in (a,2*a,a+F(1,7)):
                    assert sum(min(z,b) for z in v[q:])>=tau-q*a
                count+=1
    record('exact rational clipping inequality',count)

def counting_checks():
    count=0
    for n in range(3,13):
        for _ in range(30):
            v=sorted([F(int(RNG.integers(1,30)),int(RNG.integers(1,12))) for _ in range(n)],reverse=True)
            for k in range(1,n-1):
                e=elementary(v,k);t=elementary(v,k+1)/e;u=elementary(v,k-1)/e;tau=sum(v[k:])
                assert sum(t/(z+t) for z in v[:k])<=tau*u<=tau/t
                for b in (v[k-1],t,sum(v)/n):
                    assert sum(z<=b for z in v[:k])<=tau*(b+t)/(t*t)
                count+=1
    record('exact spectral counting inequality',count)

def hollow_checks():
    count=0;worst=0.
    for n in range(2,16):
        for _ in range(12):
            ev=RNG.normal(size=n);B,Q=equal_diagonal(ev)
            error=max(np.linalg.norm(Q.T@Q-np.eye(n)),np.linalg.norm(B-Q.T@np.diag(ev)@Q),np.max(abs(B.diagonal()-ev.mean())))
            assert error<2e-10;worst=max(worst,float(error));count+=1
    record('real equal-diagonal construction',count,max_error=worst)

def harmonic_checks():
    count=0;worst=0.
    for n in range(4,9):
        for _ in range(4):
            ev=np.sort(np.exp(RNG.normal(size=n)))[::-1]
            for k in range(1,n-1):
                for r in range(k+1,n+1):
                    B,_=equal_diagonal(1/ev[:r]);K=np.zeros((n,n));K[:r,:r]=np.linalg.inv(B);K[r:,r:]=np.diag(ev[r:])
                    bound=ev[r:].sum()+r*(r-k)/np.sum(1/ev[:r])
                    for I in combinations(range(n),k):
                        value=nystrom_error(K,I);ge(value,bound);worst=min(worst,value-bound);count+=1
    record('harmonic-block bound for every subset',count,min_numeric_margin=worst)

def compression_checks():
    count=0
    for d in range(2,15):
        for m in range(1,d+1):
            q=d-m
            for _ in range(12):
                ev=np.sort(np.exp(RNG.normal(size=d)))[::-1];O=orthogonal(d,RNG);R=orthogonal(d,RNG)[:,:m]
                C=np.linalg.inv(R.T@O@np.diag(1/ev)@O.T@R)
                ge(np.trace(C),ev[q:].sum());ge(ev[0],np.linalg.eigvalsh(C)[-1])
                Z=orthogonal(m,RNG);E=R@Z@R.T+np.eye(d)-R@R.T
                C2=np.linalg.inv(R.T@E@O@np.diag(1/ev)@O.T@E.T@R)
                assert np.linalg.norm(C2-Z@C@Z.T)<2e-8*max(1.,np.linalg.norm(C))
                count+=1
    record('harmonic compression interlacing',count)
    record('harmonic compression conjugation equivariance',count)

def frame_checks():
    count=0;ordered=0;counter=0
    for n in range(4,17):
        for j in range(1,n):
            O=orthogonal(n,RNG);U=O[:,:j];Q=O[:,j:]
            for q in range(n-j):
                k=j+q;m=n-k;I=RNG.choice(n,k,replace=False);J=np.setdiff1d(np.arange(n),I)
                left=inverse_trace(np.eye(m)/n+(1-1/n)*Q[J]@Q[J].T)
                right=m-j+inverse_trace(np.eye(j)/n+(1-1/n)*U[I].T@U[I])
                close(left,right);count+=1
        j=n//2
        for _ in range(20):
            G=RNG.normal(size=(n,j));H=G.T@G;ev,O=np.linalg.eigh(H);ih=(O/np.sqrt(ev))@O.T
            W=G[RNG.choice(n,j,replace=False)];B=W.T@W;N=ih@B@ih
            assert np.all(np.linalg.eigvalsh(N)<=np.linalg.eigvalsh(B)/ev[0]+2e-10)
            if np.linalg.eigvalsh(B/ev[0]-N)[0]<-1e-9:counter+=1
            ordered+=1
    record('regularized complementary-frame identity',count)
    assert counter>0
    record('ordered eigenvalues instead of invalid Loewner comparison',ordered,
           counterexamples_to_stronger_false_statement=counter)

def finite_checks():
    count=0;singular=0
    for n in range(4,11):
        for k in range(2,n-1):
            for q in range(k):
                j=k-q;d=n-j;m=n-k
                for _ in range(3):
                    Q=orthogonal(n,RNG)[:,:d];sigma=np.exp(RNG.normal(size=d));B=Q@np.diag(1/sigma)@Q.T;P=np.eye(n)-Q@Q.T
                    a=float(np.exp(RNG.normal()))
                    for J in combinations(range(n),m):
                        J=np.array(J);H=B[np.ix_(J,J)];inf=inverse_trace(H);fin=inverse_trace(H+P[np.ix_(J,J)]/a)
                        ge(fin,a*inf/(a+inf) if np.isfinite(inf) else a);count+=1
    for m in range(2,10):
        for r in range(m):
            O=orthogonal(m,RNG);B=(O*np.r_[np.exp(RNG.normal(size=r)),np.zeros(m-r)])@O.T
            ge(inverse_trace(B+np.eye(m)/2),2.);singular+=1
    record('finite-to-infinite comparison',count)
    record('singular limiting block convention',singular)

def grouping_checks():
    spectra=0;posteriors=0
    for k,q,n in ((5,1,26),(5,0,23),(9,2,42),(9,1,41)):
        j=k-q
        for _ in range(8):
            sigma=np.sort(np.exp(RNG.normal(size=n-j)))[::-1];D=grouped_covariance(sigma,k,q,RNG,level=150.)
            assert np.linalg.norm(np.linalg.eigvalsh(D['full'])-np.sort(np.r_[np.full(j,150.),sigma]))<1e-8
            assert np.linalg.norm(D['T'].T@D['T']-np.eye(2*k))<1e-10
            assert np.linalg.norm(D['contrast']@D['T'])<1e-9
            ge(sigma[k+q],D['c'].max()-D['c'].min());spectra+=1
            for _ in range(35):
                I=RNG.choice(n,k,replace=False);val,J,Z,W,heavy,single=granted_posterior(D,I)
                K=D['reduced'];res=K-K[:,J]@np.linalg.pinv(K[np.ix_(J,J)],rcond=1e-12)@K[J,:]
                close(float(np.trace(D['U'].T@res@D['U'])),val,2e-7)
                original=nystrom_error(K,I,auxiliary_psd=True);granted=nystrom_error(K,J,auxiliary_psd=True)
                ge(nystrom_error(D['full'],I),original,3e-7);ge(original,granted,3e-7);ge(granted,val,3e-7)
                distinct=len(heavy)+len(single)
                if distinct>=j:
                    u=k-distinct;h=len(heavy);r=j-h;extra=q-u
                    assert 0<=h<=u<=q and 0<=extra and 3*extra<r
                    assert W.shape==(r+extra,r)
                    HZ=Z.T@D['H']@Z
                    limiting=float(np.trace(HZ@np.linalg.inv(W.T@(W/D['c'][single,None]))))
                    lower=np.linalg.eigvalsh(D['H'])[0]*D['c'].min()*inverse_trace(W.T@W)
                    ge(limiting,lower,5e-7)
                posteriors+=1
    record('grouped covariance exact prescribed spectrum',spectra)
    record('round-robin contrast spread',spectra)
    record('granted-information leading posterior identity',posteriors)
    record('PSD and additional-observation comparisons',posteriors)

def constants_checks():
    mp.mp.dps=100;delta=mp.exp(-256);a=delta/2**20;d0=2**20;c2=delta*a/64;A=128/c2;eps=mp.exp(-2048);c=eps*delta*a/1024
    net=mp.log(65)/2+mp.log(4*mp.e)/2+mp.log(delta)/4
    assert net<-60 and 2*mp.log(9)-128<-123
    assert A>4*d0 and c<1/(2*d0+1)
    assert c<=eps*c2/15 and c<=delta*a/16 and c<=1/(4*A)
    assert c2*(A-1)>100 and 3*c2*(A-1)>4*mp.log(2)+5
    assert (2-mp.log(3))/2*32**2>400
    ct=0
    for d in (d0,d0+1,2*d0,10*d0,10**9):
        p=int(mp.ceil(32*mp.sqrt(d)))
        for q in (0,1,d//7,d//3):
            v=max(q,1);R=d+v
            assert 2*(p+v)<=R and p<=33*mp.sqrt(d)
            ratio=2**19*(mp.mpf(R)/d)*(q+mp.sqrt(d))/(p+v)
            assert ratio>3;ct+=1
    record('analytic probability constants in high precision',ct,net_exponent=float(net),log_C=float(mp.log(16/c)),
           limitation='Analytic margins, not Monte Carlo verification of rare probabilities')
    for k in range(2,10000):
        assert (k+1)**2/k+(k+1)/math.sqrt(k)<=4*k
    record('finite-spectrum reduction scalar constants',9998)

def main():
    start=time.monotonic()
    for f in (clipping_checks,counting_checks,hollow_checks,harmonic_checks,compression_checks,frame_checks,finite_checks,grouping_checks,constants_checks):f()
    result=dict(all_checks_passed=True,check_groups=len(CHECKS),checks=CHECKS,seed=20260913,
                elapsed_seconds=time.monotonic()-start,
                environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__),
                limitations=['Finite tests do not prove universal statements.','No formal proof-assistant certification or independent peer review.','The sharp joint n,k order in TR-03 remains unestablished.'])
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Completed',len(CHECKS),'check groups.')
if __name__=='__main__':main()
