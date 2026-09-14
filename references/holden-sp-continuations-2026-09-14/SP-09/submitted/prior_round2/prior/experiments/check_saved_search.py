#!/usr/bin/env python3
"""Audit the saved heuristic searches. This is not an exact lower-bound proof."""
from pathlib import Path
import json
import numpy as np
from search_orbits import value

def main():
    folder=Path(__file__).resolve().parent/'data'
    records=[json.loads(line) for line in (folder/'outer_log.jsonl').read_text().splitlines()]
    unitary_error=0.;value_error=0.
    for r in records:
        s=np.load(folder/f"outer_case{r['case']}.npz")
        a,b,U,V=s['a'],s['b'],s['baseU'],s['ampU']
        unitary_error=max(unitary_error,float(np.linalg.norm(U.conj().T@U-np.eye(len(U)),2)),
                          float(np.linalg.norm(V.conj().T@V-np.eye(len(V)),2)))
        value_error=max(value_error,abs(value(a,b,U)-r['base_upper']),
                        abs(value(np.repeat(a,2),np.repeat(b,2),V)-r['amplified_upper']))
    summary={'cases':len(records),'base_dimension':4,'amplification':2,
             'largest_base_minus_amplified_estimate':max(r['candidate_gap'] for r in records),
             'largest_unitarity_residual':unitary_error,'largest_recomputed_value_discrepancy':value_error,
             'interpretation':'No candidate gap above 1e-6 was found. Numerical minima are not certified global minima.'}
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
