# LinguaCore v0.3 — executable foundation

A runnable foundation for an evidence-first language documentation platform. Bororo is the canonical demonstration project; the core contains no Bororo-specific business logic.

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
uvicorn linguacore.main:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

## Test

```bash
pytest
```

## Core rule

Imported material begins as `imported_unverified`. AI output and automated imports may propose data but cannot publish or validate scientific claims.
