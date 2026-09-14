CXX ?= g++
CXXFLAGS ?= -O3 -std=c++17
PYTHON ?= python
.PHONY: backend quad verify tests tests-core report clean

backend: verify/exact_backend.so
verify/exact_backend.so: verify/exact_backend.cpp
	$(CXX) $(CXXFLAGS) -fPIC -shared $< -o $@

# Optional proposal helper. Not needed to verify the final stored centers.
quad: verify/quad_proposal_kernel.so
verify/quad_proposal_kernel.so: verify/quad_proposal.cpp
	$(CXX) $(CXXFLAGS) -fPIC -shared $< -lquadmath -o $@

verify: backend
	$(PYTHON) verify/verify_roots.py certificates/rank1.npz --workers 1 --output results/rerun_rank1.json
	$(PYTHON) verify/verify_roots.py certificates/rank2.npz --workers 1 --output results/rerun_rank2.json
	$(PYTHON) verify/verify_roots.py certificates/rank3.npz --workers 4 --output results/rerun_rank3.json
	$(PYTHON) verify/verify_roots.py certificates/rank4.npz --workers 4 --output results/rerun_rank4.json

tests-core: backend
	$(PYTHON) verify/test_backend.py
	$(PYTHON) verify/test_factorization.py
	$(PYTHON) verify/test_stein_form.py
	$(PYTHON) verify/test_boundary.py
	$(PYTHON) verify/test_selection.py
	$(PYTHON) verify/test_polynomial_system.py
	$(PYTHON) verify/test_zero_coupling.py

tests: tests-core quad
	$(PYTHON) verify/test_new_checks.py

report: report.tex
	pdflatex -interaction=nonstopmode -halt-on-error report.tex
	pdflatex -interaction=nonstopmode -halt-on-error report.tex

clean:
	rm -f report.aux report.log report.out
