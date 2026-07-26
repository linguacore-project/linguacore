CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TYPE editorial_status AS ENUM (
  'draft','imported_unverified','under_review','partially_validated',
  'validated','published','rejected','superseded','archived'
);
CREATE TYPE access_level AS ENUM ('public','registered','community','research','restricted','private');
CREATE TYPE assertion_method AS ENUM ('manual','automatic','imported','inferred');
CREATE TYPE link_decision AS ENUM ('suggested','confirmed','rejected');

CREATE TABLE agent (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  display_name text NOT NULL,
  agent_type text NOT NULL CHECK (agent_type IN ('person','organization','software')),
  orcid text,
  metadata jsonb NOT NULL DEFAULT '{}'
);

CREATE TABLE language (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  iso639_3 char(3),
  glottocode text,
  name text NOT NULL,
  autonym text,
  slug text NOT NULL UNIQUE,
  metadata jsonb NOT NULL DEFAULT '{}'
);

CREATE TABLE resource (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  resource_type text NOT NULL,
  language_id uuid REFERENCES language(id),
  stable_slug text,
  status editorial_status NOT NULL DEFAULT 'draft',
  access access_level NOT NULL DEFAULT 'public',
  license_uri text,
  current_revision_id uuid,
  created_by uuid REFERENCES agent(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(language_id, resource_type, stable_slug)
);

CREATE TABLE resource_revision (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  resource_id uuid NOT NULL REFERENCES resource(id) ON DELETE CASCADE,
  revision_no integer NOT NULL,
  payload jsonb NOT NULL,
  status editorial_status NOT NULL,
  changed_by uuid REFERENCES agent(id),
  change_note text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(resource_id, revision_no)
);
ALTER TABLE resource ADD CONSTRAINT resource_current_revision_fk
  FOREIGN KEY (current_revision_id) REFERENCES resource_revision(id);

CREATE TABLE import_batch (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  language_id uuid REFERENCES language(id),
  source_path text NOT NULL,
  source_sha256 char(64) NOT NULL,
  importer text NOT NULL,
  importer_version text NOT NULL,
  manifest_key text,
  imported_by uuid REFERENCES agent(id),
  imported_at timestamptz NOT NULL DEFAULT now(),
  report jsonb NOT NULL DEFAULT '{}',
  UNIQUE(source_sha256, importer, importer_version)
);

CREATE TABLE external_identifier (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  resource_id uuid NOT NULL REFERENCES resource(id) ON DELETE CASCADE,
  scheme text NOT NULL,
  value text NOT NULL,
  import_batch_id uuid REFERENCES import_batch(id),
  UNIQUE(scheme, value, import_batch_id)
);

CREATE TABLE collection (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  title text NOT NULL,
  description text,
  sequence_no integer
);

CREATE TABLE text_document (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  collection_id uuid REFERENCES collection(resource_id),
  title text,
  genre text,
  source_description text,
  sequence_no integer
);

CREATE TABLE sentence (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  text_id uuid REFERENCES text_document(resource_id) ON DELETE CASCADE,
  sequence_no integer,
  surface_text text NOT NULL,
  tokenization_status editorial_status NOT NULL DEFAULT 'imported_unverified',
  raw_metadata jsonb NOT NULL DEFAULT '{}'
);
CREATE INDEX sentence_text_search_idx ON sentence USING gin (surface_text gin_trgm_ops);

CREATE TABLE translation (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  sentence_id uuid NOT NULL REFERENCES sentence(resource_id) ON DELETE CASCADE,
  target_language_code text NOT NULL,
  translation_type text NOT NULL DEFAULT 'free',
  text text NOT NULL,
  translator_id uuid REFERENCES agent(id)
);

CREATE TABLE token (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  sentence_id uuid NOT NULL REFERENCES sentence(resource_id) ON DELETE CASCADE,
  position numeric(12,3) NOT NULL,
  source_token_id text,
  form text NOT NULL,
  normalized_form text,
  is_multiword boolean NOT NULL DEFAULT false,
  is_empty_node boolean NOT NULL DEFAULT false,
  raw_payload jsonb NOT NULL DEFAULT '{}',
  UNIQUE(sentence_id, position)
);
CREATE INDEX token_form_search_idx ON token USING gin (form gin_trgm_ops);

CREATE TABLE lemma (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  citation_form text NOT NULL,
  normalized_form text,
  ipa text,
  broad_pos text
);
CREATE INDEX lemma_form_search_idx ON lemma USING gin (citation_form gin_trgm_ops);

CREATE TABLE dictionary_entry (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  lemma_id uuid REFERENCES lemma(resource_id),
  headword text NOT NULL,
  ipa text,
  pos text,
  scientific_name text,
  note text,
  source_payload jsonb NOT NULL DEFAULT '{}'
);
CREATE INDEX dictionary_headword_search_idx ON dictionary_entry USING gin (headword gin_trgm_ops);

CREATE TABLE sense (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  dictionary_entry_id uuid NOT NULL REFERENCES dictionary_entry(resource_id) ON DELETE CASCADE,
  sense_no integer NOT NULL,
  definition_language text NOT NULL DEFAULT 'pt',
  definition text,
  semantic_domain text,
  UNIQUE(dictionary_entry_id, sense_no)
);

CREATE TABLE corpus_example_link (
  sense_id uuid NOT NULL REFERENCES sense(resource_id) ON DELETE CASCADE,
  sentence_id uuid NOT NULL REFERENCES sentence(resource_id) ON DELETE CASCADE,
  note text,
  status link_decision NOT NULL DEFAULT 'suggested',
  PRIMARY KEY (sense_id, sentence_id)
);

CREATE TABLE lexical_link (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token_id uuid NOT NULL REFERENCES token(resource_id) ON DELETE CASCADE,
  lemma_id uuid REFERENCES lemma(resource_id),
  dictionary_entry_id uuid REFERENCES dictionary_entry(resource_id),
  decision link_decision NOT NULL DEFAULT 'suggested',
  method assertion_method NOT NULL,
  confidence numeric(5,4),
  status editorial_status NOT NULL DEFAULT 'imported_unverified',
  note text
);

CREATE TABLE morphological_analysis (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token_id uuid NOT NULL REFERENCES token(resource_id) ON DELETE CASCADE,
  lemma_form text,
  upos text,
  xpos text,
  features jsonb NOT NULL DEFAULT '{}',
  segmentation text,
  gloss text,
  method assertion_method NOT NULL,
  status editorial_status NOT NULL DEFAULT 'imported_unverified',
  preferred boolean NOT NULL DEFAULT false,
  created_by uuid REFERENCES agent(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX one_preferred_morphology_per_token
  ON morphological_analysis(token_id) WHERE preferred;

CREATE TABLE syntactic_analysis_set (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sentence_id uuid NOT NULL REFERENCES sentence(resource_id) ON DELETE CASCADE,
  framework text NOT NULL DEFAULT 'UD',
  framework_version text,
  method assertion_method NOT NULL,
  status editorial_status NOT NULL DEFAULT 'imported_unverified',
  preferred boolean NOT NULL DEFAULT false,
  created_by uuid REFERENCES agent(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX one_preferred_syntax_set_per_sentence
  ON syntactic_analysis_set(sentence_id) WHERE preferred;

CREATE TABLE dependency_arc (
  analysis_set_id uuid NOT NULL REFERENCES syntactic_analysis_set(id) ON DELETE CASCADE,
  dependent_token_id uuid NOT NULL REFERENCES token(resource_id) ON DELETE CASCADE,
  head_token_id uuid REFERENCES token(resource_id),
  source_head_id text,
  relation text,
  enhanced text,
  PRIMARY KEY (analysis_set_id, dependent_token_id)
);

CREATE TABLE media_asset (
  resource_id uuid PRIMARY KEY REFERENCES resource(id) ON DELETE CASCADE,
  media_type text NOT NULL CHECK (media_type IN ('audio','image','video','document')),
  uri text NOT NULL,
  mime_type text,
  checksum text,
  metadata jsonb NOT NULL DEFAULT '{}'
);

CREATE TABLE resource_media_link (
  resource_id uuid NOT NULL REFERENCES resource(id) ON DELETE CASCADE,
  media_id uuid NOT NULL REFERENCES media_asset(resource_id) ON DELETE CASCADE,
  role text NOT NULL,
  sequence_no integer,
  PRIMARY KEY(resource_id, media_id, role)
);

CREATE TABLE provenance_assertion (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_resource_id uuid NOT NULL REFERENCES resource(id) ON DELETE CASCADE,
  field_path text,
  source_resource_id uuid REFERENCES resource(id),
  import_batch_id uuid REFERENCES import_batch(id),
  agent_id uuid REFERENCES agent(id),
  method assertion_method NOT NULL,
  citation_locator text,
  note text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE editorial_review (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  resource_id uuid REFERENCES resource(id) ON DELETE CASCADE,
  analysis_type text,
  analysis_id uuid,
  previous_status editorial_status,
  new_status editorial_status NOT NULL,
  reviewer_id uuid NOT NULL REFERENCES agent(id),
  note text,
  reviewed_at timestamptz NOT NULL DEFAULT now()
);
