# Provenance and limits

## Retained material

`prior_results/` contains the previously delivered recovered archive, including its report, 64 certificates, source code, verification records, source bibliography, and recovery note. Its statements about 64 certificates refer to that earlier edition, not to the enlarged archive. The previous recovery report is preserved rather than rewritten as though it had contained the new results.

The stage counts in the retained certificate set are 2 through 64 inclusive and 80.

## New material in this continuation

The top-level eight-page report adds the all-stage small/large-shift theorem, a weighted rank-two identity, a square-root sufficient condition for a stronger norm bound, and exact rejected-generalization examples. It does not claim an arbitrary-stage solution.

The two new certificate candidates were generated with the retained numerical proposal code for stages 96 and 128. They were then accepted by the retained standard-library integer-interval verifier. The new common-energy squared radii are exactly 7801459205/10000000000 and 8069729082/10000000000, respectively.

The initial q=128 invocation completed all mathematical checks but encountered a file-output permission problem. Its successful mathematical-check JSON was captured. The subsequent complete recheck in `results/full_recheck/` is the authoritative clean end-to-end run for all 66 certificates; consult its exit status, summary, and logs.

The new exact obstruction checker uses the earlier independent Q(sqrt(6)) arithmetic and adds exact complex-field operations. Its complex-shift obstruction has positive real part but is not a positive real scalar, and its generic-matrix obstruction is not a Radau matrix. Neither is an IE-27 counterexample.

Floating-point experiments informed the search but are not proof decisions. Their scripts and outputs are separated from exact certificate checks. Exploratory dead ends and uncompleted large-stage runs are not advertised as certified results.

## Research status

The problem statement and relevant primary-source HTML were reread at the web addresses listed in `references/sources.md`. No arbitrary-stage proof was located in that bounded check. More importantly, this continuation itself does not supply the missing intermediate-shift inequality at unrestricted stages.

The verification is an exact-arithmetic program plus the written arguments, not formal proof-assistant verification or external peer review. The literature check is not exhaustive.
