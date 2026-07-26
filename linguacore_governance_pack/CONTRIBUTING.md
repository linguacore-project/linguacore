# Contributing to LinguaCore

LinguaCore welcomes contributions to its software, executable specifications, documentation, tests, and project infrastructure.

## Development principles

Contributions must preserve the following rules:

1. Knowledge is represented once and referenced elsewhere.
2. Scientific claims remain traceable to evidence and provenance.
3. Imported or machine-generated material is never treated as reviewed by default.
4. Language-specific logic belongs in project configuration or plugins, not in the language-independent core.
5. Changes to persistent concepts require an architectural record or specification update.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python tools/generate.py
pytest
```

## Before opening a pull request

Run:

```bash
ruff check .
python tools/generate.py
git diff --exit-code generated/
pytest
```

A pull request should:

- describe the problem and the proposed change;
- include or update tests;
- update executable specifications when the domain model changes;
- avoid unrelated formatting or generated-file changes;
- identify compatibility or migration consequences.

## Architecture changes

Open an issue before implementing a change that affects:

- the root `Resource` model;
- persistent identifiers;
- provenance, evidence, review, or publication semantics;
- database compatibility;
- public APIs or interchange formats;
- boundaries between LinguaCore and language-specific projects.

Substantial decisions should be recorded as an ADR under `docs/`.

## Data and community responsibilities

Do not contribute restricted, culturally sensitive, personally identifying, or improperly licensed language data. Contributors are responsible for verifying that material may be stored and distributed under its declared access conditions and license.

## Licensing

By contributing, you agree that your contribution may be distributed under the Apache License 2.0. Data packaged with a LinguaCore project may use a different explicit license and access policy.
