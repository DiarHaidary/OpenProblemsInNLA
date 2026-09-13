"""Run the new component checks and unchanged prior suites; retain outcomes.

No diagnostic is an oracle lower-bound certificate.  Numerical examples need
not meet the proof's deliberately conservative sufficient constant condition.
"""
from __future__ import annotations
import csv, hashlib, json, math, os, platform, re, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import scipy
import mpmath
from scipy.linalg import null_space
from src.weighted_krylov import (
    chebyshev_geometry, hard_spectrum, interpolation_budget, numerical_cone_optimum,
    shifted_kernel_posterior_geometry, shifted_rank_one_filter,
)
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'


def suite(name: str, cwd: Path, directory: str='tests') -> dict:
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s',directory,'-v'],
        cwd=cwd, text=True, capture_output=True, env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
    log=result.stdout+result.stderr
    (OUT/f'{name}.log').write_text(log)
    match=re.search(r'Ran (\d+) tests?',log)
    return {'name':name,'exit_code':result.returncode,
            'test_count':int(match.group(1)) if match else None,'log':f'{name}.log'}


def extract_safe(source: Path, target: Path) -> None:
    target=target.resolve()
    with zipfile.ZipFile(source) as archive:
        for item in archive.infolist():
            candidate=(target/item.filename).resolve()
            if not candidate.is_relative_to(target):
                raise ValueError(f'unsafe archive member: {item.filename}')
        archive.extractall(target)


def save_rows(name: str, rows: list[dict]) -> None:
    keys=list(dict.fromkeys(key for row in rows for key in row))
    with (OUT/name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=keys);writer.writeheader();writer.writerows(rows)


def cone_diagnostics() -> dict:
    cases=[]
    for n,k,b,d in [(512,1,1,4),(512,1,1,20),(1024,2,3,12),
                     (2048,2,4,20),(4096,1,2,40),(4096,1,2,80)]:
        for tag,e in [('transition',(math.log(n/k)/(n/k))**2),('fixed',.08)]:
            cases.append((n,k,b,d,tag,e))
    rows=[];index=0
    for n,k,b,d,tag,e in cases:
        for trial in range(6):
            seed=13140000+index;index+=1
            row={'n':n,'k':k,'gaussian_width_B':b,'degree':d,'regime':tag,
                 'epsilon':e,'trial':trial,'seed':seed}
            try:
                spec=hard_spectrum(n,k,b,d,e)
                omega=np.random.default_rng(seed).normal(size=(n,b))
                row.update({'multiplicity_budget_condition':spec.allocation_condition,
                            'log_sufficient_analytic_condition':spec.log_analytic_condition,
                            'sufficient_analytic_condition':spec.log_analytic_condition<=0})
                row.update(interpolation_budget(omega,spec))
                row.update(numerical_cone_optimum(omega,spec))
                row['status']='ok'
            except Exception as error:
                row['status']='diagnostic_error';row['error']=f'{type(error).__name__}: {error}'
            rows.append(row)
    save_rows('weighted_cone_trials.csv',rows)
    good=[r for r in rows if r['status']=='ok']
    return {'rows':len(rows),'numerical_errors':len(rows)-len(good),
            'no_cone_diagnostics':int(sum(r['numerical_no_nonzero_cone_vector'] for r in good)),
            'cone_not_excluded_diagnostics':sum(not r['numerical_no_nonzero_cone_vector'] for r in good),
            'sufficient_constant_condition_met':sum(r['sufficient_analytic_condition'] for r in good),
            'minimum_optimum_over_delta':min(r['optimum_over_delta'] for r in good),
            'maximum_optimum_over_delta':max(r['optimum_over_delta'] for r in good),
            'maximum_tail_feature_condition':max(r['tail_feature_condition'] for r in good)}


def gaussian_diagnostics() -> dict:
    rng=np.random.default_rng(13146001);rows=[];draws=1000
    for b in (1,2,4,8):
        for ratio in (8,12,32):
            m=ratio*b;values=[]
            for _ in range(draws):
                g=rng.normal(size=(m,b));values.append(m/np.linalg.eigvalsh(g.T@g)[0])
            values=np.asarray(values)
            rows.append({'m':m,'B':b,'draws':draws,'mean_m_times_inverse_gram_norm':float(values.mean()),
                         'sample_standard_error':float(values.std(ddof=1)/math.sqrt(draws)),
                         'max_sample':float(values.max()),'proved_expectation_bound':3000})
    save_rows('reciprocal_gram_trials.csv',rows)
    return {'cases':len(rows),'draws':len(rows)*draws,
            'maximum_empirical_scaled_mean':max(r['mean_m_times_inverse_gram_norm'] for r in rows)}


def scalar_diagnostics() -> dict:
    rows=[]
    for d in (1,2,5,20,100,1000):
        for e in (1e-60,1e-30,1e-12,1e-6,.001,.03,.49):
            g=chebyshev_geometry(d,e)
            rows.append({'degree':d,'epsilon':e,'weighted_L_over_T':g.weighted_lagrange_over_chebyshev,
                         'sH':math.sqrt(e)*g.harmonic_number,
                         'ratio_to_proved_bound':g.weighted_lagrange_over_chebyshev/(10*math.sqrt(e)*g.harmonic_number),
                         'log_T':g.log_chebyshev_at_spike,'proved_log_T_upper':2*d*math.sqrt(e),
                         'diagnostic_matrix_spike_representable':1<1+e<1+2*e})
    save_rows('weighted_interpolation_grid.csv',rows)
    return {'rows':len(rows),'maximum_ratio_to_proved_bound':max(r['ratio_to_proved_bound'] for r in rows)}


def shifted_diagnostics() -> dict:
    rng=np.random.default_rng(13146002);rows=[]
    for n,k,t in ((32,1,3),(40,2,5),(48,3,7)):
        for h in (.01,.3,4.):
            for trial in range(5):
                r=n-k;u=np.linalg.qr(rng.normal(size=(n,r)),mode='reduced')[0]
                g=rng.normal(size=(r,r+1));a=u@(g@g.T+h*np.eye(r))@u.T
                v=np.linalg.qr(rng.normal(size=(n,t)),mode='reduced')[0];rest=null_space(v.T)
                j=v.T@a@v;b=rest.T@a@v;s=rest.T@a@rest-b@np.linalg.solve(j,b.T)
                row={'n':n,'k':k,'t':t,'shift_h':h,'trial':trial,'compression_above_wall':np.linalg.eigvalsh(j)[0]>h}
                if row['compression_above_wall']:
                    _,ev=np.linalg.eigh(s);q=ev[:,:k]
                    info=shifted_kernel_posterior_geometry(j,b,q,h);qperp=info['complement']
                    w=qperp.T@s@qperp-h*info['shorted_R']
                    row.update({'minimum_shifted_schur_eigenvalue':float(np.linalg.eigvalsh(w)[0]),
                        'full_positive_eigenvalue_margin':float(np.linalg.eigvalsh(a)[k]-h),
                        'trace_identity_error':abs(info['log_density_up_to_constant']-info['log_density_with_trace_constant']-h/2*np.trace(info['R']))})
                else:row['status']='posterior_formula_domain_not_met'
                rows.append(row)
    save_rows('shifted_posterior_geometry.csv',rows)
    inside=[r for r in rows if r['compression_above_wall']]
    return {'rows':len(rows),'outside_stated_domain':len(rows)-len(inside),
            'maximum_trace_identity_error':max(r['trace_identity_error'] for r in inside),
            'minimum_shifted_schur_eigenvalue':min(r['minimum_shifted_schur_eigenvalue'] for r in inside)}


def resolvent_diagnostics() -> dict:
    rng=np.random.default_rng(13146111); rows=[]; draws=2000
    for r in (1,4,12,32):
        spectra=[]
        for _ in range(draws):
            g=rng.normal(size=(r,r+1)); spectra.append(np.linalg.eigvalsh(g@g.T))
        spectra=np.asarray(spectra)
        for ratio in (.001,.1,1.,10.):
            t=r*ratio; inverse=1/(spectra+t); traces=inverse.sum(axis=1)
            rhs=t*traces+t*(inverse**2).sum(axis=1)+t*traces**2
            rows.append({'r':r,'N':r+1,'resolvent_shift':t,'draws':draws,
                'empirical_mean_trace':float(traces.mean()),'proved_mean_trace_upper':math.sqrt(r/t),
                'empirical_mean_over_upper':float(traces.mean()/math.sqrt(r/t)),
                'identity_rhs_empirical_mean':float(rhs.mean()),'identity_rhs_target':r,
                'identity_rhs_standard_error':float(rhs.std(ddof=1)/math.sqrt(draws)),
                'smallest_eigenvalue_empirical_mean':float(spectra[:,0].mean()),
                'smallest_eigenvalue_exact_mean':2/r})
    save_rows('wishart_resolvent_trials.csv',rows)
    return {'cases':len(rows),'independent_gram_draws':4*draws,
        'maximum_mean_trace_over_proved_upper':max(r['empirical_mean_over_upper'] for r in rows),
        'maximum_identity_standard_errors':max(abs(r['identity_rhs_empirical_mean']-r['identity_rhs_target'])/r['identity_rhs_standard_error'] for r in rows)}


def shifted_rank_one_diagnostics() -> dict:
    """Rotation-equivariant method evaluated in an eigenbasis for efficiency.

    Only the validator receives the sampled spectrum. Each algorithm product
    is charged, including all columns in an exact-recovery branch.
    """
    class DiagonalOracle:
        def __init__(self,diagonal):
            self.diagonal=np.asarray(diagonal); self.n=len(diagonal); self.queries=0
        def product(self,block,transpose=False):
            block=np.asarray(block)
            if block.ndim!=2 or block.shape[0]!=self.n:raise ValueError('invalid block')
            self.queries+=block.shape[1]
            return self.diagonal[:,None]*block
    rows=[];index=0
    for n in (64,128,256,512):
        for tag,e in [('transition',(math.log(n)/n)**2),('inverse_dimension',1/n),('linear_cap',1/n**2)]:
            for trial in range(8):
                seed=13146200+index; index+=1; rng=np.random.default_rng(seed)
                row={'n':n,'k':1,'epsilon':e,'regime':tag,'trial':trial,'seed':seed}
                try:
                    g=rng.normal(size=(n-1,n)); w=np.linalg.eigvalsh(g@g.T)
                    h=400*n*e; diagonal=np.r_[1.,1-(h+w)/(100*n)]
                    oracle=DiagonalOracle(diagonal)
                    z,meta=shifted_rank_one_filter(oracle,e,rng); row.update(meta)
                    norm_event=(h+w[-1])<=100*n
                    sigma2=np.sort(np.abs(diagonal))[-2]; tau=(1+e)*sigma2
                    if norm_event and np.argmax(np.abs(diagonal))==0 and tau<1:
                        E=tau*tau-diagonal[1:]**2
                        cone=(1-tau*tau)*np.sum(z[1:,0]**2/E)/(z[0,0]**2)
                        success=cone<=1+1e-9
                        row['actual_target_cone_ratio']=float(cone)
                    else:
                        residual=np.diag(diagonal)@(np.eye(n)-z@z.T)
                        ratio=np.linalg.norm(residual,2)/sigma2
                        row['residual_ratio']=float(ratio); success=ratio<=1+e+1e-9
                    row.update({'status':'ok','success_diagnostic':bool(success),
                        'norm_event':bool(norm_event),'minimum_gram_eigenvalue':float(w[0]),
                        'minimum_gram_event':bool(w[0]<=25*n*e),
                        'orthogonality_error':abs(float((z.T@z)[0,0])-1),
                        'queries_over_F':meta['actual_queries']/meta['F_scale']})
                except Exception as error:
                    row.update({'status':'diagnostic_error','error':f'{type(error).__name__}: {error}'})
                rows.append(row)
    save_rows('shifted_rank_one_trials.csv',rows)
    good=[r for r in rows if r['status']=='ok']
    return {'rows':len(rows),'numerical_errors':len(rows)-len(good),
        'successes':sum(r['success_diagnostic'] for r in good),
        'failures':sum(not r['success_diagnostic'] for r in good),
        'polynomial_runs':sum(r['branch']=='shifted_ensemble_polynomial' for r in good),
        'exact_column_runs':sum(r['branch']=='exact_columns' for r in good),
        'maximum_queries_over_F':max(r['queries_over_F'] for r in good),
        'maximum_orthogonality_error':max(r['orthogonality_error'] for r in good)}


def resolvent_holdout() -> dict:
    """Independent larger check of two high-variance cases; originals retained.

    Draw counts and seed are fixed here, not selected after seeing this run.
    No pass/fail claim is assigned to a Monte Carlo expectation estimate.
    """
    rng=np.random.default_rng(13146666); rows=[]; draws=250000; batch=5000
    for r in (1,4):
        t=.001*r; total=0.; total_sq=0.; trace_total=0.; below_shift=0
        for _ in range(draws//batch):
            g=rng.normal(size=(batch,r,r+1)); w=np.linalg.eigvalsh(g@g.transpose(0,2,1))
            inverse=1/(w+t); trace=inverse.sum(axis=1)
            rhs=t*trace+t*(inverse**2).sum(axis=1)+t*trace**2
            total+=float(rhs.sum()); total_sq+=float((rhs**2).sum()); trace_total+=float(trace.sum())
            below_shift+=int((w[:,0]<t).sum())
        mean=total/draws; variance=(total_sq-draws*mean*mean)/(draws-1)
        rows.append({'r':r,'N':r+1,'resolvent_shift':t,'draws':draws,
            'seed':13146666,'identity_rhs_mean':mean,'identity_rhs_target':r,
            'sample_standard_error':math.sqrt(variance/draws),
            'mean_trace':trace_total/draws,'smallest_below_shift_count':below_shift,
            'expected_smallest_below_shift_count':draws*(-math.expm1(-r*t/2))})
    save_rows('wishart_resolvent_holdout.csv',rows)
    return {'cases':len(rows),'independent_gram_draws':draws*len(rows),'rows':rows,
            'original_2000_draw_results_retained':True,'no_statistical_pass_fail_claim':True}


def main() -> int:
    OUT.mkdir(exist_ok=True)
    suites=[suite('new_components',ROOT)]
    previous=ROOT/'prior/RA14_finite_accuracy_v5.zip'
    with tempfile.TemporaryDirectory(prefix='ra14_v6_prior_') as temp:
        base=Path(temp);extract_safe(previous,base)
        v5=base/'RA14_finite_accuracy_v5'
        suites.append(suite('unchanged_v5_components',v5))
        base4=base/'nested_v4';base4.mkdir()
        extract_safe(v5/'prior/RA14_adaptive_lower_bounds_v4.zip',base4)
        v4=base4/'RA14_adaptive_lower_bounds_v4'
        suites.append(suite('unchanged_v4_components',v4))
        suites.append(suite('unchanged_v3_upper_bound',v4/'upper_bound'))
    summary={'created_utc':datetime.now(timezone.utc).isoformat(),
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                       'mpmath':mpmath.__version__,'platform':platform.platform()},
        'suites':suites,'all_suites_passed':all(s['exit_code']==0 for s in suites),
        'total_tests':sum(s['test_count'] or 0 for s in suites),
        'weighted_cone':cone_diagnostics(),'reciprocal_gram':gaussian_diagnostics(),
        'scalar_grid':scalar_diagnostics(),'shifted_posterior':shifted_diagnostics(),
        'wishart_resolvent':resolvent_diagnostics(),'wishart_resolvent_holdout':resolvent_holdout(),
        'shifted_rank_one':shifted_rank_one_diagnostics(),
        'prior_zip_sha256':hashlib.sha256(previous.read_bytes()).hexdigest(),
        'limitations':[
            'Full RA-14 remains PARTIAL; this round does not improve the unrestricted bounds.',
            'The matching theorem is for deterministic-width full-block span queries only.',
            'Numerical trials test whole Krylov coefficient spaces, not every legal oracle algorithm.',
            'The practical spectra need not satisfy the theorem\'s conservative sufficient constant condition.',
            'A floating-point no-cone diagnostic is not an interval or formal certificate.',
            'The shifted posterior identity requires J > h I; no all-adaptive first-exit bound is proved.',
            'The shifted rank-one algorithm has an ensemble-average guarantee, not a pointwise all-input F-scale guarantee.',
            'That shifted rank-one ensemble is too easy to witness a linear critical-transition lower bound.',
            'No claims of novelty, independent peer review, or proof-assistant verification are made.',
            'All recorded errors and countervailing diagnostic outcomes are retained.',
        ]}
    summary['completed_utc']=datetime.now(timezone.utc).isoformat()
    (OUT/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return 0 if summary['all_suites_passed'] else 1

if __name__=='__main__':raise SystemExit(main())
