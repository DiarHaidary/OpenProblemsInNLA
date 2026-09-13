# KE-04 Frames helper handoff

Complete scoped implementation in `NLA/KE04/Frames.lean`, SHA256
`bfea6b02091db4e999c2c870b4b1f238cb546ad84df010c7d5431fe82904db0b`.

The five exact frozen exports under `NLA.KE04._proved` are
`real_matrix_semantics`, `krylovBasis_exists`, `frameProjection_semantics`,
`compression_semantics`, and `compressedQuadratic_semantics`.
All actual types match; zero dimensions and arbitrary independently chosen frames
remain included. The lifted quadratic is exactly `Q*q(QᵀAQ)*Qᵀ`.

Reusable interfaces include `act_mul`, `act_one`, `inner_act_transpose`,
`inner_act_left`, `frame_iff_orthonormal`, `columnSpace_eq_range_act`,
`act_transpose_act`, `frameProjection_act`, `frameProjection_fixed_iff`, and
`submodule_frame_exists`. Frames imports only Definitions from this project,
so it can be consumed by Krylov/Spectral/assembly without a project import cycle.

Final fresh three-command run: 21.36 seconds, five exact type matches,
27 kernel/standard-three reports, 38 actual project declarations and 34 retained
dependencies. Mathematical sources have zero warnings; four unused-binder warnings
in literal expected Prop definitions are retained and explained in the report.
All 1598 frozen inputs, seventeen original Git sources and ten clean pins remain
unchanged. All three attempts and owned-object cleanup records are preserved.

Read [the author completion report](../../reviews/frames-development.md),
[HANDOFF.json](HANDOFF.json), [audit-result.json](audit-result.json), and
[the final source run](attempt-_2m2tvtu/result.json).
For a read-only integrity check from the project root:

```
python3 verification/frames-development/verify_seal.py
```

This is local macOS author validation, not independent final review or actual Linux
Comparator verification. Concurrent proof sources, whole-proof completion,
metadata, canonical status, Git and publication are outside this helper seal.
