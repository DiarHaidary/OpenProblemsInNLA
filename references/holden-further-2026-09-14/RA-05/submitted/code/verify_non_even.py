#!/usr/bin/env python3
"""Finite diagnostics for the non-even tensor lower bound (not a proof checker)."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import combinations
import argparse, json, math, platform
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import qr
ROOT=Path(__file__).resolve().parents[1]

def exact_middle(h,p):
    return Fraction(sum((-1)**j*math.comb(h//2,j)*abs(h-4*j)**p for j in range(h//2+1)), (2**h)*(h**p))
def mp_middle(h,p):
    return mp.fsum([(-1)**j*math.comb(h//2,j)*mp.power(abs(h-4*j),p) for j in range(h//2+1)])/(mp.power(2,h)*mp.power(h,p))
def integral_middle(h,p):
    T=mp.pi/2; ell=h//2
    def integrand(t):
        if t==0 or t==T: return mp.mpf(0)
        return mp.power(mp.sin(t)*mp.cos(t),ell)*mp.zeta(p+1,t/T)/mp.power(T,p+1)
    I=mp.quad(integrand,[0,T/4,T/2,3*T/4,T])
    Jp=-mp.pi/(2*mp.gamma(p+1)*mp.sin(mp.pi*p/2))
    return ((-1)**(ell//2))*I/(mp.power(h,p)*Jp)

def main(output):
    counts=Counter(); residuals={}
    def check(ok,cat,label):
        if not bool(ok): raise AssertionError(cat+': '+label)
        counts[cat]+=1
    def close(a,b,cat,label,tol=3e-10):
        err=float(np.linalg.norm(np.asarray(a)-np.asarray(b))/(1+np.linalg.norm(np.asarray(b))))
        residuals[cat]=max(residuals.get(cat,0.),err)
        check(err<=tol,cat,label)
    coeff_table=[]
    for p in [3,5,7,9,11]:
        for h in [8,12,16,20,24,32,48,64]:
            if h//2<=p: continue
            val=exact_middle(h,p)
            check(val!=0,'exact_fourier','odd integer coefficient nonzero')
            coeff_table.append({'h':h,'p':p,'coefficient':str(val)})
    for p in [2,4,6,8,10,12]:
        for h in [8,12,16,20,24,32,48,64]:
            if h//2>p: check(exact_middle(h,p)==0,'exact_fourier','even polynomial cutoff')
    mp.mp.dps=75
    spectral_rows=[]
    for ptext,h in [('2.1',12),('2.5',12),('3',12),('3.7',16),('3.999',16),('4.001',16),('4.5',16),('5',16),('5.5',16),('6.25',20),('7.5',24)]:
        p=mp.mpf(ptext); a=mp_middle(h,p); b=integral_middle(h,p); rel=abs(a-b)/abs(a)
        check(rel<mp.mpf('1e-50'),'fractional_integral','Fourier sum equals positive integral')
        Jp=-mp.pi/(2*mp.gamma(p+1)*mp.sin(mp.pi*p/2))
        lower=mp.power(2,-mp.mpf(h)/2)*mp.power(h,-p-mp.mpf('.5'))/(4*abs(Jp))
        check(abs(a)>=lower,'fractional_integral','proved lower estimate')
        check(mp.sign(a)==((-1)**(h//4))*mp.sign(Jp),'fractional_integral','sign identity')
        spectral_rows.append({'p':ptext,'h':h,'coefficient':mp.nstr(a,35),'relative_identity_residual':mp.nstr(rel,8),'ratio_to_lower_bound':mp.nstr(abs(a)/lower,15)})
    rng=np.random.default_rng(20260913); projection_rows=[]
    h=8; n=2**h
    signs=(1-2*((np.arange(n)[:,None]>>np.arange(h))&1)).astype(float)
    C=np.stack([np.prod(signs[:,S],axis=1) for S in combinations(range(h),h//2)])
    _,_,piv=qr(C,mode='economic',pivoting=True); selected=piv[:C.shape[0]//4]
    for p in [2.3,3.,3.9]:
        H=np.abs(signs@signs.T/h)**p; lam=float(n*mp_middle(h,mp.mpf(str(p))))
        close(C@H,lam*C,'projection','middle-layer eigenvalue')
        F=H[:,selected]; BF=lam*C[:,selected]/np.sqrt(n)
        sig=float(np.linalg.eigvalsh(F.T@F)[0]); bsig=float(np.linalg.eigvalsh(BF.T@BF)[0])
        check(sig+1e-10>=bsig and bsig>0,'projection','projection contraction and full column rank')
        projection_rows.append({'p':p,'h':h,'columns':len(selected),'sigma_min_squared':sig,'projected_sigma_min_squared':bsig})
    tensor_rows=[]
    for p in [2.3,3.,3.9,4.5,5.,6.25]:
        r,M,L,h,N,T=3,5,8,4,5,9
        U=rng.normal(size=(M,r)); U/=np.linalg.norm(U,axis=1)[:,None]
        Z=np.vstack([U,rng.normal(size=(L-M,r))]); Z/=np.linalg.norm(Z,axis=1)[:,None]
        V=rng.normal(size=(N,h)); V/=np.linalg.norm(V,axis=1)[:,None]
        Y=np.vstack([V,rng.normal(size=(T-N,h))]); Y/=np.linalg.norm(Y,axis=1)[:,None]
        G=np.abs(Z@U.T)**p; F=np.abs(Y@V.T)**p
        A=np.array([np.kron(u,v) for u in U for v in V]); Q=np.array([np.kron(z,y) for z in Z for y in Y])
        K=np.abs(Q@A.T)**p
        close(K,np.kron(G,F),'tensor','Kronecker evaluation matrix')
        W=rng.normal(size=(M,N)); W[rng.random((M,N))<.6]=0; Delta=W-1
        err=G@Delta@F.T
        close(err.reshape(-1),K@(W.reshape(-1)-1),'tensor','full error matrix identity')
        sg=np.linalg.svd(G,compute_uv=False)[-1]; sf=np.linalg.svd(F,compute_uv=False)[-1]
        check(np.linalg.norm(err)**2+1e-10>=sg**2*sf**2*np.linalg.norm(Delta)**2,'tensor','Frobenius spectral lower bound')
        check(np.linalg.norm(Delta)**2+1e-10>=np.count_nonzero(W==0),'tensor','omitted-row count')
        costs=(G@np.ones(M))[:,None]*(F@np.ones(N))[None,:]
        close(costs.reshape(-1),K@np.ones(M*N),'tensor','unweighted costs factorize')
        eps=float(np.max(np.abs(err)/costs))
        check(M*N-np.count_nonzero(W)<=eps**2*np.linalg.norm(costs)**2/(sg**2*sf**2)+1e-9,'tensor','finite support conversion')
        q=Q[3]; P=np.eye(r*h)-np.outer(q,q)
        close(np.linalg.norm(A-A@P,axis=1)**p,K[3],'tensor','actual hyperplane residual costs')
        tensor_rows.append({'p':p,'rows':M*N,'ambient_dimension':r*h,'query_rank':r*h-1,'core_sigma_min':float(sg),'noise_sigma_min':float(sf)})
    for h in [8,12,16,32,64,128,256,1024]:
        t=mp.pi/4+1/(4*mp.sqrt(h)); ratio=mp.sin(2*t)**(mp.mpf(h)/2)
        check(ratio>=mp.mpf(15)/16,'interval','middle-interval lower bound')
    parameters=[]
    for p in [2.1,3,4.1,5,7.5,10.25]:
        a=2*p+2; B=2.5*p+3; h0=8
        while h0/2<=p: h0+=4
        for loginv in [10,30,100,300,1000]:
            logtheta=math.log(1e-6) # illustrative, not a uniform theorem constant
            ok=lambda h: -2*loginv+h*math.log(2)+a*math.log(h)<=logtheta
            if not ok(h0): continue
            h=h0
            while ok(h+4): h+=4
            check(ok(h) and not ok(h+4),'parameters','maximal admissible h')
            check(h<=2*loginv/math.log(2),'parameters','logarithmic dimension')
            check(abs(B-((p/2)+a+1))<1e-12 and B>(p/2)-1,'parameters','log exponent and low-rank absorption')
            check(h*math.log(2)>logtheta-math.log(16)+2*loginv-a*math.log(h+4)-1e-10,'parameters','lower size from maximality')
            parameters.append({'p':p,'log_inverse_epsilon':loginv,'h':h,'log_exponent':B})
    result={'passed':True,'assertions':sum(counts.values()),'categories':dict(counts),'largest_scaled_residual_by_category':residuals,
            'details':{'exact_odd_coefficients':coeff_table,'fractional_integral_checks':spectral_rows,'projected_noise_checks':projection_rows,'tensor_checks':tensor_rows,'parameter_examples':parameters},
            'seed':20260913,'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mp.__version__,'mpmath_decimal_precision':75},
            'scope':'Finite algebra and numerical diagnostics, not formal or independent verification of the general proof or imported theorems.'}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--output',type=Path,default=ROOT/'results/non_even_verification.json')
    main(ap.parse_args().output)
