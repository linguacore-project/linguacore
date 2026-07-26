# Generated; do not edit manually.
from datetime import datetime
from pydantic import BaseModel
from linguacore.domain.enums import EditorialStatus, Visibility

class EvidenceLinkSpec(BaseModel):
    claim_resource_id: str
    evidence_resource_id: str
    relation_type: str
    note: str | None = None

class LanguageSpec(BaseModel):
    name: str
    native_name: str | None = None
    iso_639_3: str | None = None
    glottocode: str | None = None
    description: str | None = None

class SentenceSpec(BaseModel):
    text_id: str | None = None
    sequence: int
    transcription: str
    normalized_text: str | None = None
    translation_pt: str | None = None
    translation_en: str | None = None
    speaker_id: str | None = None
    start_ms: int | None = None
    end_ms: int | None = None

