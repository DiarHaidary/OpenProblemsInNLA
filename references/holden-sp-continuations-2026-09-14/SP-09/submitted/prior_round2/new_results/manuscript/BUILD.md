# Build the new manuscript

From the archive root, with a LaTeX installation containing the standard AMS, Latin Modern, geometry, microtype, xurl, and hyperref packages:

```bash
mkdir -p build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build new_results/manuscript/SP09_local_invariance.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build new_results/manuscript/SP09_local_invariance.tex
```

The output is `build/SP09_local_invariance.pdf`. The supplied root PDF is compiled from this source. No external figures, private fonts, bibliography database, or online LaTeX service is required.
