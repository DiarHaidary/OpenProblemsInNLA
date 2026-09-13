#!/usr/bin/env bash
# K3: exhaustive finite-field search for decompositions of length 2(p+q)-1 (and controls of length 2(p+q))
cd "$(dirname "$0")"
mkdir -p logs
PY=${PYTHON:-python3}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONWARNINGS=ignore
for args in "5 1 1 3" "5 1 1 4" "5 2 1 5" "5 2 1 6" "5 1 2 5" "7 1 1 3" "7 2 1 5" "5 2 2 7" "5 3 1 7"; do
  $PY fp_rank_exhaustive.py $args; echo
done
