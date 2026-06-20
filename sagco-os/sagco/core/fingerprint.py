"""SHA-256 fingerprinting via stdlib hashlib."""
import hashlib
import json


def sha256_str(text: str) -> str:
    """Return SHA-256 hex digest of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str) -> str:
    """Return SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_dict(d: dict) -> str:
    """Return SHA-256 hex digest of a dict (sorted keys)."""
    serialized = json.dumps(d, sort_keys=True, ensure_ascii=False)
    return sha256_str(serialized)


def fingerprint_rows(rows: list) -> str:
    """Return SHA-256 of a list of dicts."""
    serialized = json.dumps(rows, sort_keys=True, ensure_ascii=False)
    return sha256_str(serialized)
