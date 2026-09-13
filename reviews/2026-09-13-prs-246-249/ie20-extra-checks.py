from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import sys,json,hashlib
sys.path.insert(0,'/private/tmp/nla-ie20-replay-249/code')
from envelope_cg import ErrorMachine,exact_dot,run_cg,significant_bits
from joint_breakdown import joint_breakdown
from bounds import backward_error_compare

count=0
for n,K in product(range(2,18),(Q(15),Q(46,3),Q(31),Q(95,3),Q(127),Q(511,2))):
    A,b,p,actualK,policy=joint_breakdown(n,K)
    c=A[0][-1]
    # Independently use the active block eigenvalues; its complement is I.
    assert 0<c<1 and (1+c)/(1-c)==actualK<=K
    assert significant_bits(c)<=p
    machine=ErrorMachine(p,policy)
    q=machine.matvec(A,b,0)
    assert all(x==0 for x in q)
    assert all(abs(Q(f['delta']))<=Q(1,2**p) for f in machine.faults)
    out=run_cg(A,b,p,policy)
    assert len(out.iterates)==1 and out.status=='zero_denominator_before_alpha'
    count+=1

# Independent check of true backward-error comparator including equality,
# cancellation and C=0 branches using inputs with rational norm square roots.
comparisons=0
for r,x,a,b,e in product((Q(0),Q(1,7),Q(1),Q(13,2)),(Q(0),Q(2,3),Q(7)),(Q(1,11),Q(1),Q(5)),(Q(1,3),Q(2)),(Q(1,32),Q(3,8),Q(1,2))):
    eta=r/(a*x+b)
    assert backward_error_compare(r*r,x*x,a,b*b,e)==(eta>e)-(eta<e)
    comparisons+=1
result={'joint_witnesses_extended_parameter_grid':count,'backward_comparator_independent_rational_comparisons':comparisons,'all_passed':True,'scope':'Additional finite checks, including odd dimensions and noninteger condition bounds; not a universal proof.'}
Path('/private/tmp/nla-ie20-extra-checks-249.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
