#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python code/check_manifest.py
TMPDIR_RA05=$(mktemp -d)
trap 'rm -rf "$TMPDIR_RA05"' EXIT HUP INT TERM
python code/check_certificate.py --output "$TMPDIR_RA05/exact.json"
python code/verify_non_even.py --output "$TMPDIR_RA05/numerical.json"
