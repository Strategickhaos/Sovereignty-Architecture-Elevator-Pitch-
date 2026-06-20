"""
BOARD-40-SAGCO-SOLVER — fingerprint.py
Compute sha256, size, extension, and mtime for any file.
"""

import hashlib
import os
import time
from pathlib import Path


def fingerprint(path: str) -> dict:
    """
    Returns {sha256, size_bytes, extension, modified, path}
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"fingerprint: path not found: {path}")

    sha = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)

    stat = p.stat()
    return {
        "sha256":     sha.hexdigest(),
        "size_bytes": stat.st_size,
        "extension":  p.suffix.lstrip(".").lower() or "unknown",
        "modified":   time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(stat.st_mtime)),
        "path":       str(p.resolve()),
        "name":       p.name,
    }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Usage: fingerprint.py <file>")
        sys.exit(1)
    result = fingerprint(sys.argv[1])
    print(json.dumps(result, indent=2))
