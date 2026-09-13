"""Independent NR-03 PR251 finite arithmetic audit (stdlib only).

Reconstructs all Boolean tuples and mathematical set atoms from the statement;
does not import a submitted generator, checker, or PASS output.
"""
from pathlib import Path
from itertools import product, combinations
from fractions import Fraction
from math import comb
import ast, csv, hashlib, json, re, subprocess

ROOT=Path('/private/tmp/nla-audit-251')
LEAN=ROOT/'nonnegative-and-positive-factorizations/NR-03/lean'
PKG=ROOT/'references/holden-nr03-2026-09-13'
OUT=Path('/private/tmp/nla-pr-251-finite-checks.json')
HEAD='589ec79798ee42adc7a7160a376c67252280a121'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==HEAD
report={'head':HEAD,'status':'RUNNING','checks':{},'row_modules':[],'reviewer_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

# The complete expected command grammar was inspected in the three Block00
# and three Block15 sources. Whole-file equality rejects any added declaration,
# local instance, changed row, weakened quantifier, alternate tactic or import.
header='''/-
Generated NR-03 literal-row certificates; see row-certificates/INTERFACES.md.
Each row uses its own closed kernel decision. The predecessor import makes
heavy row reductions sequential during ordinary Lake dependency builds.
No earlier probe source is imported. This source awaits full verification.
-/
'''
previous='NLA.NR03.FamilyDefs'
seen=[]
for family in ['Singleton','Pair','Four']:
    low=family.lower()
    for block in range(16):
        module=f'NLA.NR03.RowCertificate.{family}.Block{block:02}'
        path=LEAN/Path(module.replace('.','/')).with_suffix('.lean')
        expected=header+f'''import {previous}
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace NLA.NR03.RowCertificate.{family}

'''
        for row in range(8*block,8*block+8):
            expected+=f'''theorem row{row} : ∀ b : Mask7,
    {low}Sum ({row} : Mask7) b = {low}Closed ({row} : Mask7) b := by
  decide +kernel

#print axioms NLA.NR03.RowCertificate.{family}.row{row}

'''
            seen.append((family,row))
        expected+=f'end NLA.NR03.RowCertificate.{family}\n'
        actual=path.read_text()
        assert actual==expected, f'Unexpected complete source contents: {path}'
        report['row_modules'].append({'module':module,'row_start':8*block,'row_end':8*block+7,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'full_source_matches_reviewed_template':True})
        previous=module
assert len(seen)==len(set(seen))==384
assert set(LEAN.glob('NLA/NR03/RowCertificate/*/*.lean'))=={LEAN/Path(x['module'].replace('.','/')).with_suffix('.lean') for x in report['row_modules']}
report['checks']['whole_file_row_audit']={'modules':48,'literal_row_theorems':384,'rows_per_family':128,'columns_per_theorem':128,'ordered_family_obligations':49152,'all_expected_sources_exact':True}
print('PASS all 48 complete source files: exactly 384 distinct universal-row kernel decisions',flush=True)

def encode(a):return sum(x*(2**i) for i,x in enumerate(a))
bools=sorted(product((0,1),repeat=7),key=encode)
assert len(bools)==len(set(bools))==128
assert [encode(a) for a in bools]==list(range(128))
sets=[frozenset(i for i,x in enumerate(a) if x) for a in bools]
ground=frozenset(range(7))
cores=[a for a in sets if 6 not in a]
singletons=[frozenset((i,)) for i in range(7)]
pairs=[frozenset(x) for x in combinations(range(7),2)]
fours=[frozenset(x) for x in combinations(range(7),4)]
atoms=[('core',s) for s in cores]+[('singleton',s) for s in singletons]+[('pair',s) for s in pairs]+[('four',s) for s in fours]
assert list(map(len,[cores,singletons,pairs,fours]))==[64,7,21,35]
assert len(atoms)==len(set(atoms))==127

# Independent original matrix: ordinary coordinate dot product and signed
# subtraction, followed by squaring. It does not use the mask/popcount code.
C=[[(1-sum(ai*bi for ai,bi in zip(a,b)))**2 for b in bools] for a in bools]
assert C[0][127]==1 and C[1][1]==0 and C[127][127]==36
d=[max(1,(len(b)-1)**2) for b in sets]
assert all(x>0 for x in d)
W=[]
for a in sets:
    W.append([int(a==s or a==ground-s) if f=='core' else
              int(not(a&s)) if f=='singleton' else
              int(s<=a) if f=='pair' else max(len(a&s)-2,0)
              for f,s in atoms])
V=[]
for f,s in atoms:
    V.append([(1-len(s&b))**2*(1-len((ground-s)&b))**2 if f=='core' else
              int(b==s) if f=='singleton' else
              4*(len(b)-2) if f=='pair' and s<=b else
              12 if f=='four' and s<=b else 0 for b in sets])
H=[[Fraction(x,d[j]) for j,x in enumerate(row)] for row in V]
assert all(x>=0 for A in (W,V,H) for row in A for x in row)

ranges=[range(64),range(64,71),range(71,92),range(92,127)]
family_counts=[0]*4
for i,a in enumerate(sets):
    nonzero=[k for k in range(127) if W[i][k]]
    for j,b in enumerate(sets):
        p=len(b);t=len(a&b)
        closed=[(1-t)**2*(1-(p-t))**2,
                1-t if p==1 else 0,
                4*max(p-2,0)*comb(t,2),
                12*((p-t)*comb(t,3)+2*comb(t,4))]
        fs=[sum(W[i][k]*V[k][j] for k in rr) for rr in ranges]
        assert fs==closed,(i,j,fs,closed)
        assert sum(fs)==d[j]*C[i][j]
        # Actual rational right factor and explicit rational sum, not a
        # tolerance test or a lookup of a stored product.
        assert sum((W[i][k]*H[k][j] for k in nonzero),Fraction(0))==C[i][j]
        for k in range(4):family_counts[k]+=1
report['checks']['independent_matrix_and_factorization']={'rows':128,'columns':128,'width':127,'atom_family_counts':[64,7,21,35],'exact_entry_products':16384,'family_entry_identities':family_counts,'rational_product_all_exact':True,'W_V_H_entrywise_nonnegative':True,'denominators_all_positive':True,'denominator_values':sorted(set(d)),'target_entry_values':sorted({x for row in C for x in row}),'rank_conclusion':'rank_+(C_7) <= 127 < 128; no claim of exact rank 127'}
print('PASS independently constructed 128x128 original matrix = W H through 127 rational nonnegative terms',flush=True)

# Read literal arrays as inert data, never as executable Lean/Python. Array
# order is independently determined above by coordinate combinations.
defs=(LEAN/'NLA/NR03/FamilyDefs.lean').read_text()
for name,ss in [('pairMasks',pairs),('fourMasks',fours)]:
    match=re.search(r'def '+name+r' : Array Nat :=\s*(#\[[\s\S]*?\])',defs)
    assert match
    literal=ast.literal_eval(match.group(1).replace('#[','['))
    assert literal==[sum(2**i for i in s0) for s0 in ss]
data=(LEAN/'NLA/NR03/CertificateData.lean').read_text()
for name,expected in [('certificateWRows',W),('certificateVRows',V),('certificateDenominators',d)]:
    # Definitions following these arrays provide a clear syntax boundary.
    match=re.search(r'def '+name+r' : Array(?: \(Array ℕ\)| ℕ) :=\s*([\s\S]*?)(?=\n\ndef )',data)
    assert match,name
    literal=ast.literal_eval(match.group(1).strip().replace('#[','['))
    assert literal==expected,name
obj=json.loads((PKG/'data/factors_n7.json').read_text())
assert obj['n']==7 and obj['r']==127
for key,expected in [('W',W),('H_scaled',V),('denominators',d)]:assert obj[key]==expected,key
for name,expected,cast in [('W_n7.csv',W,int),('H_scaled_n7.csv',V,int),('H_n7_rational.csv',H,Fraction),('column_denominators_n7.csv',[d],int)]:
    with (PKG/'data'/name).open(newline='') as stream: rows=[[cast(x) for x in row] for row in csv.reader(stream)]
    assert rows==expected,name
report['checks']['secondary_artifact_comparisons']={'Lean_pair_four_masks_match_complete_combination_sets':True,'retained_Lean_W_V_d_arrays_equal_independent_factors':True,'submitted_JSON_equal_independent_factors':True,'all_four_numeric_CSVs_equal_independent_factors':True,'none_used_as_original_matrix_oracle':True}
print('PASS Lean masks and retained W/V/d arrays, submitted JSON and numeric CSVs equal independent construction',flush=True)

# Specific invalid constructions must be rejected by the independently built
# original matrix: omitted singleton correction, one changed positive atom,
# and replacing real subtraction by natural subtraction before squaring.
assert sum(W[0][k]*V[k][1] for k in range(127) if k not in range(64,71)) != d[1]*C[0][1]
assert Fraction(sum(W[0][k]*(V[k][0]+int(k==0)) for k in range(127)),d[0]) != C[0][0]
assert max(1-sum(x*y for x,y in zip(bools[127],bools[127])),0)**2 != C[127][127]
report['checks']['negative_controls']={'omitted_singleton_family_detected':True,'mutated_factor_entry_detected':True,'natural_subtraction_target_corruption_detected':True}
report['status']='PASS'
report['scope']='Independent finite exact arithmetic and complete literal-source audit. Does not claim a new local Lean compilation or authenticate remote canonical receipts.'
OUT.write_text(json.dumps(report,indent=2)+'\n')
print('PASS all finite audits; result',OUT)
