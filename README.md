# DocuLing

**An Open Scientific Infrastructure for Language Documentation, Research, Education, and Revitalization**

DocuLing is an open-source platform that integrates linguistic corpora, lexicons, grammars, multimedia resources, educational materials, and reproducible research workflows within a unified, evidence-based infrastructure.

The project is designed for documentary linguists, language communities, educators, archivists, researchers, and software developers. Its architecture prioritizes provenance, versioning, interoperability, scientific reproducibility, and community control over linguistic data.

> **Current status:** early architectural prototype. The data model, interfaces, and APIs remain under active development.

## Included

- FastAPI application with health, language, resource and sentence endpoints
- SQLAlchemy domain models and initial Alembic migration
- Executable YAML entity specifications
- Generator for Pydantic models, TypeScript interfaces and documentation tables
- Bororo project manifest
- Existing v0.2 importers and architecture assets preserved under `legacy_v0_2/`
- Unit tests for specifications, generation and API behavior
- Docker Compose for PostgreSQL and the API

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python tools/generate.py
uvicorn doculing.main:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

## Test

```bash
pytest
```

## Core rule

Imported material begins as `imported_unverified`. AI output and automated imports may propose data but cannot publish or validate scientific claims.
