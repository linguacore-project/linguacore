from pydantic import BaseModel, ConfigDict, Field, model_validator
class LanguageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    native_name: str|None=None
    iso_639_3: str|None=Field(default=None, pattern=r"^[a-z]{3}$")
    glottocode: str|None=None
    description: str|None=None
class LanguageRead(LanguageCreate):
    model_config=ConfigDict(from_attributes=True)
    id: str
    editorial_status: str
    visibility: str
class SentenceCreate(BaseModel):
    language_id: str
    sequence: int=Field(ge=1)
    transcription: str=Field(min_length=1)
    translation_pt: str|None=None
    translation_en: str|None=None
    start_ms: int|None=Field(default=None,ge=0)
    end_ms: int|None=Field(default=None,ge=0)
    @model_validator(mode="after")
    def valid_time(self):
        if self.start_ms is not None and self.end_ms is not None and self.end_ms <= self.start_ms:
            raise ValueError("end_ms must be greater than start_ms")
        return self
class SentenceRead(SentenceCreate):
    model_config=ConfigDict(from_attributes=True)
    id: str
    editorial_status: str
    visibility: str
