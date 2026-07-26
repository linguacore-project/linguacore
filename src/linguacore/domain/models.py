from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from linguacore.db import Base

def now(): return datetime.now(timezone.utc)
class Resource(Base):
    __tablename__="resources"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    resource_type: Mapped[str]=mapped_column(String(50), index=True)
    language_id: Mapped[str|None]=mapped_column(String(36), nullable=True, index=True)
    organization_id: Mapped[str|None]=mapped_column(String(36), nullable=True)
    editorial_status: Mapped[str]=mapped_column(String(32), default="draft", index=True)
    visibility: Mapped[str]=mapped_column(String(20), default="restricted")
    license: Mapped[str|None]=mapped_column(String(100), nullable=True)
    persistent_uri: Mapped[str|None]=mapped_column(String(500), nullable=True, unique=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    __mapper_args__={"polymorphic_on": resource_type, "polymorphic_identity":"resource"}
class Language(Resource):
    __tablename__="languages"
    id: Mapped[str]=mapped_column(ForeignKey("resources.id"), primary_key=True)
    name: Mapped[str]=mapped_column(String(200), index=True)
    native_name: Mapped[str|None]=mapped_column(String(200), nullable=True)
    iso_639_3: Mapped[str|None]=mapped_column(String(3), unique=True, nullable=True)
    glottocode: Mapped[str|None]=mapped_column(String(20), unique=True, nullable=True)
    description: Mapped[str|None]=mapped_column(Text, nullable=True)
    __mapper_args__={"polymorphic_identity":"language"}
class Sentence(Resource):
    __tablename__="sentences"
    id: Mapped[str]=mapped_column(ForeignKey("resources.id"), primary_key=True)
    text_id: Mapped[str|None]=mapped_column(String(36), nullable=True, index=True)
    sequence: Mapped[int]=mapped_column(Integer)
    transcription: Mapped[str]=mapped_column(Text)
    normalized_text: Mapped[str|None]=mapped_column(Text, nullable=True)
    translation_pt: Mapped[str|None]=mapped_column(Text, nullable=True)
    translation_en: Mapped[str|None]=mapped_column(Text, nullable=True)
    speaker_id: Mapped[str|None]=mapped_column(String(36), nullable=True)
    start_ms: Mapped[int|None]=mapped_column(Integer, nullable=True)
    end_ms: Mapped[int|None]=mapped_column(Integer, nullable=True)
    __mapper_args__={"polymorphic_identity":"sentence"}
