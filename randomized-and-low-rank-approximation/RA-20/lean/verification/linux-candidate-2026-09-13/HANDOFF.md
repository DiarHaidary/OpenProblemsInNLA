# RA-20 candidate-document installation handoff

**Author checks passed; independent packaging review is pending.** This record
hands the installed candidate to a different agent. It does not approve its
own packaging, repeat a mathematical approval, claim a Linux result, or change
canonical status. Canonical RA-20 remains **Solved**.

Document preparer: `/root/ra20_final_referee1`, previously independent final
mathematical referee 1 and subsequently the author of these candidate documents.
George Stepaniants is the formalization author, Department of Computing and
Mathematical Sciences, California Institute of Technology, Pasadena, California,
USA, with AI assistance. The original negative-resolution mathematics remains
attributed to the Codex automated maintainer audit, and the original conjecture
to Kubjas, Sodomaco and Tsigaridas. No personal email is published here.

## Fixed candidate bytes and accepted gate

| File, relative to the Lean project | SHA-256 |
| --- | --- |
| `README.md` | `83e19faf1bf25a9748de40da3193cfd68690100923a50379553e288c45b5e8bc` |
| `formalization.yaml` | `bec9d851e204464fa2d3e29033d5958034665d51c3554d2043f1470bfafd4197` |
| `verification/pre-candidate-README.md` | `7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50` |
| `verification/final-review-acceptance.json` | `a1c7ffebd2c0db8159b9861adf3663051b8e03346b776393553773d97e0abbbb` |

The original source base is `5830ed4fb06da0659414a3deb2a40ad327aca052`.
There is **no candidate commit, push, pull request, or RA-20 Linux run asserted
by this installation**. The root accepted both complete independent mathematical
reviews before the documents were authored. The separate packaging reviewer
must inspect these concrete bytes before a candidate commit and Linux run.

The initial [installation receipt](installation.json) has SHA-256
`4ebd760e4d36633039f1fd42f9d3bd3755b9f5696b15391bb18c1ed3e35f39e9`.
Its initial pending-author-check status is superseded by the actual subsequent
[author check results](CHECKS.json), SHA-256
`d1aebfbe7e4c7d6fff464225b123229399b5279b1a4d55f2c84674492fb8a45e`.
The [preinstallation gate and complete baseline](preflight.json), SHA-256
`a6540a7a937fc0298954cf5b508f0354881fec87e832f80f223773c6f9cd0210`,
was captured before this installation introduced any project file.

## Complete preservation and the only historical mapping

The baseline contains **958 project files**. Of those, 957 remain byte-for-byte
unchanged at their original paths. The only replaced prior file is `README.md`;
its exact prior bytes remain in `verification/pre-candidate-README.md`.
The YAML, that archive, and this installation-evidence directory are new.
No Lean source, pin, mathematical target, proof map, historical evidence, Git
metadata, or canonical problem status was edited in this task.

Historical manifests must use exactly this rule:

> Only a path resolving to the project `README.md`, when its expected SHA-256
> is `7eb951780e58ce518f0a400c90297020e7c6909ad9fd0c9c15b8036761a8bb50`,
> resolves instead to `verification/pre-candidate-README.md` for checking.
> Every other path and expected hash is checked unchanged.

This is not a blanket exemption for README files or stale hashes. It preserves
all 521 proof-freeze inputs, all 68 statement-freeze inputs, all 16 original
source files and their retained snapshots/Git blob identities, and both **full**
final-review inventories, containing 699 and 793 entries. The author check
also rehashed all **14** historical nested manifest/package inventories: the
13 `EVIDENCE-MANIFEST.json` files and the separate statement package manifest.
The statement freeze is checked separately from those 14 inventories.

The final [complete inventory](EVIDENCE-MANIFEST.json) binds every prior project
file through its preserved version, the installed wrappers and exact archive,
all installation evidence, all nested manifests, the live original source
inputs and the actual schema/ID validator scripts. Only this exact newly
created outer manifest excludes itself. It does not broadly exclude files
named `EVIDENCE-MANIFEST.json`. Later additions by a different reviewer outside
this evidence directory are not falsely presented as part of this author's seal.

## Checks actually performed

The retained command/result/log triples show the real repository v0.4 schema
validator passed for all twelve advertised Comparator exports, with no
replaceable definitions, and both permanent-ID checks passed against
`origin/main` and `nla-upstream/main`. The checks also confirm the unchanged
canonical Solved status, all exact pins and accepted gate, all twelve ordered
main-result/alignment entries, and the explicit local command
`lake build Solution`; the historical default target is Challenge.

[Publication hygiene results](HYGIENE.json) record relative-link and metadata
path checks, original immutable Git source links, and the email/whitespace
check of new publication material. External URL syntax is checked; this
installation does not claim a live HTTP probe of every external website.
The earlier failed attempt to read `tools/lean/validate.py` is retained in
[the read diagnostic](preflight-read-diagnostic.json); the actual existing
`tools/lean/validate_manifest.py` was located, read, and run successfully.

The candidate-document task performed **no Lean build**, dependency download,
cache copy or mutation. It adds no interval computations. The accepted fresh
mathematical reviews supply the actual twelve-export proof and LeanCert
standard-three kernel-trust evidence. Both historical review roles and this
later document-author role are explicit in the installed metadata.

## Read-only seal verification and next gate

From this directory, run:

```
PYTHONDONTWRITEBYTECODE=1 python3 verify_inventory.py
```

The verifier uses only Python's standard library and read-only Git access.
It checks the complete inventory, every preserved baseline entry, all nested
historical inventories under the one exact archive rule, both freezes, the
sixteen original snapshots and base Git blobs, candidate hashes, and recorded
author-check outcomes. [Preseal validation](VALIDATION.json) is itself bound
by the seal. The final sealed verifier was then run without adding or rewriting
any file in the sealed evidence directory; its printed receipt is supplied to
the coordinator and independent packaging reviewer.

Historical scripts are retained as evidence of their original execution.
Do not rerun the one-shot installer or preinstallation gate on the installed
candidate, and do not rerun `check_installation.py` into this sealed directory.
For later validation, use the read-only verifier above and put any new audit
logs in the later reviewer's separate evidence directory.

After independent packaging acceptance, the coordinator must create the clean
immutable candidate and run the actual non-root Ubuntu bootstrap, full control
suite, standalone default kernel and real Comparator described in the installed
README. Independent operational acceptance and reviewed canonical publication
are still required. No `Lean verified` status is authorized by this author
handoff alone.
