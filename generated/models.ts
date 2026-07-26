// Generated; do not edit manually.
export type EditorialStatus = 'draft' | 'imported_unverified' | 'in_review' | 'reviewed' | 'published' | 'archived';
export type Visibility = 'public' | 'community' | 'restricted';

export interface EvidenceLinkSpec {
  claim_resource_id: string;
  evidence_resource_id: string;
  relation_type: string;
  note?: string;
}

export interface LanguageSpec {
  name: string;
  native_name?: string;
  iso_639_3?: string;
  glottocode?: string;
  description?: string;
}

export interface SentenceSpec {
  text_id?: string;
  sequence: number;
  transcription: string;
  normalized_text?: string;
  translation_pt?: string;
  translation_en?: string;
  speaker_id?: string;
  start_ms?: number;
  end_ms?: number;
}

