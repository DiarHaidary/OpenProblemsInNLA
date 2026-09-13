#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
command -v pdflatex >/dev/null 2>&1 || { echo 'pdflatex is required.' >&2; exit 1; }
BUILD=$(mktemp -d)
trap 'rm -rf "$BUILD"' EXIT HUP INT TERM
cd "$ROOT/manuscript"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" ra18.tex > "$BUILD/pass1.log"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" ra18.tex > "$BUILD/pass2.log"
cp "$BUILD/ra18.pdf" "$ROOT/manuscript/ra18.pdf"
printf 'Built %s\n' "$ROOT/manuscript/ra18.pdf"
