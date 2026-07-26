from __future__ import annotations
import hashlib, json, unicodedata, uuid
from pathlib import Path

NAMESPACE = uuid.UUID("18a2ee30-09d1-4adc-a67e-6e29f707b793")

def stable_uuid(kind: str, key: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{kind}:{key}"))

def clean(value: object) -> str | None:
    value = str(value or "").strip()
    return value or None

def normalize(value: str | None) -> str | None:
    if value is None: return None
    return unicodedata.normalize("NFC", value).casefold().strip()

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def emit_jsonl(path: Path, records):
    with path.open("w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
