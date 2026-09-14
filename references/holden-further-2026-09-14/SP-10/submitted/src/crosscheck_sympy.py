"""Independent exact check of the saved supplement (requires SymPy)."""
from pathlib import Path
import json
import sympy as s


def main():
    root=Path(__file__).resolve().parents[1]
    count=0
    masks=set()
    for line in (root/'certificates/polynomial_complements.jsonl').read_text().splitlines():
        record=json.loads(line)
        v=s.Matrix(record['vectors'])
        n=record['n']
        if v.rows!=n or any(all(v[i,j]==0 for j in range(v.cols)) for i in range(n)):
            raise ValueError('invalid nonzero-vector dimensions')
        a=v*v.T
        edges={tuple(sorted(pair)) for pair in record['edges']}
        for i in range(n):
            for j in range(i+1,n):
                if bool(a[i,j])!=((i,j) not in edges):
                    raise ValueError(f'wrong complement support at {i,j}')
        if v.rank()!=record['rank']:
            raise ValueError('claimed rank incorrect')
        if record['family']=='labeled_3_by_3':
            p,q=record['parts']
            assert (p,q)==(3,3)
            possibilities=[(i,p+j) for i in range(p) for j in range(q)]
            mask=sum(1<<k for k,e in enumerate(possibilities) if e in edges)
            assert mask==record['mask'] and mask not in masks
            masks.add(mask)
        count+=1
    assert masks==set(range(512))
    f=json.loads((root/'certificates/sdp_support_obstruction.json').read_text())
    m={name:s.Matrix([[s.Rational(x) for x in row] for row in f[name]]) for name in ['V','C','S','X','B']}
    assert m['C']==m['V']*m['V'].T
    a,b,c=[s.Rational(f[key]) for key in ['a','b','c']]
    q=s.Matrix([[1,0],[-1,0],[0,1],[0,-1]])
    assert a>0 and c>0 and a*c-b*b>0
    assert m['S']==q*s.Matrix([[a,b],[b,c]])*q.T
    assert m['B']==m['C']+m['S'] and m['S']*m['X']==s.zeros(4)
    assert m['X']==s.Matrix([[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]])
    assert [m[name].rank() for name in ['C','S','X','B']]==[2,2,2,4]
    assert m['X'][1,2]==0  # Required path edge is missing; this is NOT a valid pair.
    path={(0,1),(1,2),(2,3)}
    for i in range(4):
        for j in range(i+1,4): assert bool(m['B'][i,j])==((i,j) not in path)
    print(json.dumps({'independently_checked_complement_records':count,'labeled_3_by_3_coverage':len(masks),
        'defective_sdp_pair':'REJECTED as required','sympy_version':s.__version__},indent=2))

if __name__=='__main__': main()
