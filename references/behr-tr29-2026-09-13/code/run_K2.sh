#!/usr/bin/env bash
# K2: exhaustive finite-field test of Lemma 3 (all (1,q)- and (p,1)-curves)
cd "$(dirname "$0")"
mkdir -p logs
PY=${PYTHON:-python3}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONWARNINGS=ignore
for args in "5 1 1" "5 2 1" "5 1 2" "5 2 2" "5 3 1" "5 3 2" "5 2 3" "5 3 3" "7 2 2" "7 4 2 1q" "7 5 2 1q" "13 5 2 1q" "17 1 1"; do
  $PY fp_curves_exhaustive.py $args; echo
done
