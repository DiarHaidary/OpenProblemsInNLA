#!/usr/bin/env python3
"""Check the reviewed KE-04 bytes after the two documented packaging changes.

This is an identity check, not an independent mathematical or Linux review.
The historical review verifiers expect the pre-packaging paths. Here only the
README and Lakefile are mapped to their exact archives; mathematical inputs and
every other sealed file must still match at their original paths.
"""
from pathlib import Path
import hashlib
import json

PROJECT = Path(__file__).resolve().parents[2]
ARCHIVES = {
    "README.md": "verification/packaging/frozen-inputs/README.md",
    "lakefile.toml": "verification/packaging/frozen-inputs/lakefile.toml",
}
SEALS = {
    "reviews/proof-freeze.json":
        "394db25967661b12b107062fb00976dc847817c03942dca44c4725492d4003c4",
    "reviews/final-referee-1-evidence/EVIDENCE-MANIFEST.json":
        "db660ae18b7efa4b6d41602e5a16a465bd932621061081efa5b6ac70ff221d70",
    "reviews/final-referee-2-evidence/EVIDENCE-MANIFEST.json":
        "9788aac814efbb81b88b9d118fed6ca174067fe4fffa945b3dc3656b954e14a9",
}


def read_input(relative):
    path = PROJECT / ARCHIVES.get(relative, relative)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or nonordinary reviewed input: {relative}")
    if not path.resolve().is_relative_to(PROJECT):
        raise ValueError(f"Reviewed input escapes project: {relative}")
    return path.read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    counts = {}
    for relative, expected in SEALS.items():
        raw = read_input(relative)
        if digest(raw) != expected:
            raise ValueError(f"Historical seal changed: {relative}")
        manifest = json.loads(raw)
        for name, record in manifest["files"].items():
            data = read_input(name)
            target = record if isinstance(record, str) else record["sha256"]
            size = manifest.get("file_sizes", {}).get(name)
            if isinstance(record, dict):
                size = record["bytes"]
            if digest(data) != target or (size is not None and len(data) != size):
                raise ValueError(f"Reviewed input differs: {relative}: {name}")
        counts[relative] = len(manifest["files"])

    old_lakefile = read_input("lakefile.toml").decode()
    expected_lakefile = old_lakefile.replace(
        'defaultTargets = ["Challenge"]', 'defaultTargets = ["Solution"]'
    ).replace(
        "# Reserved for the post-approval proof phase; no Solution source exists yet.",
        "# The completed proof is built independently of the reference Challenge.",
    )
    if (PROJECT / "lakefile.toml").read_text() != expected_lakefile:
        raise ValueError("Lakefile changes exceed the documented default and comment")
    print(json.dumps({"success": True, "sealed_file_counts": counts,
                      "exact_archive_mapping": ARCHIVES}, indent=2))


if __name__ == "__main__":
    main()
