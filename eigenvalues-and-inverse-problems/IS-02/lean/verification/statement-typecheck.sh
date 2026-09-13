#!/usr/bin/env bash
set -euo pipefail

# Statement-stage check only. It deliberately invokes Lean directly and never
# runs Lake: dependency objects are supplied read-only by IS02_DEP_ROOT, while
# all newly written artifacts go to one fresh private prefix.
project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
dep_root=${IS02_DEP_ROOT:?Set IS02_DEP_ROOT to an existing .lake/packages directory}
lean_bin=${LEAN_BIN:-lean}
tmp_root=${IS02_TYPECHECK_TMPDIR:-${TMPDIR:-/tmp}}
prefix=$(mktemp -d "${tmp_root%/}/nla-is02-statement-typecheck.XXXXXX")
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
$lean_bin -R "$project_dir" -o "$out/Challenge.olean" \
  "$project_dir/Challenge.lean"

printf 'statement boundary typecheck: PASS\n'
printf 'lean: %s\n' "$version"
printf 'output prefix: %s\n' "$prefix"
printf 'challenge warnings: intentional sorry placeholders only\n'
