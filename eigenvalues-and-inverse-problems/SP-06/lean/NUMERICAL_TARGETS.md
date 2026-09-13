# SP-06: complete target and numerical obligations

Statement-stage draft, 13 September 2026. No proof implementation is authorized
until the complete boundary is typechecked and two independent statement
referees approve it. Canonical source base:
`50838e37dd793830e2cecd1055cfc7e0349490f1`.

The original target quantifies over every finite complex Laurent polynomial
with nonzero extreme coefficients at exponents `-r` and `s`, where `r,s ≥ 1`.
It asks whether existence of a continuous injective image of the unit circle
avoiding zero, on which the symbol is real, forces every finite Toeplitz section
to have real spectrum. Toeplitz entry `(i,j)` uses exponent `i-j`. The formal
target must retain arbitrary complex coefficients and every positive section
size. Spectrum must be the actual complex spectrum of the matrix algebra.

The negative resolution uses the exact symbol

```text
b(z) = -64 z^(-2) + 8 z^(-1) - 128 - 8 z
       - 63 z^2 - 16 z^3 - z^4.
```

Its band is `[-2,4]`, with both extreme coefficients nonzero. Put
`a(z)=8/z + 8z + z^2`. For every nonzero complex `z`, the proof must establish
`b(z)=a(z)-a(z)^2` for the actual finite Laurent evaluation, with all seven
coefficients checked.

To construct the entire Jordan curve, use the actual unit circle `Circle` in
the complex plane. For its point `u`, write `c=Re(u) ∈ [-1,1]`. Set

```text
F(r,c) = r^2 - 1 + (r^3/4)c.
```

The exact real obligations, on the complete indicated intervals, are:

1. For `-1 ≤ c ≤ 1`, `F(1/2,c) ≤ -23/32 < 0` and `F(2,c) ≥ 1 > 0`.
2. For `1/2 ≤ s ≤ r ≤ 2` and `-1 ≤ c ≤ 1`,
   `(r-s)/4 ≤ F(r,c)-F(s,c)`. This replaces a derivative/interval computation
   by an exact polynomial inequality on one fixed box.
3. For each `c ∈ [-1,1]`, there is exactly one `r ∈ (1/2,2)` with `F(r,c)=0`.
4. If `r,s ∈ (1/2,2)` are roots at `c,d ∈ [-1,1]`, respectively, then
   `|r-s| ≤ 8|c-d|`. The uniform separation in item 2 and the coefficient
   bound `s^3/4 ≤ 2` imply this estimate.
5. There exists an actual continuous radius `ρ : Circle → ℝ` with
   `1/2 < ρ(u) < 2` and `F(ρ(u),Re(u))=0` at every circle point.
   Existence or continuity must not be assumed in the final theorem.
6. The map `γ(u)=ρ(u)u` is continuous, injective and nonzero everywhere.
   For every such point its auxiliary symbol has imaginary part zero. Thus
   the actual Laurent symbol is real on the whole curve. No samples, finite
   mesh, limiting curve or weaker notion of Jordan curve can replace this.
7. The actual order-two Toeplitz section is
   `[[-128,8],[-8,-128]]`. Its genuine spectrum contains `-128+8i`, whose
   imaginary part is exactly `8`, and therefore is not entirely real.
8. Combine the valid band, entire real Jordan curve and nonreal finite-section
   spectrum to prove the negation of the complete original universal target.

The source additionally describes enclosure of zero. The canonical question
requires only a Jordan curve avoiding zero, so enclosure is not an additional
claim of this formalization. The continuous positive radial construction is
retained; no regularity is imposed as an extra premise of the universal target.

The method minimizes computation by replacing trigonometric parameterization
with the unit-circle coordinate and a single scalar root equation. Exact
algebra and the Lipschitz estimate remove an implicit-function theorem and
all curve subdivisions. LeanCert must use kernel trust for any retained
numerical certificates; the final exports also receive explicit kernel-trust
and transitive permitted-axiom checks. Standard Mathlib continuity and the
intermediate value theorem may be used; no unproved analytic input is allowed.

Original mathematical proof: Matthew J. Colbrook, Department of Applied
Mathematics and Theoretical Physics, University of Cambridge. Formalization:
George Stepaniants, Department of Computing and Mathematical Sciences,
California Institute of Technology, Pasadena, California, USA. Substantial
AI assistance is disclosed; no email is added for George Stepaniants.
