#!/usr/bin/env bash
# Re-runs every check of REPORT.md §5. Exact over Q (K1) or exact over finite fields (K2-K4, K6).
cd "$(dirname "$0")"
mkdir -p logs
PY=${PYTHON:-python3}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONWARNINGS=ignore
($PY check_lemmas_exact.py) > logs/K1_check_lemmas_exact.log 2>&1
bash run_K2.sh > logs/K2_fp_curves_exhaustive.log 2>&1
bash run_K3.sh > logs/K3_fp_rank_exhaustive.log 2>&1
($PY check_tightness_fp.py) > logs/K4_check_tightness_fp.log 2>&1
$PY fp_rank_monomial.py 5 4 2 3 2 8 > logs/K6_fp_rank_monomial.log 2>&1
grep -h -E "ALL OK|FAIL|CONFIRMED|VIOLATED|subsets whose span" logs/*.log
