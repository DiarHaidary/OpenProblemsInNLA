#!/bin/sh
set -eu
cd "$(dirname "$0")"
(cd manuscript && pdflatex -interaction=nonstopmode -halt-on-error part_i_non_even.tex && pdflatex -interaction=nonstopmode -halt-on-error part_i_non_even.tex && pdflatex -interaction=nonstopmode -halt-on-error part_ii_cover.tex)
python code/assemble_pdf.py
