# NR-03: second independent full mathematical source review

Reviewer: `/root`, OpenAI Codex AI agent, 13 September 2026. I integrated the
canonical package and edited its descriptive metadata; I did not author its
Lean mathematical proof bodies. This report continues my independent original
mathematical review and the separate complete-row and bridge reviews. It is
an AI-agent review under the repository's Tau Ceti adaptation, not an official
Tau Ceti endorsement or human peer review.

Disposition: approve the complete mathematical source at commit
`523c5aeaddd8bf7c2dc01afb053bb0dea8811335`. Final mechanical acceptance remains
pending the actual canonical Linux run `34783909558`. NR-03 remains uncounted.

## Complete original target and mathematical meaning

The canonical question asks whether the real matrix with every Boolean-vector
row and column and entries `(1 - dot(a,b))^2` has nonnegative rank `2^n` for
every `n >= 3`. Definitions retains all functions `Fin n -> Bool`; its dot
product and target subtraction are over the reals. The n = 7 width-127 witness
therefore refutes the full universal assertion. This is neither a selected
submatrix nor a claim of the exact rank at seven, and it makes no unnecessary
claim about a counterexample in every dimension. Intersections above one are
included without changing the target to natural truncated subtraction.

The definition of nonnegative rank is the least natural width of an ordinary
nonnegative real rectangular factorization when one exists. The accompanying
attained/minimal theorem gives both attainment and comparison with every
admissible width. The explicit witness supplies existence before this branch
is used, so the fallback value zero for matrices lacking a factorization is
irrelevant to the counterexample. No rank inequality is assumed as a premise.

I reread Definitions, Encoding, Core, FamilyDefs, Index, the final family
assembly, CertificateBridge, Certificate and Rank in the integrated graph.
The numerical obligations and independent Challenge are unchanged from the
two approved pre-proof statement boundaries. My source audit additionally
compared all ten literal theorem signatures to Challenge and their exact names
to Comparator and both LeanCert/axiom commands. This source comparison supports
statement correspondence but does not substitute for actual Comparator.

## Encoding and complete certificate proof

The recursive encoding is structurally bounded by `2^n` and has the requisite
bit theorem. Its seven-bit mask-to-vector left inverse transports the proved
all-mask identity to every public Boolean row and column. The guarded natural
square uses `(1-t)^2` for `t <= 1` and `(t-1)^2` otherwise. Its real-cast lemma
proves equality to the full real square using the corresponding subtraction
bounds. It therefore preserves t = 0, t = 1 and every t > 1 case.

The atom space has exactly 64 + 7 + 21 + 35 = 127 elements. The generic sum
splitter is proved for an arbitrary natural summand, and the eight W/V index
lemmas connect each disjoint block to its intended factor. The representative
and complement argument proves the core identity without enumerating the
entire rectangular product. The explicit arrays contain every two-set and
four-set of the seven positions exactly once; I independently rechecked this
against combinatorial enumeration in the fresh source audit.

Each remaining family has 128 separate literal-row theorems, universally
quantified over all 128 columns, using default-kernel `decide +kernel`. The
48 modules contain exactly eight rows each. The three 128-way assemblies use
each row from 0 through 127 exactly once. I independently checked the literal
row statements, indices, proof forms and assembly coverage in all 48 files,
not just a sample. This represents 49,152 family-entry obligations. The closed
family identity reduces to the 64 pairs of `Fin 8` with the implication
`t <= s`; the separately proved cardinality and intersection bounds discharge
that condition for all masks. The positive-part natural coefficients are
combinatorial helpers and do not replace the original real subtraction.

My earlier original-source review includes an independent exact integer check
of every mask pair and family formula. That audit remains supplementary
mathematical evidence, never a trusted Lean premise. The current row graph is
byte-identical to the fully reviewed development graph and to the source
whose complete row and family elaboration passed in run `34780136595`.

## Algebraic assembly and real rank bridge

The added CertificateBridge module isolates algebra without importing the
row computations. Its four sum equalities use pointwise multiplication
congruence and finite-sum congruence; three nested additions preserve the
exact original association and block order. The conditional component helper
substitutes precisely the four family identities and the final closed sum.
Certificate supplies every premise with the actual unconditional core, three
complete row families and closed identity. No conditional helper premise
survives into any final public export.

The cast bridge expands the full real matrix sum, uses `Nat.cast_mul` term by
term and `Nat.cast_sum` over the complete atom universe, casts the full natural
identity, then applies the target cast lemma. The generic denominator is one
when the column cardinality is at most one and otherwise the positive square
of cardinality minus one. Rank proves nonnegative factors, explicitly
establishes that the real denominator is nonzero, distributes division through
the complete finite product, and recovers the ordinary real factorization.
The width-127 witness gives rank at most 127, strictly less than 128, and the
last theorem contradicts the original universal target at the admissible
value seven. These arguments use the entire prescribed matrix.

The two bridge interfaces were independently approved before their bodies.
I also reviewed the exact seven-path implementation overlay and its pinned
Mathlib cast API. The conditional bridge-only run `34782819568` passed its
actual selected helpers, but neither that result nor the earlier full-row
result supplies final Certificate/Rank/Comparator acceptance.

## Source integrity, trust and remaining acceptance

`INPUT-HASHES.json` binds all 102 committed package files, independently
compared against immutable Git blobs. The complete active import closure is
acyclic and consists of precisely the 58 manifest modules; all are
byte-identical to their stated reviewed development sources. The frozen
Definitions, Challenge, Comparator configuration and toolchain files match
their recorded hashes. The complete non-self inventory also matches. No
Challenge, probe, supplementary CertificateData table or historical generator
is imported by Solution. Source scanning found no proof placeholder, custom
axiom, native evaluation or unsafe declaration in the active bodies.

All ten public exports request LeanCert kernel trust and axiom diagnostics.
Only `propext`, `Classical.choice` and `Quot.sound` are permitted. The eventual
actual transitive checks and default-kernel export replay, sandbox controls,
negative controls and fresh source/pin logs are essential remaining evidence;
a source scan, partial compilation or green job alone cannot establish them.
No local Lean/Lake compilation or dependency cache operation was performed.

The proof uses exact structural reductions, small integer certificates and
literal-row splitting, so no numerical interval enclosure is necessary.
Schiffer and Forsythe are accurately cited as structural examples, without
imported mathematical assumptions. Formalization metadata uses the pinned
v0.4 schema. George Stepaniants receives formalization credit with Department
of Computing and Mathematical Sciences, California Institute of Technology,
Pasadena, California, USA, without an email. Sidney Holden's mathematical
resolution and Matthew J. Colbrook's historical partial result remain credited.

No source issue remains open in this review. After the canonical run actually
finishes, an immutable mechanical addendum must bind the successful raw logs
and inputs to this exact source and confirm every required gate. Publication
and the count increase require that addendum and the other independent final
referee's acceptance.
