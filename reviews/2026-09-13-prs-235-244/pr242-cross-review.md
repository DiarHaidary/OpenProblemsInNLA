# PR #242: independent bounded mathematical cross-check

**PASS. No actionable mathematical blocker found in the assigned sections.**

Reviewed head: `2617484a85db56dbbcf3531e35eb3231144d2c8d`.

Source inspected: `/private/tmp/nla-audit-242/references/holden-mi05-2026-09-13/report.tex`, especially lines 250–435, with definitions and the fourteen-term feature-span argument at lines 41–167. The coordinating reviewer owns the full report audit, exact-arithmetic suite and PDF inspection. I did not rerun code, rebuild a PDF, or mutate repository source.

## Maximizing-permutation criterion, lines 250–274

The argument correctly uses a linear map on the whole feature span, rather than requiring the augmented feature vector to come from another unitary. Every entry of the fourteen-term coefficient table is linear in the feature coordinates. The normalization coordinate is among the coordinates checked in the basis proof, so the sum of reconstructed coefficients tracks arbitrary total mass.

Let F be the current unitary feature vector, Pκ the permutation feature vector, and f the positive-branch obstruction function. The fixed expectation is f(F)=−2τ. With a=2τ/f(κ)>0, one has f(F+aPκ)=0. Thus h'=−f(F+aPκ)/2=0 in the appropriate relabeled/transposed table. All entry and squared-minor coordinates of F+aPκ are nonnegative; when h'=0 every reconstructed coefficient is such a coordinate or zero. Their sum is 1+a. Their support lies in f=0, disjoint from κ because f(κ)>0. Subtracting aPκ therefore gives precisely a negative coefficient −a at κ and nonnegative coefficients of total mass 1+a elsewhere. Applying the support functional gives (1+a)M−aM=M, even if M itself is negative. The claim only requires one maximizing permutation with positive f; it does not falsely exclude directions whose maximizing permutations all have f=0.

## Quaternion coverage, lines 312–334

The displayed matrices are left/right quaternion multiplication in a fixed coordinate convention, so their actions commute. They are real orthogonal for unit quaternions and have determinant +1 by continuity from the identity. The map from the two unit-quaternion factors has six-dimensional domain and a differential of rank six: a kernel pair of imaginary infinitesimals a,b satisfies ax+xb=0 for every quaternion x (with harmless sign changes under the displayed convention). Setting x=1 gives b=−a; consequently a commutes with every quaternion. The quaternion center is real, and a is imaginary, so a=b=0. The image is a subgroup containing a neighborhood of the identity, hence open; compactness makes it closed. Connectedness of SO(4), obtainable from plane rotations as stated, gives surjectivity. A row-sign change preserves every squared minor and every diagonal-entry square while correcting determinant −1. Thus the restriction to the quaternion parameterization does not omit a component of O(4). Column reordering also remains in O(4), so the bound covers every branch.

## Two-simplex stationary argument, lines 336–391

The constrained derivatives are α/pᵢ−sᵢ=λ and β/sᵢ−pᵢ=μ, where α=√∏pᵢ and β=√∏sᵢ. Multiplication by the coordinates and summation gives λ=4α−p·s, μ=4β−p·s, Φ=(λ+μ)/2 and λ(pᵢ−1/4)=μ(sᵢ−1/4).

The case split is complete. If one multiplier is zero and the other is nonzero, the centered-vector identity makes one vector uniform, and its stationary equation makes the other uniform; both multipliers must then be zero. If both are nonpositive, Φ≤0. If both are positive, the centered vectors are positively proportional, so p·s≥1/4, whereas AM–GM gives 4α≤1/4, contradicting λ>0. Uniform vectors also have Φ=0.

The only remaining case relevant to a positive stationary value has k=λ/μ<0. Substitution gives the displayed quadratic for each pᵢ, so a nonuniform p has exactly two positive values a,b, with multiplicities m and 4−m; s has corresponding values c,d. Their root products give

`k=−(a/b)^((m−2)/2)` and `1/k=−(c/d)^((m−2)/2)`.

For m=2, k=−1 gives λ+μ=0. For m=1 or 3, multiplying the relations yields ac=bd. Put v=a/b. Normalization yields b=1/(mv+4−m), c=1/(m+(4−m)v), and k=−(mv+4−m)/(m+(4−m)v). Substituting u=√v into either remaining equation indeed gives (u−1)³=0. This contradicts the two distinct values. No positive interior stationary point remains.

Φ is continuous on the compact product of simplices. The exhibited boundary pair has value 128/2401−49/2401=79/2401>0. Hence a global maximizer lies on the boundary. If p has a zero coordinate, its product term vanishes and p·s≥min sᵢ; equality is attained by choosing p as a vertex at a minimizing coordinate. If instead only s is on the boundary, symmetry gives the same reduction. This establishes the claimed global maximum, not merely a local stationary bound.

## Sharp one-variable bound, lines 393–436

For x=min sᵢ∈[0,1/4], AM–GM bounds the other-coordinate product by ((1−x)/3)³; equality respects the minimum restriction because (1−x)/3≥x. The derivative formula is correct. On the open interval 1−4x is positive, so squaring its critical equation introduces no extra sign branch. The resulting polynomial g(x)=16x³−24x²+36x−1 is strictly increasing, with opposite signs at 0 and 1/4. The derivative of h₀ changes from positive to negative at the unique root, giving the global maximum. The stated expression τ=x(1+2x)/(1−4x) follows directly from the unsquared critical equation.

With one quaternion factor equal to (1,0,0,0) and the other having positive coordinates with squared values x*,(1−x*)/3 repeated three times, the triangle bound is equality and h=2√(x*(1−x*)³/27)−x*=τ*>0. The upper bound is therefore attained. The resultant and decimal bracket are exact-algebra subclaims covered by the coordinating reviewer's suite; this bounded review did not independently recompute them.

The conclusions remain explicitly about obstruction values and optimal signed common weights. The report does not promote them to a positive hull distance or a full solution of MI-05.
