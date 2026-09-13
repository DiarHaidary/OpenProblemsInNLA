# MI-05: order-four partial results — Sidney Holden

**Author:** Sidney Holden.  
**Affiliation:** Center for Computational Biology, Flatiron Institute, Simons Foundation.  
**Submission date:** 13 September 2026.  
**Status:** Partial results; unrestricted MI-05 remains open.

[Manuscript PDF](report.pdf) · [Editable source](report.tex) · [Independent review](independent-review.md) · [Original target](../../matrix-inequalities-and-norms/MI-05/README.md).

## Verified affiliation

Checked on 13 September 2026 against the [official Simons Foundation profile](https://www.simonsfoundation.org/people/sidney-holden/) and [CCB staff directory](https://www.simonsfoundation.org/flatiron/center-for-computational-biology/about/people/?group=biological-transport&type=ccb-staff). Both identify Sidney Holden as a Flatiron Research Fellow in Biological Transport Networks, CCB, Flatiron Institute. The current institutional profile supersedes the historical Edinburgh student affiliation. Authorship was supplied explicitly by Sidney Holden; affiliation does not imply institutional endorsement.

## Scope

- Theorem 2.1 gives a universal fourteen-term signed determinant identity in order four.
- Theorems 3.1–3.2 establish optimal negative mass and uniqueness on positive-obstruction regions.
- Corollary 4.1 and Theorem 4.2 prove the conjecture for all complex spectra on a specified class, including an operator-norm ball of radius 1/100 around the displayed Hadamard matrix. Corollary 4.3 extends these classes by block sums.
- Theorem 5.1 gives a support-direction criterion; Theorem 6.1 bounds the complex obstruction by 1/6.
- Lemma 7.1 and Theorem 7.2 give the sharp real-orthogonal obstruction constant, the positive root of 32t³ + 48t² + 28t − 1 = 0.

These results do not prove the determinant inclusion for arbitrary order-four unitaries or arbitrary dimensions. Negative spectrum-independent weights are not counterexamples to the original spectrum-dependent convex-hull question. The general zero-obstruction classification is also not established here. The canonical status remains **Partially resolved** under the repository resolution policy.

## Provenance and review

The supplied archive `MI-05_round5_package.zip` has SHA-256 `4729441f0a8862379e167fed31067743c0c7155a75c816fdbb7cc6833ea1b14b`. Its eight original files are preserved in [submitted/](submitted/), including its original manifest and delivery status. It contains no PDF, results directory, previous-round archive or extensions. Its delivery status says the exact audit had not passed; this is not relabeled as an original successful audit. References to absent companion material are historical context, not proof premises.

The repository edition adds the requested author/verified affiliation/date and replaces the absent-audit reference with the new verification record and review disclosure. Line-break opportunities were added to one long inline coordinate list for PDF layout. Mathematical statements and proofs are unchanged. Code copies are unchanged. No historical novelty claim is made; prior source attribution is retained.

A separate Codex AI agent independently reviewed the mathematics and exact checks; see its [dated report](independent-review.md). This is informal AI review, not formal verification or external human peer review. No Lean verification was performed. Fresh execution evidence is in [verification/audit.json](verification/audit.json). The supplied checks corroborate finite identities and examples; they do not resolve unrestricted MI-05.

## Duplicate screen

Fetched upstream main and all fork branches on 13 September 2026. MI-05 remains partially resolved on upstream main; the fetched history of its canonical page contains no full-solution submission. Searches of upstream pull requests for MI-05 and of Sidney Holden's pull requests found no prior full MI-05 solution. Existing source-status material and prior credit are retained. This is a new branch and new pull request against `ajt60gaibb/OpenProblemsInNLA:main`.

## Reproduction

Python 3 with SymPy 1.14.0 was used. From this directory:

```sh
python3 submitted/code/check_manifest.py
python3 code/verify_analytic.py
python3 -O code/verify_analytic.py
python3 -m unittest discover -s code -p test_analytic.py -v
python3 -O -m unittest discover -s code -p test_analytic.py -v
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```
