#!/usr/bin/env bash
# Rebuild without leaving TeX intermediates next to the deliverable.
set -euo pipefail
cd "$(dirname "$0")/manuscript"
command -v pdflatex >/dev/null || { echo "Install a TeX distribution with pdflatex." >&2; exit 1; }
build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT
for pass in 1 2 3; do
    if ! pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory="$build_dir" ra11_partial_results.tex > "$build_dir/pass-$pass.log"; then
        cat "$build_dir/pass-$pass.log" >&2
        exit 1
    fi
done
if grep -Eq 'undefined references|Label\(s\) may have changed|Overfull' "$build_dir/pass-3.log"; then
    cat "$build_dir/pass-3.log" >&2
    echo 'Review TeX warnings before distributing this PDF.' >&2
    exit 1
fi
cp "$build_dir/ra11_partial_results.pdf" ra11_partial_results.pdf
printf 'Built %s\n' "$PWD/ra11_partial_results.pdf"
