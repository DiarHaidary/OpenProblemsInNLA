"""Find and then EXACTLY verify a positive Gram-form in the minor ideal.

The numerical SDP only proposes a certificate. The saved certificate is accepted
only after rational ideal-membership and positive-definiteness checks.
"""
from __future__ import annotations
from pathlib import Path
from itertools import combinations,combinations_with_replacement
import argparse,ast,json,re,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1]

def exponents(n,k):
    out=[]
    for c in combinations_with_replacement(range(n),k):
        v=[0]*n
        for i in c:v[i]+=1
        out.append(tuple(v))
    return out

def monomial(xs,e):return s.prod(x**a for x,a in zip(xs,e))

def positive_definite(G):
    H=s.Matrix(G);piv=[]
    while H.rows:
        p=H[0,0]
        if p<=0:return False,piv
        piv.append(p);v=H[1:,0];H=H[1:,1:]-v*v.T/p
    return True,piv

def input_pencil():
    D=json.loads((ROOT/'data/interrupted_pencil.json').read_text());xs=s.symbols('x0:5')
    Bs=[s.Matrix([[s.Rational(v) for v in row] for row in B]) for B in D['basis']]
    A=sum((x*B for x,B in zip(xs,Bs)),s.zeros(4))
    ijs=list((I,J) for I in combinations(range(4),3) for J in combinations(range(4),3))
    fs=[s.expand(A.extract(I,J).det()) for I,J in ijs]
    return D,xs,A,ijs,fs

def require(condition,message):
    if not condition:raise ValueError(message)

def rational_entry(value):
    # Exact decimal integers/fractions only; floats must not silently become
    # rational approximations, and expression strings are not evaluated.
    require(type(value) is int or isinstance(value,str),'Gram entries must be rational integers/fractions')
    text=str(value)
    require(len(text)<=4096 and re.fullmatch(r'[+-]?\d+(?:/[+-]?\d+)?',text) is not None,
            'Invalid or oversized rational Gram entry')
    try:
        value=s.Rational(text)
        require(value.is_Rational is True,'Gram entries must be finite rationals')
        return value
    except (ValueError,TypeError,ZeroDivisionError) as error:
        raise ValueError('Invalid rational Gram entry') from error

def polynomial_multiplier(text,xs,max_degree):
    """Parse rational polynomials without evaluating Python or accepting poles."""
    require(isinstance(text,str) and len(text)<=100000,'Invalid or oversized multiplier')
    try:tree=ast.parse(text,mode='eval')
    except (SyntaxError,RecursionError) as error:raise ValueError('Invalid multiplier syntax') from error
    require(sum(1 for _ in ast.walk(tree))<=20000,'Multiplier expression is too large')
    names={str(x):s.Poly(x,*xs,domain=s.QQ) for x in xs}
    def parse(node):
        if isinstance(node,ast.Constant) and type(node.value) is int:
            require(node.value.bit_length()<=16384,'Multiplier integer is too large')
            result=s.Poly(node.value,*xs,domain=s.QQ)
        elif isinstance(node,ast.Name) and node.id in names:result=names[node.id]
        elif isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            result=parse(node.operand)
            if isinstance(node.op,ast.USub):result=-result
        elif isinstance(node,ast.BinOp):
            left=parse(node.left)
            if isinstance(node.op,ast.Pow):
                require(isinstance(node.right,ast.Constant) and type(node.right.value) is int
                        and 0<=node.right.value<=max_degree,'Invalid polynomial exponent')
                require(left.total_degree()*node.right.value<=max_degree,
                        'Polynomial power exceeds the multiplier degree')
                result=left**node.right.value
            else:
                right=parse(node.right)
                if isinstance(node.op,ast.Add):result=left+right
                elif isinstance(node.op,ast.Sub):result=left-right
                elif isinstance(node.op,ast.Mult):result=left*right
                elif isinstance(node.op,ast.Div):
                    require(right.total_degree()==0 and not right.is_zero,
                            'A multiplier denominator must be a nonzero rational constant')
                    result=left.mul_ground(1/right.TC())
                else:raise ValueError('Unsupported multiplier operation')
        else:raise ValueError('Multipliers must be rational polynomials in the pencil variables')
        require(result.total_degree()<=max_degree,'Multiplier degree exceeds the certificate degree')
        return result
    try:poly=parse(tree.body)
    except RecursionError as error:raise ValueError('Multiplier expression is too deep') from error
    require(poly.is_zero or all(sum(e)==max_degree for e,c in poly.terms()),
            'Nonzero multipliers must have the required homogeneous degree')
    return poly.as_expr()

def verify(path):
    _,xs,A,ijs,fs=input_pencil();D=json.loads(Path(path).read_text())
    require(isinstance(D,dict),'Certificate must be an object')
    degree=D.get('degree')
    require(type(degree) is int and degree in (4,6,8),'Certificate degree must be 4, 6, or 8')
    raw=D.get('monomials');expected=set(exponents(len(xs),degree//2))
    require(isinstance(raw,list) and len(raw)==len(expected),'A complete monomial basis is required')
    es=[]
    for e in raw:
        require(isinstance(e,list) and len(e)==len(xs)
                and all(type(a) is int and 0<=a<=degree//2 for a in e)
                and sum(e)==degree//2,'Invalid monomial exponent vector')
        es.append(tuple(e))
    require(set(es)==expected,'Monomials must list the complete common-degree basis exactly once')
    z=s.Matrix([monomial(xs,e) for e in es]);q=len(es)
    gram=D.get('gram')
    require(isinstance(gram,list) and len(gram)==q
            and all(isinstance(row,list) and len(row)==q for row in gram),'Invalid Gram dimensions')
    G=s.Matrix([[rational_entry(v) for v in row] for row in gram])
    require(G==G.T,'Gram matrix must be symmetric')
    raw_h=D.get('multipliers')
    require(isinstance(raw_h,list) and len(raw_h)==len(fs),'Invalid multiplier count')
    hs=[polynomial_multiplier(h,xs,degree-3) for h in raw_h]
    indices=D.get('minor_indices')
    require(isinstance(indices,list) and len(indices)==len(ijs),'Invalid minor-index count')
    require(all(isinstance(pair,list) and len(pair)==2
                and all(isinstance(t,list) and all(type(v) is int for v in t) for t in pair)
                and pair==[list(I),list(J)] for pair,(I,J) in zip(indices,ijs)),
            'Minor indices do not match the recomputed pencil')
    require(s.Poly((z.T*G*z)[0]-sum(h*f for h,f in zip(hs,fs)),*xs,domain=s.QQ).is_zero,
            'Gram form is not the claimed polynomial combination of the minors')
    ok,piv=positive_definite(G);require(ok,'Gram matrix is not positive definite')
    return {'status':'EXACTLY_VERIFIED','degree':degree,'gram_dimension':len(es),'positive_pivots':list(map(str,piv))}

def search(degree):
    import numpy as np
    import cvxpy as cp
    start=time.monotonic();_,xs,A,ijs,fs=input_pencil();half=degree//2
    ze=exponents(5,half);oe=exponents(5,degree);me=exponents(5,degree-3);rows={e:i for i,e in enumerate(oe)}
    W=s.zeros(len(oe),len(fs)*len(me))
    for i,f in enumerate(fs):
        terms=s.Poly(f,*xs).terms()
        for j,e in enumerate(me):
            for u,c in terms:
                if c:W[rows[tuple(a+b for a,b in zip(e,u))],i*len(me)+j]+=c
    null=W.T.nullspace();L=s.Matrix.hstack(*null).T if null else s.zeros(0,len(oe))
    pairs=[(i,j) for i in range(len(ze)) for j in range(i,len(ze))]
    Q=s.zeros(len(oe),len(pairs))
    for k,(i,j) in enumerate(pairs):Q[rows[tuple(a+b for a,b in zip(ze[i],ze[j]))],k]=1 if i==j else 2
    D=L*Q; R,piv=D.rref(); free=[j for j in range(len(pairs)) if j not in piv]
    H=cp.Variable((len(ze),len(ze)),symmetric=True);gv=cp.hstack([H[i,j] for i,j in pairs])
    constraints=[H-np.eye(len(ze)) >> 0]
    if D.rows:
        Df=np.asarray(D,dtype=float);Df=Df/np.maximum(np.max(np.abs(Df),axis=1,keepdims=True),1)
        constraints.append(Df@gv==0)
    prob=cp.Problem(cp.Minimize(cp.trace(H)),constraints)
    solvers=cp.installed_solvers();done=False
    for solver in ('CLARABEL','CVXOPT','SCS'):
        if solver not in solvers:continue
        try:
            kw={'solver':solver}
            if solver=='SCS':kw.update({'eps':1e-8,'max_iters':15000})
            if solver=='CLARABEL':kw.update({'time_limit':20.0,'max_iter':200})
            prob.solve(**kw)
            if H.value is not None and prob.status in ('optimal','optimal_inaccurate'):done=True;break
        except Exception:continue
    if not done:raise RuntimeError(f'No candidate Gram matrix; SDP status {prob.status}')
    vals=[float(H.value[i,j]) for i,j in pairs]
    for digits in (6,9,12,15):
        den=10**digits;g=[s.Rational(round(v*den),den) for v in vals]
        for i,p in enumerate(piv):g[p]=-sum(R[i,j]*g[j] for j in free)
        G=s.zeros(len(ze))
        for v,(i,j) in zip(g,pairs):G[i,j]=G[j,i]=v
        ok,_=positive_definite(G)
        if ok:break
    if not ok:raise RuntimeError('Rational recovery did not produce a positive-definite Gram matrix')
    q=Q*s.Matrix(g);_,cols=W.rref();U=W[:,list(cols)]
    alpha,params=U.gauss_jordan_solve(q);assert not params.rows
    full=s.zeros(W.cols,1)
    for j,v in zip(cols,alpha):full[j]=v
    hs=[s.expand(sum(full[i*len(me)+j]*monomial(xs,e) for j,e in enumerate(me))) for i in range(len(fs))]
    obj={'degree':degree,'monomials':ze,'gram':[[str(v) for v in G.row(i)] for i in range(G.rows)],
         'minor_indices':ijs,'multipliers':list(map(str,hs)), 'note':'All final coefficients are rational. SDP output is not itself a certificate.'}
    out=ROOT/f'data/pencil_sos_degree_{degree}.json';out.write_text(json.dumps(obj,indent=2))
    res=verify(out);res['elapsed_seconds']=time.monotonic()-start
    (ROOT/f'data/pencil_sos_degree_{degree}_verified.json').write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,choices=(4,6,8),default=4);p.add_argument('--verify')
    a=p.parse_args()
    if a.verify:print(json.dumps(verify(a.verify),indent=2))
    else:search(a.degree)
