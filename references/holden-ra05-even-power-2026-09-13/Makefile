.PHONY: pdf check clean
pdf:
	pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
	pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
check:
	sh ./run_checks.sh
clean:
	rm -f manuscript.aux manuscript.log manuscript.out manuscript.toc
