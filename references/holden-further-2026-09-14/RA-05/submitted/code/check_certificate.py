#!/usr/bin/env python3
"""Verify the cubic tensor support certificate with integers/Fractions only.

This checks the finite spectral/support certificate, not the asymptotic theorem.
No floating point or third-party library is used.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import json
import math

ROOT=Path(__file__).resolve().parents[1]

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def transpose(A): return [list(c) for c in zip(*A)]
def mul(A,B):
    Bt=transpose(B)
    return [[dot(row,col) for col in Bt] for row in A]
def rank_mod(A, prime=1000003):
    a=[[v%prime for v in row] for row in A]
    rank=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(rank,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][j],-1,prime)
        a[rank]=[(v*inv)%prime for v in a[rank]]
        for i in range(rank+1,len(a)):
            t=a[i][j]
            if t: a[i]=[(x-t*y)%prime for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==len(a[0]): break
    return rank

def run(path):
    data=json.loads(path.read_text())
    groups={}
    def check(cond,category,label):
        if not cond: raise AssertionError(f'{category}: {label}')
        groups[category]=groups.get(category,0)+1
    core=data['core_numerators_denominator_2']
    idx=data['noise_selected_cube_indices']
    signs=[[1-2*((x>>j)&1) for j in range(8)] for x in range(256)]
    C=[]
    for S in combinations(range(8),4):
        C.append([math.prod(x[j] for j in S) for x in signs])
    Csel=[[row[t] for t in idx] for row in C]
    G=[[Q(abs(dot(x,y))**3,64) for y in core] for x in core]
    Fnum=[[abs(dot(x,signs[t]))**3 for t in idx] for x in signs]
    F=[[Q(v,512) for v in row] for row in Fnum]
    B=[[Q(int(i//4==j//4),4) for j in range(12)] for i in range(12)]
    J=[[Q(1,12) for j in range(12)] for i in range(12)]
    Id=[[Q(int(i==j)) for j in range(12)] for i in range(12)]
    check(all(dot(row,row)==4 for row in core),'core','unit lengths')
    check(mul(B,B)==B and mul(J,J)==J and mul(B,J)==J,'core','nested orthogonal projections')
    check(G==[[Id[i][j]-B[i][j]/2+3*J[i][j]/2 for j in range(12)] for i in range(12)],'core','kernel decomposition')
    G2=mul(G,G)
    check(G2==[[Id[i][j]/4+3*(Id[i][j]-B[i][j])/4+15*J[i][j]/4 for j in range(12)] for i in range(12)],'core','squared singular value at least 1/4')
    check(all(sum(row)==2 for row in G),'core','all row sums equal two')
    CCt=mul(C,transpose(C))
    check(CCt==[[256*int(i==j) for j in range(70)] for i in range(70)],'noise','middle Walsh orthogonality')
    check(mul(C,Fnum)==[[512*v for v in row] for row in Csel],'noise','exact eigenvalue one on selected columns')
    gram=mul(transpose(Csel),Csel)
    check(gram==data['middle_selected_gram'],'noise','selected Gram matrix')
    L=[[Q(v) for v in row] for row in data['gram_minus_32I_ldl_lower']]
    D=[Q(v) for v in data['gram_minus_32I_ldl_diagonal']]
    check(all(v>0 for v in D),'noise','strictly positive rational LDL pivots')
    LDL=mul([[L[i][j]*D[j] for j in range(17)] for i in range(17)],transpose(L))
    check(LDL==[[Q(gram[i][j]-32*int(i==j)) for j in range(17)] for i in range(17)],'noise','LDL factorization implies F^T F >= I/8')
    A=[[a*b for a in c for b in signs[t]] for c in core for t in idx]
    check(A==data['input_integer_rows'],'tensor','all 204 original tensor rows')
    check(len(A)==204 and len(A[0])==32,'tensor','input shape')
    check(all(dot(a,a)==32 for a in A),'tensor','common row norm')
    check(rank_mod(A)==32,'tensor','full ambient rank witnessed modulo a prime')
    # Deterministic check of every factorized query coefficient on a spanning
    # tensor grid.  Equality of integer inner products proves the evaluation
    # identity for all selected data indices at all 3072 queries.
    for i,c in enumerate(core):
        for j,u in enumerate(core):
            cg=abs(dot(c,u))**3
            for t in range(17):
                a=A[j*17+t]
                for x in (0,1,7,31,85,170,255):
                    q=[v*w for v in c for w in signs[x]]
                    check(abs(dot(a,q))**3==cg*Fnum[x][t],'tensor_factorization_samples','integer tensor identity')
    cost_square_sum=sum(sum(row)**2 for row in G)*sum(sum(row)**2 for row in F)
    check(cost_square_sum==Q(data['sum_squared_normalized_original_query_costs']),'support','squared query-cost sum')
    check(cost_square_sum==Q(34287,2),'support','recorded exact value')
    coeff=cost_square_sum/(Q(1,4)*Q(1,8))
    check(coeff==548592 and coeff==Q(data['universal_support_bound']['epsilon_squared_coefficient']),'support','universal m >= 204 - 548592 epsilon^2')
    for row in data['support_examples']:
        e=Q(row['epsilon']); threshold=Q(204)-coeff*e*e
        check(threshold==Q(row['real_threshold']),'support','exact support threshold')
        check(math.ceil(threshold)==row['integer_lower_bound'],'support','integer support conclusion')
    w=data['candidate']['weights']; witness=data['candidate']['witness']
    check(all(x>=0 for x in w) and sum(x!=0 for x in w)==12 and sum(w)==204,'witness','positive candidate support and total mass')
    normal=witness['integer_normal']; Pn=witness['projector_numerator']
    check(dot(normal,normal)==32,'witness','normal norm')
    check(Pn==[[32*int(i==j)-normal[i]*normal[j] for j in range(32)] for i in range(32)],'witness','projector definition')
    check(Pn==transpose(Pn),'witness','projector symmetry')
    check(mul(Pn,Pn)==[[32*v for v in row] for row in Pn],'witness','projector idempotence')
    check(sum(Pn[i][i] for i in range(32))==32*31,'witness','projector rank 31')
    # Direct Euclidean residual numerators, rather than only linear-form costs.
    inner=[]
    for a in A:
        residual_num=[32*a[j]-sum(a[i]*Pn[i][j] for i in range(32)) for j in range(32)]
        aq=dot(a,normal)
        check(residual_num==[aq*q for q in normal],'direct_residuals','projector residual identity')
        check(dot(residual_num,residual_num)==32*aq*aq,'direct_residuals','residual squared norm')
        inner.append(abs(aq)**3)
    orig=Q(sum(inner),256); weighted=Q(sum(x*y for x,y in zip(w,inner)),256)
    check(orig==Q(witness['original_cost_rational_coefficient_of_sqrt2'])==396,'witness','original cubic Euclidean cost = 396 sqrt(2)')
    check(weighted==Q(witness['weighted_cost_rational_coefficient_of_sqrt2'])==4352,'witness','weighted cubic cost = 4352 sqrt(2)')
    rel=abs(weighted-orig)/orig
    check(rel==Q(witness['relative_error'])==Q(989,99),'witness','exact relative error')
    check(rel>Q(witness['violated_epsilon']),'witness','accuracy violation')
    return {'passed':True,'arithmetic':'Python integers and fractions.Fraction only',
            'assertions':sum(groups.values()),'categories':groups,
            'universal_signed_support_bound':'m >= 204 - 548592 epsilon^2',
            'support_at_1_over_100':150,'support_at_1_over_1000':204,
            'finite_scope':'One explicit p=3 tensor input. Asymptotic existence and imported theorems are not machine-verified.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate',type=Path,default=ROOT/'results/cubic_tensor_certificate.json')
    ap.add_argument('--output',type=Path,default=None)
    args=ap.parse_args(); result=run(args.certificate)
    text=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')
