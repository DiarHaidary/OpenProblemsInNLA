# Building the manuscript

The supplied PDF is in the package root. To rebuild it, run the following from this directory with a standard TeX installation:

```bash
pdflatex -interaction=nonstopmode -halt-on-error SP09_writeup.tex
pdflatex -interaction=nonstopmode -halt-on-error SP09_writeup.tex
```

The second pass resolves theorem and equation references. The source uses standard packages, including amsmath, amsthm, lmodern, microtype, xurl, and hyperref. The JSON certificate in the adjacent `certificate/` directory is an essential companion to the manuscript.
