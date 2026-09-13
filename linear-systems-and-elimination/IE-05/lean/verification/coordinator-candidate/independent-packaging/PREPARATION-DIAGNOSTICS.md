# Preparation diagnostics retained

The independent reviewer made two unsuccessful read-only exploratory requests
while the candidate author was still preparing its final handoff. Neither path
was promised by the candidate and neither diagnostic is a package rejection.

- `cat /tmp/nla-lean-formalization/ie05-candidate-package/lean/verification/candidate-package/schema/README.md`
  returned exit 1 and `No such file or directory`. The actual small schema source
  identities are in `schema/SOURCE-RECORDS.json`, which was then read in full.
- An `rg -n` search included the nonexistent guessed path
  `verification/reference-lock.json` and returned exit 2 with `(os error 2)`;
  it also returned matches from the existing NOTICE and packaging files. Actual
  reference source paths are retained in the historical inventories and the
  27-source `verification/original-source-inventory.json`. No file was created
  to make either guessed path exist.

Before its first execution, the independent audit was adjusted for the observed
Python 3.10.13 schema environment, which has PyYAML and jsonschema but neither
tomllib nor tomli. Its Lake-file check instead requires the exact accepted old
bytes with only `defaultTargets = ["Challenge"]` changed to `Solution`, alongside
the actual shared harness's static input validation. This avoids any unsupported
TOML parser assumption. No failed independent proof or package-audit execution
is concealed by this preparation adjustment; the main audit had not yet run.
