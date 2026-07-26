# Generated entity catalogue

## EVI-0001 — EvidenceLink

A typed link connecting a claim or interpretation to primary evidence.

| Field | Type | Required |
|---|---|---|
| `claim_resource_id` | `uuid` | yes |
| `evidence_resource_id` | `uuid` | yes |
| `relation_type` | `string` | yes |
| `note` | `string` | no |

## LAN-0001 — Language

A human language or documented language variety.

| Field | Type | Required |
|---|---|---|
| `name` | `string` | yes |
| `native_name` | `string` | no |
| `iso_639_3` | `string` | no |
| `glottocode` | `string` | no |
| `description` | `string` | no |

## SEN-0001 — Sentence

A segment of linguistic text that may carry translations, annotations and evidence links.

| Field | Type | Required |
|---|---|---|
| `text_id` | `uuid` | no |
| `sequence` | `integer` | yes |
| `transcription` | `string` | yes |
| `normalized_text` | `string` | no |
| `translation_pt` | `string` | no |
| `translation_en` | `string` | no |
| `speaker_id` | `uuid` | no |
| `start_ms` | `integer` | no |
| `end_ms` | `integer` | no |

