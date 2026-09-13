# Retained independent-review diagnostics

These are reviewer tooling diagnostics, not mathematical defects in the draft.
No original statement, definition, author evidence file, dependency, or metadata
was changed to address them.

1. The initial read-only inventory probe assumed `files` was a list. It is a
   mapping, so slicing raised `KeyError`. Its exact code/output and corrected
   read are retained in `initial-probes.py` and `initial-probes-transcript.txt`.
   All original 168 bytes/file identities and exact membership were subsequently
   checked before creating the reviewer directory; see `baseline.json`.
2. A later read-only probe expected the historical directory named
   `api-evidence-final` to be successful. Its manifest is explicitly a retained
   failed author attempt with zero files, and `next` raised `StopIteration`.
   The actual successful author API capture is `api-evidence-complete`; it is
   independently checked in the input audit. Both original manifests remain.
3. `attempt-7tjmj3b0` compiled fresh Definitions and Challenge, then my inspector
   requested the unbuilt umbrella `LeanCert.olean`. Lean exited 1 with an actual
   missing-object diagnostic. The runner and inspector source, all 58 child
   commands, logs, two object hashes and exact removal receipt are retained.
   Only my inspector import changed to the actual pinned, available
   `LeanCert.Tactic.Verification`. No dependency object was copied or built.
4. `attempt-5t4u9ww4` completed all four modules and inspections. Its fully
   explicit logs were verbose, so `attempt-nglj5yvu` repeated the same original
   inputs in another empty prefix and added readable prints of those same
   elaborated declarations. Both complete successful receipts remain; no failed
   statement or definition was repaired. Each used 79 child commands and
   hashed/removed only its own four objects.
5. The first independent provenance audit (`input-audit`) assumed the archived
   Tau Ceti tree response's outer `sha` was the root tree hash. The response
   actually echoes its requested commit `afb424...`; the commit's tree is
   `239214...`. The failed assertion and original executed script remain.
   The corrected audit requires that observed commit identity, independently
   reconstructs every one of the seven Git trees from all entries, and checks
   the reconstructed root against the commit's actual tree field. It does not
   substitute the response label for a tree computation.
6. `input-audit-_jmvo_yj` then assumed identical `rg` byte ordering. Parallel
   file result groups arrived in a different order, with identical complete
   lines. Both exact outputs remain. The corrected check compares sorted lists
   of complete lines, preserving duplicate counts, while separately checking
   the source/Git identities and preserving both raw byte hashes.
7. `input-audit-w00yn2fr` compared complete author preflight and postflight
   dictionaries. Those records have different timing fields and preflight-only
   build/expected-revision annotations. The corrected check validates all ten
   package names, exact revisions, command arguments, command exit codes,
   empty clean-status outputs, corresponding working directories, and the
   explicitly recorded nine build-directory choices. Original dictionaries are
   retained unchanged. The final audit succeeds; its exact directory/result
   identity appears in `RESULT.json`.
8. The first output-summary parser expected single quotes around the word
   `sorry`. The actual pinned Lean warnings use backticks. The failed parser
   source and tool transcript are retained in `output-validation-initial`;
   correcting that exact string permitted the already successful raw
   compilation logs to be parsed. No compiler command or original source was
   rerun or changed for this correction.

The author's earlier overwritten elaboration JSON is a separate preexisting
incident documented in `verification/EVIDENCE-RECOVERY.md`. Its original final
JSON and exact old object/postflight records are lost; no recovery is claimed.
The independent review uses the author's fresh intact attempt only as audited
historical evidence, and relies on its own new executions for elaboration.
