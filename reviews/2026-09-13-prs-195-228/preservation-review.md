# PRs 195–228 independent preservation review — PASS

Published integration base: `2db1e5857a4813ca627b60b4e30fa9bf6258c1cc`; all 25 reviewed source heads branch from `5830ed4fb06da0659414a3deb2a40ad327aca052`.

Checked 8,861 previous-main tracked paths, all 217 permanent IDs and canonical paths, 22 changed canonical targets, and 7,044 authored reference/code/evidence paths. All original target blocks are byte-identical in their respective source heads. 86 shared tools/workflows/schema/test/config paths are protected unchanged.

The only shared source modification is tools/render_problems.py. Independent diff review restricts its final content to the exact union of four source layout patches: add MI-27 to the reference-page-break set; remove TR-08, RA-17 and RE-03 from that set; add RE-03 to the Context-and-notation page-break set. The separately reviewed maintainer adjustment also removes RA-04 from the reference-page-break set after combining its histories, keeping its contextual text and references on page two. No other renderer byte and no Lean or permanent-ID safeguard may change.

Authored archives and verification records: 5,127 paths; manifest-named authored files: 173. Complete repository-relative paths are checked, including all nested manifests and copied source trees. No authored blob/mode conflict, case-fold/NFC collision, symlink, submodule or path traversal was found unless listed below. Repeated generic filenames inside distinct archives are not merged or ignored. The unchanged Lean selector derives project roots only from the canonical registry; nested archived manifests cannot introduce or shadow an active project.

Canonical README.md/problem.tex/problem.pdf files for the 22 affected entries and combined root/category/reference indexes are explicit integration surfaces. Their exemption from whole-file identity does not exempt original titles, IDs, complete mathematical targets, final status semantics, or added RESOLVED/reference-index records. Every other previous-main source/reference/evidence file and each new authored reference/code file outside the two explicitly reviewed #223 repairs must preserve its exact Git blob and mode. Metadata and all 25 source head hashes are frozen in the audit script. The final check uses one immutable Git commit, never the mutable worktree.

Expected final counts: 24 Lean verified, 77 Solved, 46 Open, 70 Partially resolved; 116 still open in total.

| PR | ID | Reviewed head | Authored paths | Original target bytes |
|---|---|---|---:|---:|
| #195 | MI-27 | `b190a7ca5580669ea98d12e23970581abbe6ae7c` | 18 | 1001 |
| #197 | RA-17 | `31756a4a1cc997e48af77637ee90f44e3b8fb7fb` | 28 | 1018 |
| #199 | RA-05 | `98e2ff0c035fd5ebb0532de47db0e687cbaf2a5c` | 34 | 1641 |
| #201 | RA-04 | `f1e8b7d324823ccca225cbd261330b727b423cab` | 24 | 2023 |
| #202 | MI-16 | `a183f28836d47f22a270e50ebf0c3f1b0729a1e9` | 37 | 797 |
| #203 | IS-03 | `ec0b2c267f476c2e9abd04322ba18e43d2be4b13` | 819 | 749 |
| #204 | RE-06 | `e898eb61eccaa1cd8a9a7e0b25d64f176fd71a53` | 29 | 1488 |
| #205 | TR-08 | `9777c86853b40206f70438c92a47a7dec9bc66ae` | 22 | 1939 |
| #207 | RA-04 | `754aa792a5a19d25a353a3975912558820184edf` | 38 | 2023 |
| #209 | PF-04 | `3fececca7c8dbdc594270e07626f6af7ff9e7f14` | 17 | 1405 |
| #211 | PF-03 | `d4c9b7568f237a9467dbf91bfae4b5ffa655d970` | 37 | 1193 |
| #213 | PF-01 | `d499a398d5d0f8b5a07e8b31fa8d0deb1020bdba` | 40 | 1409 |
| #214 | NR-03 | `1a0d3fd4315e9683d56745de586a469b85d2e0ac` | 26 | 933 |
| #216 | NM-01 | `946ce081fb7d67d5f1cae6da688e7c6f7e945418` | 67 | 2181 |
| #217 | NR-01 | `55163265143e2f2b180268b2693ea7d582065806` | 67 | 810 |
| #218 | TR-09 | `40b933b77b654055a2ad2cb9b8ed8b3c9e8b5974` | 29 | 1439 |
| #219 | MD-02 | `f7705090561ed0cc831bce5ad297983ede2c2b7f` | 35 | 780 |
| #220 | RA-14 | `32c71ebf9ee7d89874fcc4c82deae8d374874854` | 51 | 1555 |
| #222 | RA-05 | `f540441a8521a724461c7b393ed1f19f5e1b2b57` | 39 | 1641 |
| #223 | RA-17 | `957c36750778d0414bdaab6ee0b92d6db7396253` | 60 | 1018 |
| #224 | MF-16 | `18d5719d7f0642e549829588799d19cb3d11ecea` | 862 | 693 |
| #225 | RA-08 | `bd82acc73c14835b1497c9bd664648d30f27a925` | 1498 | 1107 |
| #226 | RE-03 | `5561d3efbe8bfd5502d7b5889c46b75f1be4aad2` | 28 | 1549 |
| #227 | RA-09 | `8d1048119fb3664e2b4123bfda28ba7dffaa6e2b` | 1299 | 1167 |
| #228 | RA-20 | `a62bb7e56d858af6a7725d4b12ac657b36b6bda2` | 1840 | 1219 |

Final frozen commit: `b7495d4cf9442c2e1a12956dbd99edc0b8ad5477`; tree `84f7939bdefb52e0eda2cca3e52e7b4bca2f3434`. All checks above were exercised on its 15,960 tracked paths. All 25 source heads and the previous main must be ancestors. Newly authored resolution-record lines checked: 70; reference-index lines: 1.

Exactly 7,042 authored files retain their original blobs and modes. The two explicit authored exceptions are the repaired #223 optional checker and the package README’s four-line repair link; their original/final blobs and SHA-256 values are recorded separately in the JSON. The new regression file and MAINTAINER_CHECKER_CORRECTION.md are independently reviewed additions with exact bound hashes. The 53 maintainer evidence records are confined to the approved audit directory, and every record’s type, blob and SHA-256 is inventoried. No additional integration-only file is accepted.

The history review protects 403 prior resolution lines plus 70 new resolution/credit lines and the new reference-index line. Eight precise historical replacements from b38e398 preserve earlier scopes while identifying later resolutions; the relative-direction typo in the moved RA-04 record was corrected. The new-main advance from 1c467f8 to 2db1e58 changes exactly four files and only the catalog phrase “Lean verified” to “solved with Lean verification”; all logic and test assertions are otherwise unchanged.

Unreviewed integration-only paths:
None.

This preservation script executes no submitted code, validators, test suites or Lean programs. The separate independent #223 repair review ran its ten regression methods on an isolated frozen scratch copy with optimized Python; all passed. No integration source, Git state or GitHub state was mutated. This surface/preservation review supplements the separate mathematical reviews and independently authenticated CI receipts; it does not replace them.
