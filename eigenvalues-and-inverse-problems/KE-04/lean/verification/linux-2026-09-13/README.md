# KE-04: authoritative Ubuntu verification

The complete 24-export KE-04 proof passed the actual non-root Ubuntu harness at
revision `40b0bf52e73e776e7769f0f12dbbda7cd9fff183`:
[workflow 34759746409, target job 103730400358](https://github.com/sgstepaniants/OpenProblemsInNLA/actions/runs/34759746409/job/103730400358).
The [independent operational review](independent-audit/final-verdict.md) by
OpenAI Codex agent `/root/lean_iv01_next` accepted the exact target result.
The reviewer contributed no KE-04 implementation. This is an AI-agent audit,
not external human peer review.

The original `lean-KE-04` artifact (ID `10318925539`) has SHA-256
`c48f544782d0d051396bb7ccca11808ea546a5254f314175dfd8e92a9c5bb591`.
Its [ZIP](independent-audit/lean-KE-04.zip), [API metadata](independent-audit/artifact-metadata.json),
and [extracted logs](independent-audit/linux-artifact/) are retained. The
[verification result](independent-audit/linux-artifact/verify-20260913T132545Z-4211/result.json)
binds exactly 4,250 committed candidate inputs and all 24 configured declarations.

The [Comparator log](independent-audit/linux-artifact/verify-20260913T132545Z-4211/comparator.log)
records separate Challenge and Solution builds, all exports, permitted-axiom
checks and successful default-kernel acceptance. Only `propext`,
`Classical.choice`, and `Quot.sound` are permitted. The actual sandbox,
kernel-replay, Comparator-regression, `sorryAx` and native-decision rejection
controls are retained alongside it. Lean is 4.33.1, and the pinned Mathlib cache
was used; this is not a claim that every dependency was rebuilt from source.

The aggregate workflow failed because an unrelated IE-23 job failed. The
KE-04 target job and its controls succeeded. No unrelated job result is used
as evidence for this problem.

The independent [evidence manifest](independent-audit/EVIDENCE-MANIFEST.json)
has SHA-256 `70a8b0304388917247db9c75ec7f1db69a18b2306c187f5877f8352eeeed175c`
and binds all 32 audit files, including the final report and raw run/job receipts.
Its sole self-exclusion is the exact manifest path. Verify the archive without
network access or Lean execution:

```sh
python3 independent-audit/verify_evidence.py
```

The mathematical proof freeze and both independent final mathematical review
seals remain separately checked by `../packaging/verify.py`. That checker maps
only the two explicitly archived historical wrappers, README and Lakefile;
all reviewed mathematical files stay at their original paths and hashes.
Later publication metadata and rendered documents do not change the verified
mathematics. The audit checks the committed source lock and runtime tool receipt;
it does not claim a new independent audit of every upstream harness source.
