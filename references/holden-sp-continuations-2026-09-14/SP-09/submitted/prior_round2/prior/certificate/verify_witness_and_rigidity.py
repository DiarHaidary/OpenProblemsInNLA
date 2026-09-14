#!/usr/bin/env python3
"""Exact upper-bound, matching-gap, and equality-rigidity checks for the Krause case."""
from __future__ import annotations
from fractions import Fraction
import argparse,itertools,json,time
from pathlib import Path
import numpy as np
from verify_certificate import require,words,mm,star,load_matrix

F=Fraction

def zero(n,m=None):return np.zeros((n,n if m is None else m),dtype=object)
def ident(n):
    a=zero(n)
    for i in range(n):a[i,i]=F(1)
    return a

def scale_pair(A,c):
    r,i=A;a,b=c
    return a*r-3*b*i,a*i+b*r

def add_pair(A,B):return A[0]+B[0],A[1]+B[1]
def trace_pair(A):return sum(A[0].diagonal()),sum(A[1].diagonal())

def exact_rank(a):
    a=[[F(x) for x in row] for row in a];row=0
    for col in range(len(a[0])):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row]
        p=a[row][col];a[row]=[x/p for x in a[row]]
        for j in range(row+1,len(a)):
            p=a[j][col]
            if p:a[j]=[x-p*y for x,y in zip(a[j],a[row])]
        row+=1
        if row==len(a):break
    return row

def verify(path:Path)->dict:
    started=time.monotonic();c=json.loads(path.read_text())
    w=[F(5,8),F(1,4),F(1,8)];I=ident(3);W=zero(3)
    for i in range(3):W[i,i]=w[i]
    R=np.array([[F(i==j)-2*w[j] for j in range(3)] for i in range(3)],dtype=object)
    require(np.array_equal(R@R,I),'Reflection is not involutory.')
    require(np.array_equal(R.T@W@R,W),'Reflection does not preserve the exact weighted inner product.')
    P1=zero(3);P1[0,0]=F(1);P2=zero(3);P2[1,1]=F(1)
    Ps=[P1,P2,R@P1@R,R@P2@R]
    for P in Ps:
        require(np.array_equal(P@P,P))
        require(np.array_equal(P.T@W,W@P))
    require(np.array_equal(Ps[0]@Ps[1],zero(3)))
    require(np.array_equal(Ps[2]@Ps[3],zero(3)))
    D=scale_pair((I,zero(3)),(F(-2,13),F(4,13)))
    for j in (0,2):D=add_pair(D,scale_pair((Ps[j],zero(3)),(F(14,13),F(-2,13))))
    for j in (1,3):D=add_pair(D,scale_pair((Ps[j],zero(3)),(F(5,13),F(3,13))))
    Ds=D[0],-D[1]  # All projection generators are self-adjoint for W.
    require(np.array_equal(Ds[0].T@W,W@D[0]))
    require(np.array_equal(Ds[1].T@W,-W@D[1]))
    H=mm(Ds,D)
    X=add_pair(scale_pair(H,(13,0)),(-27*I,zero(3)))
    Y=add_pair(scale_pair(H,(13,0)),(-4*I,zero(3)))
    p=mm(X,Y)
    require(np.array_equal(p[0],zero(3)) and np.array_equal(p[1],zero(3)))
    require(trace_pair(H)==(F(58,13),F(0)))
    print('PASS: the witness squared singular values are 27/13, 27/13, 4/13.')
    a=[(F(1),F(0)),(F(4,13),F(5,13)),(F(-1,13),F(2,13))]
    costs=[[ (x[0]+y[0])**2+3*(x[1]+y[1])**2 for y in a] for x in a]
    distances=[max(costs[i][p[i]] for i in range(3)) for p in itertools.permutations(range(3))]
    require(min(distances)==F(28,13))
    print('PASS: exhaustive exact matching gives bottleneck squared distance 28/13.')
    B=words(4);evals=[]
    for word in B:
        E=I.copy()
        for letter in word:E=E@Ps[letter]
        evals.append(E)
    E=np.column_stack([M.ravel() for M in evals])
    K=load_matrix(c['blocks'][0]['kernel_real']);KI=load_matrix(c['blocks'][0]['kernel_s'])
    require(np.array_equal(KI,zero(61,52)))
    require(np.array_equal(E@K,zero(9,52)))
    require(exact_rank(E[:,:9])==9)
    require(np.array_equal(K[9:,:],768*ident(52)))
    require(all(len(word)<=2 for word in B[:9]))
    print('PASS: the first nine words span M_3; the 52 columns give the entire degree-four relation kernel.')
    print('EQUALITY RIGIDITY VERIFIED together with the positive Gram block in verify_certificate.py.')
    return {'result':'PASS','witness_squared_singular_values':['27/13','27/13','4/13'],
            'matching_squared_distance':'28/13','word_evaluation_rank':9,
            'relation_kernel_dimension':52,'basis_word_degree_at_most':2,
            'elapsed_seconds':time.monotonic()-started}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate',nargs='?',type=Path,default=Path(__file__).with_name('krause_certificate.json'))
    p.add_argument('--json-report',type=Path);a=p.parse_args();r=verify(a.certificate)
    if a.json_report:a.json_report.write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
