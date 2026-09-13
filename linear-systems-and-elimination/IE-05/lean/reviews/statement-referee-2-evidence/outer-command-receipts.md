These are receipts for the outer script invocations visible in the tool
transcript; the nested actual subprocess commands and raw outputs are retained
in `commands.jsonl` and `logs/`. The source display reads were repeated with
full raw capture in `final_check.py`. The 103 original handed-off files are
also retained as byte-for-byte snapshots.

```
python3 reviews/statement-referee-2-evidence/audit.py
exit 0
PASS: 103 complete draft inputs and 27 immutable original Git/source bindings verified and snapshotted.

python3 -B reviews/statement-referee-2-evidence/numerical_reconstruction.py
exit 0
PASS: independently parsed canonical and Lean arrays, exact Gram/LU and all pivot ties; 64+204 reduced bounds; gap 117335164/1147041. Python diagnostic only.

python3 -B reviews/statement-referee-2-evidence/elaborate.py
first invocation: exit 1 in the outer Python warning-format post-check
All three Lean subprocesses: exit 0
Complete copied terminal exception: attempt-1-terminal.log
Actual first script snapshot: attempt-1-elaborate.py
First result: elaboration-result.json

python3 -B reviews/statement-referee-2-evidence/elaborate.py
second invocation, corrected warning parser: exit 0
PASS: fresh Definitions, 17-placeholder Challenge and all 41 local definition trust checks; own objects hashed then removed.
Second result: elaboration-result-2.json
```

An early display-only `cat reviews/statement-referee-2-evidence/elaboration-result.json`
ran while the first elaboration process was still active and reported that the
result did not yet exist. It was a read-only status probe, not a Lean or
mathematical failure. Both eventual results and every own object hash/cleanup
receipt are retained. No source correction or mathematical proof was attempted.
