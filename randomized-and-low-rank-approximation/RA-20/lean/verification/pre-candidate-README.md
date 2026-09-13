# RA-20 Lean statement package — awaiting independent review

Formalization author: **George Stepaniants**, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA. The original negative resolution remains attributed to the **Codex automated
maintainer audit** in the retained repository source. Kubjas, Sodomaco and
Tsigaridas retain credit for the original conjecture.

This is a **statement-only candidate**. It contains no completed Lean theorem
or `Solution.lean`, and claims no Lean verification of RA-20. The twelve `sorry`
terms in `Challenge.lean` are deliberate reference placeholders; they may not be
imported by a future implementation. Two independent statement approvals and an
explicit coordinating gate are required before mathematical proof work starts.

The original target is the joint generic critical-point formula for all
`n >= 3` and `1 <= s <= min(4,n)`. The planned counterexample proves the true
generic count at `n=s=3` is three, and therefore negates that full target. It
does not settle the other formulas or propose corrected values elsewhere.

`NLA/RA20/Definitions.lean` uses the real library definitions of matrix rank,
the reduced coordinate ring of the actual complex point variety,
`Algebra.smoothLocus`, and the Zariski tangent directions obtained from its full
vanishing ideal. Criticality uses the actual complex Fréchet derivative of
`sum (Xij-Uij)^2`. It is the complex bilinear extension of the full Frobenius
metric: there is no complex conjugation, and both off-diagonal entries occur.

Generic counts quantify over an arbitrary nonempty principal Zariski-open set
of all symmetric data, not just the specific open set used in the source.
`Cardinal.mk` prevents an infinite set from being silently counted as zero.
The three-coordinate smoothness and critical-point formulas are obligations to
prove from these definitions, not definitions of smoothness or criticality.

Read [the exact contracts](Challenge.lean), [numerical and mathematical
targets](NUMERICAL_TARGETS.md), and [source correspondence](SourceCorrespondence.md)
before reviewing. The principal unresolved implementation burden is the genuine
algebraic smooth-locus theorem; statement elaboration does not establish it.

The pinned toolchain is Lean 4.33.1, Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`, and LeanCert
`621a43d7cf21f87872392a01e874f2f1dbddc926`, with all ten dependency revisions in
`lake-manifest.json`. The statement checker uses a fresh project prefix and the
ten read-only dependency object trees; it invokes neither Lake nor a download.

```
python3 verification/check_statements.py
python3 verification/reconstruct.py
```

These are author-local macOS statement/diagnostic checks. Raw attempts, including
failed API or inspection attempts, are retained. The exact statements must be
frozen and independently reviewed before proofs. Final proof review, all-export
LeanCert `#assert_trust kernel` and axiom checks, fresh Linux Comparator with the
repository's full negative/control suite, actual v0.4 `formalization.yaml`, and
publication review remain future gates. `comparator.json` specifies all twelve
planned exports and the standard-three axiom whitelist with no definition
exceptions; it does not report a Comparator result.

The proof organization, immutable dependency pins, fresh-source/checker separation
and trust review follow the campaign's audited infrastructure, with examples
from [Schiffer](https://github.com/jaumededios/Schiffer/tree/2938e277969c329caf154e48a3d8823f3635c7f1)
and [Forsythe](https://github.com/sgstepaniants/Forsythe/tree/8d1b0c0545a77b40245e84705aa7d273e6c81e62).
No theorem from those projects is assumed. The reused RA-09 configuration and
fresh-prefix script pattern are credited; RA-09 proofs are not dependencies.
The Tau Ceti review angles apply as described in the upstream `docs/lean/REVIEW.md`.
This exact algebra target needs no numerical interval certificate: LeanCert's
role is kernel trust/dependency auditing, with no native execution trust.
