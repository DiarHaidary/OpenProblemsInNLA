"""Generate certified full-coordinate centers from reduced root proposals.

The input's Q-data are numerical search parameters. Certification is against
exact dyadic ordinary-coordinate data from --ordinary-data, not a round-trip
coordinate transform of the Q-data. Failed proposals are reported and dropped.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import sys,argparse,time,json
from concurrent.futures import ThreadPoolExecutor
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'));sys.path.insert(0,str(BASE/'verify'))
from polynomial import evaluate,refine,forms
from backend import check,load
from separation import check_disjoint,select_disjoint
from quad_proposal import refine_quad
from fast_reduction import lift

def main(args):
    z=np.load(args.input,allow_pickle=False);a_roots=z['roots'].copy();uq=z['U'].copy()
    target=np.load(args.ordinary_data,allow_pickle=False);u=target['U'].ravel().copy()
    m=uq.shape[0]//2;n=2*m;J,Q,P=forms(m);Pi=np.linalg.inv(P)
    if args.limit:a_roots=a_roots[:args.limit]
    blocks=[np.ascontiguousarray(v) for v in (uq[:m,:m],uq[:m,m:],uq[m:,:m],uq[m:,m:])]
    evaluate(np.eye(n,dtype=complex).ravel(),u,n);load();lift(a_roots[0],*blocks)
    started=time.perf_counter()
    def one(pair):
        i,a=pair
        try:
            xq,_,_=lift(a,*blocks);x=(P@xq@Pi).ravel()
            for attempt in range(3):
                x,ok=refine(x,u,n,5)
                if not ok: return i,None,None,'Newton proposal failed'
                F,H=evaluate(x,u,n);B=np.linalg.inv(H)
                passed,re,bounds=check(x,u,B)
                if passed:return i,x,re,None
            x=refine_quad(x,u,4)
            F,H=evaluate(x,u,n);B=np.linalg.inv(H)
            passed,re,bounds=check(x,u,B)
            if passed:return i,x,re,None
            return i,None,None,'Contraction inequalities failed after high-precision proposal'
        except Exception as e:return i,None,None,str(e)
    passed=[];radii=[];indices=[];failed=[]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i,x,re,error in pool.map(one,enumerate(a_roots)):
            if error:failed.append({'input_index':i,'reason':error})
            else:indices.append(i);passed.append(x);radii.append(re)
            if (i+1)%1000==0:
                print(json.dumps({'processed':i+1,'passed':len(passed),'failed':len(failed),
                                  'elapsed_seconds':time.perf_counter()-started}),flush=True)
    roots=np.asarray(passed);radii=np.asarray(radii,dtype=np.int64)
    keep,rejected=select_disjoint(roots,radii)
    removed=[indices[i] for i,j in rejected]
    roots=roots[keep];radii=radii[keep];indices=[indices[i] for i in keep]
    distinct=check_disjoint(roots,radii)
    if not distinct['distinct']:raise AssertionError('Selected balls were not exactly disjoint')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(args.output,roots=roots,U=u,radius_exponents=radii,
                        input_indices=np.asarray(indices,dtype=np.int64))
    report={'rank':m,'input_candidates':len(a_roots),'certified_distinct_simple_roots':len(roots),
            'completeness_proved':False,'failed_proposals':failed,
            'removed_unseparated_input_indices':removed,'separation':distinct,
            'elapsed_seconds':time.perf_counter()-started,'ordinary_data_source':str(args.ordinary_data),
            'input_source':str(args.input)}
    args.output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='failed_proposals'},indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('fixed_m4.npz'))
    p.add_argument('--ordinary-data',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit',type=int);p.add_argument('--workers',type=int,default=1)
    main(p.parse_args())
