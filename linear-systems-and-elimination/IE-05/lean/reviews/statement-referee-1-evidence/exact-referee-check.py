#!/usr/bin/env python3
"""Separate exact statement diagnostic from Lean literals and canonical Markdown.

This is Python arithmetic and semantic sampling, not a Lean proof. It imports
no author checker. Radical comparisons are reduced to integer/rational ones.
"""
import ast,hashlib,itertools,json,pathlib,re
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent
S=E/'input-snapshot'
SRC=S/'NLA/IE05/Definitions.lean'
CAN=S/'verification/original-sources/linear-systems-and-elimination/IE-05/solution.md'
def identity(p):return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def transpose(a):return [list(x) for x in zip(*a)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def lean_literal(text,name,case):
    body=text.split('def '+name,1)[1].split('\ndef ',1)[0].split('| '+case+' =>',1)[1]
    start=body.index('![')+1
    depth=0
    for pos in range(start,len(body)):
        if body[pos]=='[':depth+=1
        if body[pos]==']':
            depth-=1
            if depth==0:break
    literal=body[start:pos+1].replace('!','')
    assert re.fullmatch(r'[\[\],\s\d-]+',literal)
    return ast.literal_eval(literal)
def tail(l,t,k,i,j):return sum(l[i][r]*t[r][j] for r in range(k,len(l)))
def standard_shrink(block,p):
    b=[r[:] for r in block];b[0],b[p]=b[p],b[0]
    assert b[0][0]
    return [[b[i][j]-b[i][0]*b[0][j]/b[0][0] for j in range(1,len(b))] for i in range(1,len(b))]
def padded_step(a,k,p):
    n=len(a);b=[r[:] for r in a];b[k],b[p]=b[p],b[k]
    return [[b[i][j]-(b[i][k]/b[k][k])*b[k][j] if k<i and k<j else F(0)
        for j in range(n)] for i in range(n)]
def scan(a,k):
    p=k
    for i in range(len(a)):
        if k<=i and abs(a[p][k])<abs(a[i][k]):p=i
    return p
def determinant(a):
    n=len(a)
    if n==0:return F(1)
    return sum((-1)**j*a[0][j]*determinant([r[:j]+r[j+1:] for r in a[1:]]) for j in range(n))
def tiny_paths(a):
    n=len(a);input_max=max((abs(x) for row in a for x in row),default=F(0))
    count=0;swapcount=0;stages=0
    def visit(pad,block,k,largest):
        nonlocal count,swapcount,stages
        assert [[pad[i][j] for j in range(k,n)] for i in range(k,n)]==block
        if k==n:
            assert pad==[[F(0)]*n for _ in range(n)]
            assert F(1)<=largest/input_max<=2**(n-1)
            count+=1;return
        stages+=1
        maxcol=max(abs(block[i][0]) for i in range(n-k));assert maxcol>0
        ties=[i for i in range(n-k) if abs(block[i][0])==maxcol]
        assert scan(pad,k)==k+min(ties)
        thismax=max(abs(x) for row in block for x in row)
        for p in ties:
            swapcount+=p!=0
            newblock=standard_shrink(block,p);newpad=padded_step(pad,k,k+p)
            assert max((abs(x) for row in newblock for x in row),default=F(0))<=2*thismax
            visit(newpad,newblock,k+1,max(largest,thismax))
    visit(a,a,0,F(0))
    return {'paths':count,'nontrivial_swaps':swapcount,'active_stages':stages}
def main():
    text=SRC.read_text();canonical=CAN.read_text()
    assert 'if b = true ∧ i = 7 ∧ j = 1 then 0 else -1 else 0' in text
    latex={label:[[int(x.strip()) for x in row.strip().split('&')]
        for row in data.strip().split('\\\\')] for label,data in
        re.findall(r'(H_0|H|T)=\s*\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',canonical,re.S)}
    assert set(latex)=={'H','T','H_0'}
    cases={};witnesschecks=[];candidatechecks=[]
    for boolean,case in [(False,'candidate'),(True,'witness')]:
        h=lean_literal(text,'integerH',str(boolean).lower())
        t=lean_literal(text,'integerT',str(boolean).lower())
        d=lean_literal(text,'integerD',str(boolean).lower())
        assert len(h)==len(t)==len(d)==8 and all(len(row)==8 for row in h+t)
        l=[[1 if i==j else (0 if boolean and (i,j)==(7,1) else -1) if j<i else 0
            for j in range(8)] for i in range(8)]
        assert h==latex['H' if boolean else 'H_0']
        if boolean:assert t==latex['T']
        scale_pattern=r'D'+('' if boolean else '_0')+r'=\\operatorname\{diag\}\(([^)]*)\)'
        assert d==[int(x) for x in re.search(scale_pattern,canonical).group(1).split(',')]
        assert mm(transpose(h),h)==[[d[i] if i==j else 0 for j in range(8)] for i in range(8)]
        assert mm(l,t)==h
        assert all(d[i]>0 and t[i][i]>0 and l[i][i]==1 for i in range(8))
        assert all(t[i][j]==0 and abs(l[i][j])<=1 for i in range(8) for j in range(i))
        assert all(l[i][j]==0 for i in range(8) for j in range(i+1,8))
        # Recompute Gram-Schmidt residuals directly from L, preserving their positive orientation.
        residuals=[];positive_multiples=[]
        for j,col in enumerate(zip(*l)):
            col=list(map(F,col));v=col[:]
            for u in residuals:
                coef=dot(u,col)/dot(u,u);v=[x-coef*y for x,y in zip(v,u)]
            assert dot(v,v)>0
            pos=next(i for i,x in enumerate(v) if x)
            multiple=F(h[pos][j])/v[pos];assert multiple>0
            assert all(multiple*v[i]==h[i][j] for i in range(8))
            residuals.append(v);positive_multiples.append(str(multiple))
        current=[list(map(F,row)) for row in h];pivotdata=[];active_identity_count=0
        for k in range(8):
            assert scan(current,k)==k
            ties=[i for i in range(k,8) if abs(current[i][k])==abs(current[k][k])]
            assert current[k][k]>0
            assert all(abs(current[i][k])<=current[k][k] for i in range(k,8))
            pivotdata.append({'k':k,'pivot_numerator':str(current[k][k]),'ties':ties})
            for i in range(k,8):
                for j in range(k,8):
                    value=tail(l,t,k,i,j);assert current[i][j]==value;active_identity_count+=1
                    if not boolean:
                        lhs=value**2;rhs=5462*d[j];assert lhs<=rhs
                        candidatechecks.append({'k':k,'i':i,'j':j,'integer_tail':value,'lhs':lhs,'rhs':rhs})
            current=padded_step(current,k,k)
        assert current==[[F(0)]*8 for _ in range(8)]
        if boolean:
            for i in range(8):
                for j in range(8):
                    lhs=5272*h[i][j]**2;rhs=3969*d[j];assert lhs<=rhs
                    witnesschecks.append({'i':i,'j':j,'lhs':lhs,'rhs':rhs})
            assert tail(l,t,7,7,7)==5272 and d[7]==5272
        else:assert h[2][2]==51 and d[2]==3286
        cases[case]={'H':h,'D':d,'T':t,'L':l,'printed_source_match':True,
            'gram_identity':True,'lu_identity':True,'factor_hypotheses':True,
            'positive_multiples_of_independent_gram_schmidt_residuals':positive_multiples,
            'no_swap_pivots_and_ties':pivotdata,'direct_schur_vs_tail_identity_count':active_identity_count,
            'stage_eight_zero_padding':True}
    gap=F(5272,63)**2-F(17948132,2601)
    assert gap==F(117335164,1147041)>0
    assert len(witnesschecks)==64 and len(candidatechecks)==204
    # A separate shrinking-active-block representation checks padding, row positions,
    # exact ties, and n stages, across every admissible path of nonsingular tiny inputs.
    tiny={'n2_nonsingular_inputs':0,'n2_paths':0,'nontrivial_swaps':0,'active_stages':0}
    for entries in itertools.product([-1,0,1],repeat=4):
        a=[list(map(F,entries[:2])),list(map(F,entries[2:]))]
        if determinant(a):
            check=tiny_paths(a);tiny['n2_nonsingular_inputs']+=1
            tiny['n2_paths']+=check['paths'];tiny['nontrivial_swaps']+=check['nontrivial_swaps'];tiny['active_stages']+=check['active_stages']
    fixtures=[[[0,0,1],[1,0,0],[0,-1,0]],[[1,2,-1],[-1,3,2],[1,0,4]],[[1,1,1],[1,-1,0],[-1,1,2]]]
    tiny['n3_fixtures']=[]
    for a in fixtures:
        rational=[list(map(F,row)) for row in a];assert determinant(rational)
        tiny['n3_fixtures'].append({'matrix':a,**tiny_paths(rational)})
    out={'phase':'independent statement arithmetic and representation diagnostic','pass':True,
        'source':identity(SRC),'canonical_source':identity(CAN),'script':identity(pathlib.Path(__file__)),
        'matrix_cases':cases,'witness_64_input_bounds':witnesschecks,'candidate_204_active_bounds':candidatechecks,
        'exact_positive_squared_gap':str(gap),'tiny_arbitrary_path_diagnostic':tiny,
        'no_author_checker_imported':True,'no_Lean_proof_or_certificate':True,
        'limitations':'Exact finite diagnostics and sampled generic representations do not prove Lean statements or universal contracts.'}
    (E/'exact-result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'pass':True,'witness_input_bounds':len(witnesschecks),'candidate_active_bounds':len(candidatechecks),
        'gap':str(gap),'n2_arbitrary_paths':tiny,'result':identity(E/'exact-result.json')}))
if __name__=='__main__':main()
