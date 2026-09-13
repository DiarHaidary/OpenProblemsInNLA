# IE-05 Witness handoff

The scoped implementation is complete. The two exact frozen contracts are
`NLA.IE05._proved.canonical_integer_identification` and
`NLA.IE05._proved.witness_orthogonal_path`.

Stable `NLA/IE05/Witness.lean` SHA256:
`4fa2cfeef00d80f28475bf221082a786f2b035f1e77e47b1bfd70bc13f2e57b6`.

Useful integration interfaces in the same namespace are
`real_factor_certificates`, `normalizedInteger_orthogonal`,
`normalizedInteger_path_trajectory`, `normalizedInteger_trajectory_entry`,
`normalizedInteger_firstGrowth` and `integerLower_false_prescribed`.
The scalar-entry theorem covers every `k ≤ 8`, including the terminal stage,
for both Boolean data sets. The true canonical QR identification uses the
proved generic QR uniqueness bridge; it adds no numerical QR table.

The final fresh nine-command source run passed in 43.11 seconds with zero
warnings, 60 explicit kernel/standard-three reports, two exact frozen-type
matches, 93 actual project declarations and 56 retained dependencies.
All 733 frozen inputs, 27 original source/Git blobs, ten clean source pins,
six imported helper hashes and four complete prior evidence inventories
were rechecked. Development object reuse and both prefix cleanups are
recorded honestly; the final run reused no project objects.

Read [COMPLETION.md](COMPLETION.md), [HANDOFF.json](HANDOFF.json),
[audit-result.json](audit-result.json) and the immutable final
[attempt result](attempt-wo2xjo06/result.json).
The final result SHA256 is
`e3cd33e82f3fa937d2afadc347f117a3668d8681c0fb842a85ff947a32178241`.

Read-only reproduction of the scoped preservation check, from the project:

```
python3 verification/witness-development/verify_seal.py
```

This is author validation on macOS, not independent final review or actual
Linux Comparator verification. The source author also contributed statements
and earlier proof helpers. No source status, ID, metadata, Git or publication
change is included. Concurrent GrowthBounds/Growth files are outside this seal.
