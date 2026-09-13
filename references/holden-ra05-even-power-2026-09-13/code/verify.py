"""Reproducible finite diagnostics for the even-power proof.

No finite test here substitutes for a quantified existence proof. In particular,
this suite does not implement the partial-coloring theorem, choose asymptotic
random cores with certified constants, or certify a globally optimal coreset.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
from math import factorial
import argparse,json,platform
import numpy as np
from even_features import (Features,sympower,multiindices,monomials,protected_indices,
                           protected_maps,query_polynomials,power,mul,coefficient_map)
from check_exact_certificate import check as exact_check

if not __debug__:
    raise RuntimeError('Run without -O; verification uses assertions.')

class Checks:
    def __init__(self): self.count=Counter(); self.max_residual=Counter()
    def true(self,category,condition):
        if not condition: raise AssertionError(category)
        self.count[category]+=1
    def close(self,category,a,b,tol=3e-7):
        a=np.asarray(a);b=np.asarray(b)
        scale=1+max(float(np.linalg.norm(a)),float(np.linalg.norm(b)))
        res=float(np.linalg.norm(a-b))/scale
        self.max_residual[category]=max(self.max_residual[category],res)
        self.true(category,res<tol)
    def le(self,category,a,b,tol=3e-7):
        self.true(category,float(a)<=float(b)+tol*(1+abs(float(a))+abs(float(b))))

def numerical_features(ck,rng):
    records=[]
    for s,k,q,n in ((2,2,2,35),(3,2,2,45),(4,2,2,55),(3,3,2,60),(5,2,2,65),(6,2,2,70)):
        B=rng.normal(size=(n,k))*.7
        C=rng.normal(size=(n,q));C/=np.maximum(np.linalg.norm(C,axis=1),1)[:,None]
        C*=rng.uniform(.35,.95,size=n)[:,None]
        omega=rng.uniform(.8,1.2,size=n);omega/=sum(omega)
        feat=Features(B,C,omega,s); K=feat.num_probabilities
        ck.close('density',sum(feat.pi),1)
        ck.le('density',max(omega/feat.pi),K)
        for l,E in feat.E.items():
            D=E.shape[1]
            ck.close('head_feature_isotropy',E.T@E,np.eye(D))
            ck.close('head_feature_trace',np.sum(E*E),D)
            ck.le('head_leverage',max(np.sum(E*E,axis=1)/feat.pi),K*D)
        for (j,t),F in feat.F.items():
            ck.close('mixed_feature_trace',np.sum(F*F),feat.h[j,t])
            # Use the n-by-n Gram matrix to avoid enormous ambient matrices.
            ck.le('mixed_feature_covariance',np.linalg.eigvalsh(F@F.T)[-1],1)
            ck.le('mixed_leverage',max(np.sum(F*F,axis=1)/feat.pi),K*feat.h[j,t])
        for trial in range(2):
            dim=k+q;U,_=np.linalg.qr(rng.normal(size=(dim,k)))
            P=(U*rng.uniform(.25,1,size=k))@U.T
            ev,vec=np.linalg.eigh(np.eye(dim)-P);Q=(vec*np.sqrt(np.maximum(ev,0)))@vec.T
            V,W=Q[:,:k],Q[:,k:];PC=P[k:,k:]
            vb=B@V.T;wc=C@W.T
            avec=np.sum(vb*vb,axis=1);xvec=np.sum(vb*wc,axis=1)
            rvec=np.einsum('ni,ij,nj->n',C,PC,C);r2=feat.r**2
            H=float(omega@avec**s)
            direct=np.sum((vb+wc)**2,axis=1)**s
            expansion=np.zeros(n)
            theta=rng.normal(size=n)
            for a,b,c,d in monomials(s):
                coeff=factorial(s)//(factorial(a)*factorial(b)*factorial(c)*factorial(d))*2**b*(-1)**c
                mono=avec**a*xvec**b*rvec**c*r2**d
                expansion+=coeff*mono
                if a>=1 and b+c>0:
                    LL,RR,indices=protected_maps(feat,V,W,PC,a,b,c,d)
                    l,nu,h,e,j,t=indices;E=feat.E[l];F=feat.F[j,t]
                    lhs=np.einsum('no,no->n',E@LL.T,F@RR.T)*feat.r**(2*d)
                    ck.close('protected_tensor_factorization',lhs,omega*mono)
                    Z=E.T@((theta*feat.r**(2*d))[:,None]*F)
                    ck.close('protected_trace_contraction',np.trace(LL@Z@RR.T),theta@(omega*mono))
                    ck.close('left_map_norm_identity',np.sum(LL*LL),omega@avec**l)
                    ck.le('right_map_norm_bound',np.sum(RR*RR),k**c*H**(j/s))
                    ck.le('query_nuclear_bound',abs(np.trace(LL@Z@RR.T)),
                          np.linalg.norm(Z,2)*np.linalg.norm(LL)*np.linalg.norm(RR))
                    if nu:
                        ck.true('odd_degree_operator_output',LL.shape[0]==dim and RR.shape[0]==dim)
                elif a==0 and b>=2:
                    b1=b//2;b2=b-b1;Ap,Xp,Rp,VB=query_polynomials(V,W,PC)
                    pp=power(Xp,b1,dim)
                    qq=mul(power(Xp,b2,dim),power(Rp,c,dim))
                    L=coefficient_map([pp],k,q,b1,b1)@np.kron(feat.Nroot[b1,b1],np.eye(len(multiindices(q,b1))))
                    R=coefficient_map([qq],k,q,b2,b2+2*c)@np.kron(feat.Nroot[b2,b2+2*c],np.eye(len(multiindices(q,b2+2*c))))
                    F1=feat.F[b1,b1];F2=feat.F[b2,b2+2*c]
                    vals=(F1@L.T).ravel()*(F2@R.T).ravel()*feat.r**(2*d)
                    ck.close('balanced_mixed_factorization',vals,omega*mono)
                    ck.le('balanced_left_query',np.sum(L*L),H**(b1/s))
                    ck.le('balanced_right_query',np.sum(R*R),k**c*H**(b2/s))
                elif a==0 and b==1:
                    Ap,Xp,Rp,VB=query_polynomials(V,W,PC)
                    z=coefficient_map([Xp],k,q,1,1)@np.kron(feat.Nroot[1,1],np.eye(q))
                    F1=feat.F[1,1]
                    if c==0:
                        val=(F1@z.T).ravel()*np.sqrt(omega)*feat.r**(2*d)
                    else:
                        pp=coefficient_map([power(Rp,c,dim)],k,q,0,2*c)
                        pp=pp@np.kron(feat.Nroot[0,2*c],np.eye(len(multiindices(q,2*c))))
                        val=(F1@z.T).ravel()*(feat.F[0,2*c]@pp.T).ravel()*feat.r**(2*d)
                        ck.le('anisotropic_query_length',np.sum(pp*pp),k**c)
                    ck.close('one_cross_factorization',val,omega*mono)
                    ck.le('one_cross_query_length',np.sum(z*z),H**(1/s))
            ck.close('complete_residual_expansion',expansion,direct)
            ck.close('direct_positive_contraction_cost',direct,
                     np.einsum('ni,ij,nj->n',np.c_[B,C],np.eye(dim)-P,np.c_[B,C])**s)
            ck.le('tail_projector_norm',np.sum(PC*PC),k)
            # Pure-tail scalar contraction, with coefficients restricted to a subspace.
            Hcoef=rng.normal(size=(n,5));S=np.linalg.qr(Hcoef)[0];Pi=np.eye(n)-S@S.T
            U2,_=np.linalg.qr(rng.normal(size=(dim,k)))
            P2=(U2*rng.uniform(0,1,size=k))@U2.T;PC2=P2[k:,k:]
            direction=C/feat.r[:,None]
            z1=np.einsum('ni,ij,nj->n',direction,PC,direction)
            z2=np.einsum('ni,ij,nj->n',direction,PC2,direction)
            coef=omega*feat.r**(2*s)/feat.pi
            nonlinear=coef*((1-z1)**s-(1-z2)**s)
            linear=s*coef*(z1-z2)
            ck.le('tail_gaussian_metric_contraction',nonlinear@Pi@nonlinear,linear@linear)
        records.append(dict(s=s,p=2*s,head_dimension=k,tail_dimension=q,rows=n,probability_components=K))
    return records

def algebraic_checks(ck):
    degree_records=[]
    for s in range(2,13):
        cats=Counter()
        for a,b,c,d in monomials(s):
            ck.true('partition_nonnegative',a+b+c+d==s and min(a,b,c,d)>=0)
            if a and b+c:
                l,nu,h,e,j,t=protected_indices(s,a,b,c,d)
                ck.true('protected_degrees',0<=j<=s-1 and 1<=l<=s and 1<=t<=2*s and e>=0)
                ck.true('operator_degree_identity',2*h+nu==l and 2*e+b+nu==j and h+e+nu==a)
                ck.true('protected_rank_exponent',j+c<=s-1 and 2*l+j+c<=3*s-1)
                cats['protected']+=1
            elif a:
                ck.true('radial_head_degree',b==c==0 and 1<=a<=s)
                cats['radial_head']+=1
            elif b>=2:
                b1=b//2;b2=b-b1
                ck.true('balanced_rank_exponent',1<=b1<=b2<=s-1 and b2+c<=s-1)
                cats['balanced']+=1
            elif b==1:
                ck.true('one_cross_rank_exponent',max(1,c)<=s-1)
                cats['one_cross']+=1
            else: cats['pure_tail']+=1
        ck.true('monomial_count',sum(cats.values())==(s+1)*(s+2)*(s+3)//6)
        degree_records.append(dict(s=s,counts=dict(cats)))
    # Exact rational polynomial identities, not floating point evaluations.
    for s in range(2,9):
        for A,X,R,T in ((Fraction(3,2),Fraction(-2,7),Fraction(1,3),Fraction(4,3)),
                         (Fraction(5,3),Fraction(1,5),Fraction(1,7),Fraction(9,8))):
            total=Fraction(0)
            for a,b,c,d in monomials(s):
                coeff=factorial(s)//(factorial(a)*factorial(b)*factorial(c)*factorial(d))*2**b*(-1)**c
                total+=coeff*A**a*X**b*R**c*T**d
            ck.true('exact_multinomial_expansion',total==(A+2*X+T-R)**s)
    return degree_records

def covariance_checks(ck,rng):
    for trial in range(20):
        n,l,r=12,4,6
        X=rng.normal(size=(n,l,r));U,_=np.linalg.qr(rng.normal(size=(n,4)))
        Pi=np.eye(n)-U@U.T
        Y=np.einsum('ij,jab->iab',Pi,X)
        A=np.einsum('iab,icb->ac',X,X);B=np.einsum('iab,iac->bc',X,X)
        AY=np.einsum('iab,icb->ac',Y,Y);BY=np.einsum('iab,iac->bc',Y,Y)
        ck.le('left_variance_contraction',-np.linalg.eigvalsh(A-AY)[0],0)
        ck.le('right_variance_contraction',-np.linalg.eigvalsh(B-BY)[0],0)
        a=np.linalg.norm(A,2);ev,V=np.linalg.eigh(B+a*np.eye(r));W=(V/np.sqrt(ev))@V.T
        Z=np.einsum('iab,bc->iac',Y,W)
        AZ=np.einsum('iab,icb->ac',Z,Z);BZ=np.einsum('iab,iac->bc',Z,Z)
        ck.le('anisotropic_left_variance',np.linalg.norm(AZ,2),1)
        ck.le('anisotropic_right_variance',np.linalg.norm(BZ,2),1)
    # Exact positive freezing examples preserving total mass and cardinality.
    for nminus,nplus in ((3,2),(5,4),(2,2),(4,2)):
        f=max(2,nminus-nplus+1);v=Fraction(nminus-nplus,f)
        x=[Fraction(-1)]*nminus+[Fraction(1)]*nplus+[v]*f
        ck.true('fractional_cardinality_constraint',sum(x)==0 and all(-1<=z<=1 for z in x))
        eta=Fraction(1,len(x));new=[eta*(1+z) for z in x]
        ck.true('fractional_positive_mass',all(z>=0 for z in new) and sum(new)==1)
        ck.true('fractional_active_halving',nplus<=len(x)/2 and all(0<eta*(1+v)<2*eta for _ in range(f)))

def certificate_generation(root):
    k,N,R=2,3,2;d=k+k*N;A=[];w=[]
    for j in range(k):
        for t in range(N):
            for sign in (1,-1):
                row=[0]*d;row[j]=R;row[k+j*N+t]=sign;A.append(row);w.append(2 if sign==1 else 0)
    queries=[]
    for sign in (1,-1):
        Z=[[0]*d for _ in range(d)]
        for j in range(k):
            v=[0]*d;v[j]=R;v[k+j*N]=sign
            for a in range(d):
                for b in range(d):Z[a][b]+=v[a]*v[b]
        queries.append((sign,Z,R*R+1))
    powers=[]
    for p in (4,6,8,10,12):
        s=p//2;cases=[]
        for sign,Z,den in queries:
            costs=[]
            for row in A:
                proj=[sum(Fraction(Z[i][j],den)*row[j] for j in range(d)) for i in range(d)]
                costs.append(sum((Fraction(row[i])-proj[i])**2 for i in range(d))**s)
            orig=sum(costs);weighted=sum(x*y for x,y in zip(w,costs));rel=abs(weighted-orig)/orig
            cases.append(dict(label='positive' if sign==1 else 'negative',denominator=den,projector_numerator=Z,
                              original_cost=str(orig),weighted_cost=str(weighted),relative_error=str(rel)))
        powers.append(dict(p=p,optimal_head_cost='12',queries=cases))
    data=dict(k=k,N=N,R=R,rows=A,weights=w,epsilon='1/10',powers=powers)
    path=root/'results'/'exact_even_power_certificate.json';path.write_text(json.dumps(data,indent=2)+'\n')
    result=exact_check(path)
    (root/'results'/'exact_certificate_check.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    ck=Checks();rng=np.random.default_rng(13092026)
    algebra=algebraic_checks(ck)
    numerical=numerical_features(ck,rng)
    covariance_checks(ck,rng)
    certificate=certificate_generation(root);ck.true('standalone_exact_certificate',certificate['passed'])
    result=dict(passed=True,seed=13092026,total_finite_assertions=sum(ck.count.values()),
                categories=dict(ck.count),max_scaled_residuals=dict(ck.max_residual),
                numerical_instances=numerical,degree_audit=algebra,
                environment=dict(python=platform.python_version(),numpy=np.__version__),
                numerical_tolerance=3e-7,range_eigenvalue_relative_threshold=2e-10,
                limitations=['Finite assertions are not independent proofs.',
                             'No asymptotic partial-coloring, restricted-invertibility or random-core oracle is implemented.',
                             'Numerical feature cases need not have globally optimal heads; those tests assert only the stated algebra and norm inequalities.',
                             'The exact certificate illustrates violations, not an asymptotically optimal support lower bound.'])
    path=args.output or root/'results'/'verification.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','total_finite_assertions','categories')},indent=2))

if __name__=='__main__':main()
