#!/usr/bin/env python3
"""Read-only integrity check for the sealed KE-04 operational evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST_NAME = "EVIDENCE-MANIFEST.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relative_files() -> set[str]:
    found: set[str] = set()
    for path in ROOT.rglob("*"):
        if path.is_symlink():
            raise SystemExit(f"symlink is not evidence: {path.relative_to(ROOT)}")
        if path.is_file():
            found.add(path.relative_to(ROOT).as_posix())
    return found


def main() -> None:
    manifest_path = ROOT / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("self_exclusion") != MANIFEST_NAME:
        raise SystemExit("manifest self-exclusion is not exactly the manifest")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise SystemExit("manifest files must be an object")
    actual = relative_files()
    expected = set(files)
    if MANIFEST_NAME in expected:
        raise SystemExit("manifest may not list itself")
    unlisted = sorted(actual - expected - {MANIFEST_NAME})
    missing = sorted(expected - actual)
    if unlisted or missing:
        raise SystemExit(json.dumps({"unlisted": unlisted, "missing": missing}))
    checked = 0
    for name, record in sorted(files.items()):
        path = ROOT / name
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise SystemExit(f"unsafe evidence path: {name}")
        if not isinstance(record, dict):
            raise SystemExit(f"bad record: {name}")
        actual_size = path.stat().st_size
        actual_hash = digest(path)
        if actual_size != record.get("bytes") or actual_hash != record.get("sha256"):
            raise SystemExit(f"evidence changed: {name}")
        checked += 1
    print(json.dumps({"success": True, "checked_files": checked,
                      "self_exclusion": MANIFEST_NAME}, indent=2))


if __name__ == "__main__":
    main()
