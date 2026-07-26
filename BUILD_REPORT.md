# LinguaCore v0.3 build report

## Delivered

- Runnable FastAPI service and SQLAlchemy persistence layer.
- `Resource` root with joined-table `Language` and `Sentence` models.
- Initial Alembic migration.
- Executable YAML specifications for Resource, Language, Sentence and EvidenceLink.
- Generator producing Pydantic specifications, TypeScript interfaces and an entity catalogue.
- Bororo reference-project manifest without Bororo-specific core logic.
- Docker and PostgreSQL development environment.
- Preserved v0.2 importers, schema, OpenAPI contract and architecture documents.

## Validation

- Test suite: 6 passed.
- Generator: successful.
- Import policy: automated imports begin as `imported_unverified`; automatic publication is disabled.

## Next implementation target

Version 0.4 should add persistent import jobs, source manifests, checksums, staging records, validation reports and idempotent CoNLL-U/dictionary ingestion.
