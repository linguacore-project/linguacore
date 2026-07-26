from __future__ import annotations
import argparse, csv, io, json, zipfile, sys
from pathlib import Path
from .common import sha256

csv.field_size_limit(min(sys.maxsize, 2**31-1))

def inspect_zip(path: Path):
    report = {"source": str(path), "sha256": sha256(path), "files": [], "possible_overlaps": []}
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir() or info.filename.startswith("__MACOSX/"): continue
            item = {"path": info.filename, "bytes": info.file_size, "extension": Path(info.filename).suffix.lower()}
            if item["extension"] in {".csv", ".tsv"} and info.file_size < 5_000_000:
                raw = zf.read(info).decode("utf-8-sig", errors="replace")
                delimiter = "\t" if item["extension"] == ".tsv" else ","
                reader = csv.reader(io.StringIO(raw), delimiter=delimiter)
                rows = list(reader)
                item["row_count"] = max(0, len(rows) - 1)
                item["columns"] = rows[0] if rows else []
            report["files"].append(item)
    stems = {}
    for item in report["files"]:
        stem = Path(item["path"]).stem.casefold().replace("-", "_")
        stems.setdefault(stem, []).append(item["path"])
    report["possible_overlaps"] = [v for v in stems.values() if len(v) > 1]
    return report

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input", type=Path); ap.add_argument("output", type=Path)
    args=ap.parse_args(); args.output.write_text(json.dumps(inspect_zip(args.input), ensure_ascii=False, indent=2), encoding="utf-8")
if __name__ == "__main__": main()
