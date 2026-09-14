#!/usr/bin/env python3
"""Verify the Krause all-amplifications certificate using integer arithmetic.

The certificate proves a special case of SP-09, NOT the universal statement.
Every proof-critical operation uses Python integers. NumPy is only an array
container; object-dtype matrix products use arbitrary-precision integers.
No eigensolver, optimizer, or floating-point tolerance is used for acceptance.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import time
import numpy as np

Pair = tuple[int, int]  # a + b*s, where s^2 = -3 and conjugate(s) = -s

def require(condition: bool, message: str = "Certificate check failed") -> None:
    if not condition:
        raise ValueError(message)

def add(a: Pair, b: Pair) -> Pair:
    return a[0]+b[0], a[1]+b[1]

def mul(a: Pair, b: Pair) -> Pair:
    return a[0]*b[0]-3*a[1]*b[1], a[0]*b[1]+a[1]*b[0]

def adj(a: Pair) -> Pair:
    return a[0], -a[1]

def normal_word(word: tuple[int, ...], cyclic: bool = False):
    """Reduce orthogonal projection relations; optionally use trace cyclicity."""
    w=list(word)
    while True:
        found=False
        for j in range(len(w)-1):
            if (w[j]<2)==(w[j+1]<2):
                if w[j]!=w[j+1]:
                    return None
                w.pop(j+1)
                found=True
                break
        if found:
            continue
        if cyclic and len(w)>1 and (w[0]<2)==(w[-1]<2):
            if w[0]!=w[-1]:
                return None
            w.pop()
            continue
        break
    if cyclic and w:
        return min(tuple(w[j:]+w[:j]) for j in range(len(w)))
    return tuple(w)

def words(degree: int) -> list[tuple[int, ...]]:
    result=[()]
    for length in range(1,degree+1):
        result.extend(w for w in itertools.product(range(4),repeat=length)
                      if all((w[j]<2)!=(w[j+1]<2) for j in range(length-1)))
    return result

def poly_product(p, q):
    result={}
    for u,a in p.items():
        for v,b in q.items():
            w=normal_word(u+v)
            if w is not None:
                result[w]=add(result.get(w,(0,0)),mul(a,b))
    return {w:c for w,c in result.items() if c!=(0,0)}

def load_matrix(rows):
    return np.array([[int(x) for x in row] for row in rows],dtype=object)

def mm(A, B):
    """Matrix product over Q(s), with integral coefficients in this verifier."""
    ar,ai=A;br,bi=B
    return ar@br-3*ai@bi, ar@bi+ai@br

def star(A):
    return A[0].T,-A[1].T

def hermitian(A):
    return np.array_equal(A[0],A[0].T) and np.array_equal(A[1],-A[1].T)

def verify(path: Path) -> dict:
    started=time.monotonic()
    c=json.loads(path.read_text())
    den=int(c['coordinate_denominator'])
    require(den > 0 and c['q_denominator'] == 388)
    qr=np.array([int(x) for x in c['q_real']],dtype=object).reshape(-1,1)
    qi=np.array([int(x) for x in c['q_s']],dtype=object).reshape(-1,1)
    B,L=words(4),words(3)
    require(len(B) == 61 and len(L) == 29 and (qr.shape == (29, 1)) and (qi.shape == (29, 1)))
    require(all((int(x) == 0 for x in qr[5:, 0])) and all((int(x) == 0 for x in qi[5:, 0])))
    require(3 * qr[0, 0] + sum(qr[1:5, 0]) == 3 * 388)
    require(3 * qi[0, 0] + sum(qi[1:5, 0]) == 0)
    print('PASS: the distinguished polynomial q has normalized trace exactly 1.')
    Y=[];margins=[]
    require(len(c['blocks']) == 3)
    for j,(b,n,d) in enumerate(zip(c['blocks'],[52,26,26],[61,29,29])):
        K=load_matrix(b['kernel_real']),load_matrix(b['kernel_s'])
        Z=load_matrix(b['matrix_real']),load_matrix(b['matrix_s'])
        S=load_matrix(b['preconditioner_real']),load_matrix(b['preconditioner_s'])
        require(K[0].shape == K[1].shape == (d, n))
        require(Z[0].shape == Z[1].shape == S[0].shape == S[1].shape == (n, n))
        require(hermitian(Z))
        G=mm(mm(star(S),Z),S)
        require(hermitian(G))
        row_margins=[]
        for i in range(n):
            margin=int(G[0][i,i])-sum(abs(int(G[0][i,k]))+2*abs(int(G[1][i,k]))
                                       for k in range(n) if k!=i)
            require(margin > 0, f'Block {j} lacks the exact positivity certificate.')
            row_margins.append(margin)
        # |a+b*i*sqrt(3)| <= |a|+2|b|. Strict diagonal dominance with
        # positive diagonal makes S* Z S positive definite, hence Z is PD.
        margins.append(min(row_margins))
        Y.append(mm(mm(K,Z),star(K)))
        print(f'PASS: block {j} is positive definite (all {n} integer margins positive).')
    fixed=mm((qr,qi),star((qr,qi)))
    Y[1]=Y[1][0]+den*fixed[0],Y[1][1]+den*fixed[1]
    require(all((hermitian(y) for y in Y)))
    # D = d/13; h1,h2 below are 169*(27/13 - D*D) and its companion.
    d={():(-2,4),(0,):(14,-2),(1,):(5,3),(2,):(14,-2),(3,):(5,3)}
    ds={w[::-1]:adj(v) for w,v in d.items()}
    h1={w:(-a,-b) for w,(a,b) in poly_product(ds,d).items()}
    h2={w:(-a,-b) for w,(a,b) in poly_product(d,ds).items()}
    h1[()]=add(h1.get((),(0,0)),(351,0))
    h2[()]=add(h2.get((),(0,0)),(351,0))
    trace_poly={}
    for W,h,(yr,yi) in zip([B,L,L],[{():(169,0)},h1,h2],Y):
        for i,u in enumerate(W):
            for j,v in enumerate(W):
                # Tr(Y M) = sum Y[j,i] * tau(u* h v).
                yij=int(yr[j,i]),int(yi[j,i])
                if yij==(0,0):
                    continue
                for w,coef in h.items():
                    word=normal_word(u[::-1]+w+v,cyclic=True)
                    if word is None:
                        continue
                    z=mul(yij,coef)
                    trace_poly[word]=add(trace_poly.get(word,(0,0)),z)
    # Clear the only trace denominator: tau(P_i)=tau(Q_i)=1/3.
    constant=mul((3,0),trace_poly.pop((),(0,0)))
    for j in range(4):
        constant=add(constant,trace_poly.pop((j,),(0,0)))
    nonzero={w:z for w,z in trace_poly.items() if z!=(0,0)}
    require(constant == (0, 0), f'Nonzero trace constant: {constant}')
    require(not nonzero, f'Nonzero cyclic coefficients: {nonzero}')
    print('PASS: every coefficient in the universal cyclic trace identity is exactly zero.')
    result={'result':'PASS','claim':'Krause three-point case only: all finite amplifications',
            'positivity':'exact integer strict diagonal dominance after congruence',
            'trace_identity':'exact zero coefficients in Q(s), s^2=-3',
            'q_trace':'exactly 1','blocks':[52,26,26],
            'checked_cyclic_words':len(trace_poly)+5,
            'minimum_integer_margins':[str(x) for x in margins],
            'elapsed_seconds':time.monotonic()-started}
    print('CERTIFICATE VERIFIED. This is not a proof of SP-09 for arbitrary spectra.')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',nargs='?',type=Path,
                        default=Path(__file__).with_name('krause_certificate.json'))
    parser.add_argument('--json-report',type=Path)
    args=parser.parse_args()
    report=verify(args.certificate)
    if args.json_report:
        args.json_report.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
