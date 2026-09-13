# NR-03 minimal private cast repair

This is an implementation patch for the actual canonical compiler error at
`NLA/NR03/Rank.lean:40:4`, reported by run 34783909558 at commit
`523c5aeaddd8bf7c2dc01afb053bb0dea8811335`. The raw failure receipt is retained
at `/tmp/nla-nr03-canonical-linux`; this patch is not a compiler or referee
acceptance result. No live worktree file, branch, workflow, or status changed.

The sole edit inserts one tactic immediately before the failing cast step:

```lean
change (0 : ℝ) ≤ (W i k : ℝ)
```

The existing `castNatMatrix` definition is exactly
`fun i j => (M i j : ℝ)`. Thus the exposed goal is definitionally the original
entrywise real nonnegativity obligation, with no weakening, changed index,
new premise, or altered definition. The original
`exact_mod_cast (Nat.zero_le (W i k))` then sees the explicit natural-to-real
cast instead of an unapplied simplifier rule for the matrix wrapper.

All other source bytes are unchanged. In particular all ten theorem
signatures, all remaining proof bodies, imports, settings, and the approved
Definitions/Challenge/public boundary remain unchanged. The patch adds no
new module or statement. Removing the single inserted line exactly recovers
the original Rank.lean bytes.

Adjacent steps were inspected against the pinned source without executing
Lean/Lake. The next branch applies `div_nonneg` to `scaledRightFactor`, whose
definition is explicitly `(V k j : ℝ) / (d j : ℝ)`; its resulting two goals
already expose the casts. The denominator nonzero obligation is explicitly
`(d j : ℝ) ≠ 0`. The sum/division bridge unfolds the matrix wrappers with
`simp only`, distributes the external scalar using `Finset.sum_mul`, and
finishes by real ring algebra. These are source observations, not a claim
that later tactics executed after the reported failure.

Pinned API references (Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`):

- `Mathlib/Data/Nat/Cast/Order/Ring.lean:30` states natural casts are nonnegative.
- `Mathlib/Algebra/Order/GroupWithZero/Basic.lean:883` states `div_nonneg` with
  explicit nonnegative numerator and denominator premises.
- `Mathlib/Algebra/BigOperators/Ring/Finset.lean:56` distributes multiplication
  through a finite sum in the orientation used by the unchanged bridge.

The patch is private and uncompiled. Two independent source-delta reviews
and subsequent actual canonical verification remain required. No local
compiler/cache, new run, raised cap, commit, or push was performed here.
