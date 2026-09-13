# KE-04 Krylov implementation checkpoint

Status: **in progress**, temporarily checkpointed at the coordinator's request
while agent capacity is used for independent final review of IE-05. This is not
an independent mathematical review or a completed proof handoff.

`/root/mf16_final_referee` owns `NLA/KE04/Krylov.lean`,
`verification/krylov-development/`, and this note. The agent is now a KE-04 proof
contributor and cannot count as an independent final KE-04 proof referee.

All five requested frozen contracts have implementations drafted under
`NLA.KE04._proved`, using the actual span, finite rank, independent-column,
coefficient-map and Nat.findGreatest APIs. The first fresh build passed
Definitions, then stopped on elaboration errors in the rank and prefix bridges.
The source also contains fourteen explicit LeanCert kernel trust assertions;
failed-proof recovery propagated sorryAx to dependent assertions, and none of
those is accepted evidence. The seven independent early/helper declarations
reported only standard foundational axioms, but the whole module has not passed.

The immutable attempt is `verification/krylov-development/attempt-z68t67pr`.
Its complete input copies, exact commands, all raw outputs, ten dependency source
pins and clean statuses before/after, and one removed Definitions object hash
are retained. The private output directory is removed; no process remains live.
No dependency cache was copied, downloaded, rebuilt or mutated. All 1,598 frozen
statement inputs are unchanged. `CHECKPOINT.json` records exact hashes and the
specific next edits; the failed attempt must remain intact.

The next work is to replace several elaboration-sensitive simpa arguments by
explicit equality rewrites of the same frozen objects, disambiguate one pair
projection, recompile, and perform the final exact-type and actual dependency
inspection. No statement, Solution, publication metadata, Git state or canonical
status has been changed.
