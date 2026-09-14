"""Exact supplemental checks; standard-library only. Not an all-graph solver."""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import json

def rank(matrix):
    a=[[Q(x) for x in row] for row in matrix]
    if not a: return 0
    width=len(a[0])
    if any(len(row)!=width for row in a): raise ValueError('ragged matrix')
    r=0
    for col in range(width):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        q=a[r][col]; a[r]=[x/q for x in a[r]]
        for i in range(r+1,len(a)):
            q=a[i][col]
            if q: a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r

def gram(v):
    return [[sum(Q(x)*Q(y) for x,y in zip(a,b)) for b in v] for a in v]

def edgeset(n,edges):
    e=set()
    for pair in edges:
        if len(pair)!=2: raise ValueError('edge length')
        u,v=pair
        if type(u) is not int or type(v) is not int or not 0<=u<n or not 0<=v<n or u==v:
            raise ValueError('invalid edge')
        e.add(tuple(sorted((u,v))))
    return e

def support(matrix,edges):
    n=len(matrix)
    if any(len(row)!=n for row in matrix): raise ValueError('not square')
    e=edgeset(n,edges)
    for i in range(n):
        for j in range(i+1,n):
            if matrix[i][j]!=matrix[j][i]: raise ValueError('not symmetric')
            if bool(matrix[i][j])!=((i,j) in e):
                raise ValueError(f'support mismatch at {(i,j)}')
    return True

def complement(n,edges):
    e=edgeset(n,edges)
    return [(i,j) for i in range(n) for j in range(i+1,n) if (i,j) not in e]

def polynomial_vectors(p,q,edges,d=None):
    if type(p) is not int or type(q) is not int or p<0 or q<0 or p+q==0:
        raise ValueError('nonempty nonnegative part sizes required')
    e=edgeset(p+q,edges)
    if any(not (u<p<=v) for u,v in e): raise ValueError('not the specified bipartition')
    nbr=[[u+1 for u in range(p) if (u,p+j) in e] for j in range(q)]
    required=max(map(len,nbr),default=0)
    if d is None: d=required
    if type(d) is not int or d<required: raise ValueError('degree bound too small')
    vectors=[[t**h for h in range(d+1)] for t in range(1,p+1)]
    for roots in nbr:
        poly=[1]
        for root in roots:
            nxt=[0]*(len(poly)+1)
            for i,c in enumerate(poly): nxt[i]-=root*c; nxt[i+1]+=c
            poly=nxt
        vectors.append([0]*(d-len(roots))+poly)
    support(gram(vectors),complement(p+q,e))
    assert all(any(x for x in v) for v in vectors)
    assert rank(vectors)<=d+1
    return vectors

def sdp_fixture():
    v=[[1,0],[1,Q(1,4)],[Q(1,4),1],[Q(1,8),1]]
    c=gram(v)
    a,b,h=c[0][1],c[1][2],c[2][3]
    q=[[1,0],[-1,0],[0,1],[0,-1]]
    k=[[a,b],[b,h]]
    s=[[sum(Q(q[i][r])*k[r][t]*q[j][t] for r in range(2) for t in range(2)) for j in range(4)] for i in range(4)]
    x=[[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]]
    B=[[c[i][j]+s[i][j] for j in range(4)] for i in range(4)]
    return {'V':v,'C':c,'S':s,'X':x,'B':B,'a':a,'b':b,'c':h}

def run(directory):
    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)
    records=[]
    p=q=3
    possibilities=[(i,p+j) for i in range(p) for j in range(q)]
    for mask in range(1<<len(possibilities)):
        edges=[e for k,e in enumerate(possibilities) if mask>>k&1]
        v=polynomial_vectors(p,q,edges)
        records.append({'family':'labeled_3_by_3','mask':mask,'n':p+q,'parts':[p,q],
                        'edges':edges,'vectors':v,'rank':rank(v)})
    for k in range(2,13):
        edges=[(i,k+j) for i in range(k) for j in range(k) if i<=j]
        v=polynomial_vectors(k,k,edges)
        assert rank(v)==k+1
        records.append({'family':'half_graph','k':k,'n':2*k,'parts':[k,k],
                        'edges':edges,'vectors':v,'rank':rank(v)})
    p,q=7,13
    edges=sorted(set((u,p+j) for j in range(q) for u in [(j+t*t)%p for t in range(4)]))
    v=polynomial_vectors(p,q,edges,d=4)
    records.append({'family':'one_side_degree_four','n':p+q,'parts':[p,q],
                    'edges':edges,'vectors':v,'rank':rank(v)})
    with (directory/'polynomial_complements.jsonl').open('w') as out:
        for record in records: out.write(json.dumps(record,separators=(',',':'))+'\n')
    f=sdp_fixture(); e=[(0,1),(1,2),(2,3)]
    assert f['a']>0 and f['c']>0 and f['a']*f['c']-f['b']**2>0
    assert rank(f['V'])==2 and rank(f['S'])==2 and rank(f['X'])==2 and rank(f['B'])==4
    assert all(sum(f['S'][i][k]*f['X'][k][j] for k in range(4))==0 for i in range(4) for j in range(4))
    support(f['B'],complement(4,e))
    try: support(f['X'],e)
    except ValueError as exc: rejected=str(exc)
    else: raise AssertionError('unsound validator accepted missing path edge')
    serial={k:([[str(x) for x in row] for row in val] if isinstance(val,list) else str(val)) for k,val in f.items()}
    serial['expected_support_rejection']=rejected
    (directory/'sdp_support_obstruction.json').write_text(json.dumps(serial,indent=2)+'\n')
    # Freshly read saved records rather than relying only on construction-time assertions.
    checked=0
    for line in (directory/'polynomial_complements.jsonl').read_text().splitlines():
        r=json.loads(line); v=r['vectors']
        assert len(v)==r['n']
        support(gram(v),complement(r['n'],r['edges']))
        assert rank(v)==r['rank']
        checked+=1
    return {'polynomial_complement_witnesses_checked':checked,'sdp_expected_rejection':rejected,
            'sdp_rank_sum':rank(f['X'])+rank(f['B']),
            'note':'Complement-only witnesses, not 524 rank-pair certificates. The SDP pair is intentionally rejected.'}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    result=run(root/'certificates')
    print(json.dumps(result,indent=2))
