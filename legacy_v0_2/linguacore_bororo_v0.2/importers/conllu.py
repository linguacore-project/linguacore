from __future__ import annotations
import argparse
from pathlib import Path
from .common import emit_jsonl, stable_uuid

def feats(value: str):
    if value == "_": return {}
    result = {}
    for item in value.split("|"):
        if "=" in item:
            key, val = item.split("=", 1); result[key] = val
    return result

def parse(path: Path):
    metadata, rows, ordinal = {}, [], 0
    def flush():
        nonlocal ordinal, metadata, rows
        if not metadata and not rows: return None
        ordinal += 1
        external = metadata.get("sent_id") or f"unnamed-{ordinal}"
        sentence_id = stable_uuid("sentence", f"{external}:{ordinal}")
        tokens = []
        for line_no, columns in rows:
            if len(columns) != 10:
                tokens.append({"line_no": line_no, "malformed": True, "columns": columns})
                continue
            tid, form, lemma, upos, xpos, fts, head, deprel, deps, misc = columns
            token_id = stable_uuid("token", f"{sentence_id}:{tid}")
            tokens.append({
                "resource_id": token_id, "source_token_id": tid, "form": form,
                "status": "imported_unverified",
                "morphological_analyses": [{
                    "lemma_form": None if lemma == "_" else lemma,
                    "upos": None if upos == "_" else upos,
                    "xpos": None if xpos == "_" else xpos,
                    "features": feats(fts), "method": "imported",
                    "status": "imported_unverified", "preferred": False
                }],
                "dependency_proposal": {
                    "source_head_id": None if head == "_" else head,
                    "relation": None if deprel == "_" else deprel,
                    "enhanced": None if deps == "_" else deps,
                    "method": "imported", "status": "imported_unverified"
                },
                "misc": None if misc == "_" else misc,
                "lexical_link_status": "suggested"
            })
        record = {
            "resource_id": sentence_id, "external_identifier": external,
            "surface_text": metadata.get("text", ""),
            "status": "imported_unverified",
            "tokenization_status": "imported_unverified",
            "translations": [
                {"language": lang, "text": metadata[key], "status": "imported_unverified"}
                for key, lang in (("text_por", "pt"), ("text_eng", "en"))
                if metadata.get(key, "").strip()
            ],
            "tokens": tokens, "raw_metadata": metadata
        }
        metadata, rows = {}, []
        return record

    with path.open(encoding="utf-8-sig") as src:
        for line_no, raw in enumerate(src, start=1):
            line = raw.rstrip("\n\r")
            if not line.strip():
                record = flush()
                if record: yield record
            elif line.startswith("#"):
                body = line[1:].strip()
                if "=" in body:
                    key, value = body.split("=", 1); metadata[key.strip()] = value.strip()
            else:
                rows.append((line_no, line.split("\t")))
    record = flush()
    if record: yield record

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("input", type=Path); ap.add_argument("output", type=Path)
    args = ap.parse_args(); emit_jsonl(args.output, parse(args.input))
if __name__ == "__main__": main()
