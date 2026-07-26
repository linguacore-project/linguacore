from __future__ import annotations
import argparse, csv
from collections import Counter
from pathlib import Path
from .common import clean, emit_jsonl, normalize, stable_uuid

AUDIO_FIELDS = ("áudio", "áudio2", "áudio3")

def records(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as src:
        rows = list(csv.DictReader(src, delimiter="\t"))
    id_counts = Counter(clean(r.get("id")) for r in rows if clean(r.get("id")))
    for row_no, row in enumerate(rows, start=2):
        source_id = clean(row.get("id"))
        unique_id = source_id and id_counts[source_id] == 1
        seed = source_id if unique_id else f"row-{row_no}-{clean(row.get('entry')) or ''}"
        headword = clean(row.get("entry"))
        yield {
            "resource_id": stable_uuid("dictionary_entry", seed),
            "resource_type": "dictionary_entry",
            "status": "imported_unverified",
            "external_identifier": source_id,
            "source_row": row_no,
            "headword": headword,
            "normalized_headword": normalize(headword),
            "ipa": clean(row.get("ipa")),
            "pos": clean(row.get("pos")),
            "scientific_name": clean(row.get("scientific_name")),
            "note": clean(row.get("comment")),
            "senses": [{
                "resource_id": stable_uuid("sense", f"{seed}:1"),
                "sense_no": 1,
                "definition_language": "pt",
                "definition": clean(row.get("definition")),
                "legacy_example_text": clean(row.get("example_sent")),
                "status": "imported_unverified"
            }],
            "media_references": [clean(row.get(k)) for k in AUDIO_FIELDS if clean(row.get(k))],
            "links": {"wiki": clean(row.get("wiki_link")), "image": clean(row.get("pic_link"))},
            "raw_payload": row,
        }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path); ap.add_argument("output", type=Path)
    args = ap.parse_args(); emit_jsonl(args.output, records(args.input))
if __name__ == "__main__": main()
