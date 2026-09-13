#!/bin/sh
set -eu
cd "$(dirname "$0")"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
for PASS in 1 2; do
  if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$TMP" ra01_round4.tex > "$TMP/pass-$PASS.log" 2>&1; then
    cat "$TMP/pass-$PASS.log" >&2
    exit 1
  fi
done
cp "$TMP/ra01_round4.pdf" ra01_round4.pdf
cp "$TMP/ra01_round4.log" ../verification/latex_build.log
