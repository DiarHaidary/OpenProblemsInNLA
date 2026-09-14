"""Merge root proposals with certified radii while preserving an old set.

Selection is exact, but the merged file MUST be freshly verified with
verify/verify_roots.py before its count is used as a proved lower bound.
"""
from pathlib import Path
import argparse,sys,json
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'verify'))
from separation import select_disjoint,check_disjoint

def main(args):
    arrays=[];exponents=[];u=None;counts=[]
    for path in [args.prior,args.new]:
        with np.load(path,allow_pickle=False) as z:
            x=z['roots'].copy();v=z['U'].ravel().copy();r=z['radius_exponents'].copy()
        if x.dtype!=np.dtype('complex128') or v.dtype!=np.dtype('complex128'):
            raise ValueError('Complex binary64 inputs required')
        if u is None:u=v
        elif not np.array_equal(u.view(np.uint64),v.view(np.uint64)):
            raise ValueError('The exact ordinary-coordinate data differ')
        if r.shape!=(len(x),):raise ValueError('One certified radius exponent is required per center')
        arrays.append(x);exponents.append(r);counts.append(len(x))
    x=np.concatenate(arrays);r=np.concatenate(exponents)
    retained,rejected=select_disjoint(x,r,mandatory_count=counts[0])
    x=x[retained];r=r[retained]
    separation=check_disjoint(x,r)
    if not separation['distinct']:raise AssertionError('Merged selected balls were not separated')
    np.savez_compressed(args.output,roots=x,U=u,radius_exponents=r)
    report={'input_counts':counts,'preserved_prior_centers':counts[0],
            'selected_centers':len(x),'rejected_unseparated_centers':len(rejected),
            'separation':separation,'fresh_root_verification_still_required':True,
            'completeness_proved':False}
    args.output.with_suffix('.merge.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--new',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
