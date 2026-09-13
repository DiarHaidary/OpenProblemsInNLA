# Preserved IE-16 statement boundary

This directory preserves the exact pre-attainment-contract statement source
used by the first statement referee. It is retained for audit and is not
imported by the current package.

* `old-source/Definitions.lean` SHA-256:
  `7f232bb361e6e81db9460b88dc6ed2b990c8148d29d5f0a4fe92be7127ec57b9`
* `old-source/Challenge.lean` SHA-256:
  `5dd745c5d0ba7f1aa7652bdc163ca8d686b5d548b94c9d28b0cfbeaf5f73b590`
* prior `verification/STATEMENT_HASHES.json` SHA-256:
  `355a1a1c416f0f8979793017986cb432969bf200e45ac38545b2882072dee405`
* preserved manifest `verification/prior-statement-boundary-20260913.json` SHA-256:
  `30069a39510f32d9049d6509d66f47c269b2454ac610cc57f441cde4c19ff822`

The prior review state was `statement-stage-pending-two-independent-reviews`
with no reviewers recorded and no proof, Linux, or Comparator claim. The
current boundary adds explicit `IsLeast` contracts for the full and subset
infima and strict positivity of the subset maximum.
