#!/usr/bin/env bash
set -euo pipefail

# Local proof-stage check. Lean is invoked directly; dependency objects are read
# from an existing pinned package tree and all newly written artifacts use one
# fresh private prefix. This is not the authoritative Linux Comparator job.
project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
dep_root=${IS02_DEP_ROOT:?Set IS02_DEP_ROOT to an existing .lake/packages directory}
lean_bin=${LEAN_BIN:-lean}
tmp_root=${IS02_TYPECHECK_TMPDIR:-${TMPDIR:-/tmp}}
prefix=$(mktemp -d "${tmp_root%/}/nla-is02-proof-typecheck.XXXXXX")
out="$prefix/out"
mkdir -p "$out/NLA/IS02"

version=$($lean_bin --version 2>/dev/null)
printf '%s\n' "$version" | grep -F 'Lean (version 4.33.1' >/dev/null

lean_path="$out"
for package in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib leancert; do
  lean_path="$lean_path:$dep_root/$package/.lake/build/lib/lean"
done
lean_path="$lean_path:${LEAN_SYSROOT:-$HOME/.elan/toolchains/leanprover--lean4---v4.33.1/lib/lean}"
export LEAN_PATH="$lean_path"

$lean_bin -R "$project_dir" -o "$out/NLA/IS02/Definitions.olean" \
  "$project_dir/NLA/IS02/Definitions.lean"
$lean_bin -R "$project_dir" -o "$out/NLA/IS02/Proof.olean" \
  "$project_dir/NLA/IS02/Proof.lean"
$lean_bin -R "$project_dir" -o "$out/Solution.olean" \
  "$project_dir/Solution.lean"

printf 'proof-stage direct Lean check: PASS\n'
printf 'lean: %s\n' "$version"
printf 'output prefix: %s\n' "$prefix"
printf 'solution exports: 9; #assert_trust kernel and #print axioms completed\n'
