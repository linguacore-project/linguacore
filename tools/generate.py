from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TYPE_MAP = {
    "uuid": "str", "string": "str", "integer": "int", "datetime": "datetime",
    "EditorialStatus": "EditorialStatus", "Visibility": "Visibility",
}
TS_MAP = {
    "uuid": "string", "string": "string", "integer": "number", "datetime": "string",
    "EditorialStatus": "EditorialStatus", "Visibility": "Visibility",
}

def load_specs():
    return [yaml.safe_load(p.read_text()) for p in sorted((ROOT / "spec/entities").glob("*.yaml"))]

def generate():
    specs = load_specs()
    out = ROOT / "generated"
    out.mkdir(exist_ok=True)
    py = [
        "# Generated; do not edit manually.",
        "from datetime import datetime",
        "from pydantic import BaseModel",
        "from linguacore.domain.enums import EditorialStatus, Visibility",
        "",
    ]
    ts = [
        "// Generated; do not edit manually.",
        "export type EditorialStatus = 'draft' | 'imported_unverified' | 'in_review' | 'reviewed' | 'published' | 'archived';",
        "export type Visibility = 'public' | 'community' | 'restricted';",
        "",
    ]
    md = ["# Generated entity catalogue", ""]
    for spec in specs:
        if spec.get("abstract"):
            continue
        name = spec["name"]
        py.append(f"class {name}Spec(BaseModel):")
        ts.append(f"export interface {name}Spec {{")
        fields = spec.get("fields", {})
        if not fields:
            py.append("    pass")
        for field_name, field in fields.items():
            optional = not field.get("required", False)
            py_type = TYPE_MAP.get(field["type"], "str")
            py.append(f"    {field_name}: {py_type}{' | None' if optional else ''}{' = None' if optional else ''}")
            ts.append(f"  {field_name}{'?' if optional else ''}: {TS_MAP.get(field['type'], 'string')};")
        py.append("")
        ts.extend(["}", ""])
        md.extend([
            f"## {spec['code']} — {name}", "", spec.get("description", ""), "",
            "| Field | Type | Required |", "|---|---|---|",
        ])
        for field_name, field in fields.items():
            md.append(f"| `{field_name}` | `{field['type']}` | {'yes' if field.get('required') else 'no'} |")
        md.append("")
    (out / "models.py").write_text("\n".join(py) + "\n")
    (out / "models.ts").write_text("\n".join(ts) + "\n")
    (out / "entities.md").write_text("\n".join(md) + "\n")
    return len(specs)

if __name__ == "__main__":
    print(f"Generated artifacts from {generate()} entity specifications")
