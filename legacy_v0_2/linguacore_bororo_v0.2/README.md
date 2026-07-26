# LinguaCore / Boe eno Moto — arquitetura v0.2

Primeira fundação executável para uma plataforma linguística multilíngue, com Bororo como implementação inicial.

## Conteúdo

- `docs/knowledge-graph.mmd`: grafo conceitual em Mermaid.
- `docs/architecture-decisions.md`: decisões arquitetônicas consolidadas.
- `schema/schema.sql`: esquema PostgreSQL versionado e editorialmente seguro.
- `api/openapi.yaml`: contrato REST inicial.
- `importers/`: importadores para dicionário TSV, CoNLL-U e corpus ZIP.
- `config/bororo-manifest.example.yaml`: manifesto que escolhe fontes canônicas e evita duplicações.
- `tests/`: testes básicos dos importadores.

## Regra crítica

Nenhum dado importado é validado automaticamente. O estado inicial é `imported_unverified`. Validação estrutural e validação linguística são processos independentes.

## Execução rápida

```bash
python -m importers.dictionary_tsv INPUT.tsv OUTPUT.jsonl
python -m importers.conllu INPUT.conllu OUTPUT.jsonl
python -m importers.corpus_inventory Bororo-Corpus-main.zip reports/corpus_inventory.json
```
