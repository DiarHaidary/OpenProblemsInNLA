#!/usr/bin/env python3
"""Create an exact review-input inventory. This does not freeze or approve statements."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
SELF = "DRAFT-INVENTORY.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files():
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file())
    assert not any(p.is_symlink() for p in ROOT.rglob("*")), "No symlink input permitted"
    return {str(p.relative_to(ROOT)): {"sha256": digest(p), "bytes": p.stat().st_size}
            for p in paths if str(p.relative_to(ROOT)) != SELF}


def main():
    assert (ROOT / "STATEMENT-HANDOFF.md").is_file()
    generation = {"phase": "draft inventory generation, not freeze or approval", "argv": sys.argv,
                  "cwd": os.getcwd(), "script_sha256": digest(Path(__file__).resolve()),
                  "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  "only_exclusion": SELF,
                  "inclusion_rule": "Every regular file below project root including all source snapshots, failed attempts, logs, scripts, and nested manifests.",
                  "independent_statement_approvals": 0, "proof_authorized": False}
    (ROOT / "verification/inventory-generation.json").write_text(json.dumps(generation, indent=2, sort_keys=True) + "\n")
    items = files()
    inventory = {"schema_version": 1, "phase": "statement-only draft awaiting independent review",
                 "canonical_id": "KE-04", "canonical_path": "eigenvalues-and-inverse-problems/KE-04/README.md",
                 "canonical_base": "5830ed4fb06da0659414a3deb2a40ad327aca052",
                 "excluded_paths": [SELF], "input_count": len(items), "files": items,
                 "proof_authorized": False, "statement_frozen": False}
    path = ROOT / SELF
    path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")
    assert json.loads(path.read_text())["files"] == files()
    assert len(list(p for p in ROOT.rglob("*") if p.is_file())) == len(items) + 1
    print(json.dumps({"inventory": SELF, "sha256": digest(path), "input_count": len(items),
                      "files_including_inventory": len(items) + 1,
                      "handoff_sha256": digest(ROOT / "STATEMENT-HANDOFF.md"),
                      "exact_hash_and_membership_recheck": True, "proof_authorized": False}))


if __name__ == "__main__":
    main()
