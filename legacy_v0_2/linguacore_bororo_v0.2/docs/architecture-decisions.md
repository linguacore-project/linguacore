# Decisões arquitetônicas v0.2

## ADR-001 — Núcleo multilíngue
O código pertence ao LinguaCore; Bororo é uma instância configurada por dados e manifestos.

## ADR-002 — Recursos com identificadores imutáveis
Todos os objetos publicados usam UUID. Identificadores externos são preservados em `external_identifier`, nunca usados como única chave interna.

## ADR-003 — Estado editorial explícito
O estado inicial de uma importação é `imported_unverified`. Uma estrutura formalmente completa não implica correção linguística.

## ADR-004 — Revisões imutáveis
Alterações editoriais criam revisões. O registro atual aponta para a revisão vigente; versões anteriores permanecem recuperáveis.

## ADR-005 — Análises concorrentes
Um token pode possuir diversas análises morfológicas e sintáticas, manuais ou automáticas. Apenas uma pode ser marcada como preferida por camada, sem eliminar alternativas.

## ADR-006 — Proveniência em nível de afirmação
Definições, traduções, análises e vínculos podem apontar para fonte, página, importação, agente e método.

## ADR-007 — Importação idempotente
Cada lote registra SHA-256 e caminho lógico. Reimportar a mesma fonte não duplica recursos.

## ADR-008 — Manifesto de corpus
O ZIP contém versões derivadas e potencialmente sobrepostas. Um manifesto define quais arquivos são canônicos e quais são apenas exportações.

## ADR-009 — API antes da interface
Leitor, painel administrativo e aplicativo móvel consomem o mesmo contrato REST.

## ADR-010 — Publicação conservadora
Análises `imported_unverified` podem ser exibidas apenas com aviso explícito ou ocultadas. Consultas científicas podem filtrar por estado editorial.
