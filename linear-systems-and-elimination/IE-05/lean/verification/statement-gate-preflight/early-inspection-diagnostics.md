Before the portable preflight script was created, two display-only inspection
commands reported the following diagnostics. These are retained transparently;
they were not failed Lean or mathematical checks.

1. `rg --files reviews/statement-referee-1-evidence verification/statement-gate-preflight`
   exited 2 because the new preflight output directory did not yet exist. The
   referee evidence listing was returned. The directory was subsequently
   created within the coordinator's authorized write scope.
2. A read-only Python schema-display helper inspected the original
   `tools/lean/source-lock.json` and attempted
   `list(x['files'].items())[:2]`. Its `files` value is a list, so it exited 1:

   ```
   Traceback (most recent call last):
     File "<stdin>", line 11, in <module>
   AttributeError: 'list' object has no attribute 'items'
   ```

   The next display read used `x['files'][:2]` and confirmed the real schema.
   The portable verifier checks that list's 58 entries correctly. No input was
   written by either display helper.

The later, substantive first preflight failure is retained in full in
`attempt-1.stdout.json` (including its actual traceback),
`attempt-1.stderr.log`, `attempt-1-command.json`, and
`attempt-1-verifier.py`. Its actual command ran all 85 read-only subprocesses
with exit zero before encountering its own SHA-only-record schema mismatch.
