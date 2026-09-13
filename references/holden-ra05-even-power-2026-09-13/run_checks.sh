#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python3 code/check_manifest.py
python3 code/verify.py
python3 code/check_exact_certificate.py
