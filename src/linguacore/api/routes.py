from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from linguacore.db import get_db
from linguacore.domain.models import Language, Sentence
from linguacore.api.schemas import LanguageCreate, LanguageRead, SentenceCreate, SentenceRead
router=APIRouter(prefix="/v1")
@router.get("/health")
def health(): return {"status":"ok", "service":"linguacore", "version":"0.3.0"}
@router.post("/languages", response_model=LanguageRead, status_code=201)
def create_language(payload: LanguageCreate, db: Session=Depends(get_db)):
    obj=Language(resource_type="language", visibility="restricted", editorial_status="draft", **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj
@router.get("/languages", response_model=list[LanguageRead])
def list_languages(db: Session=Depends(get_db)):
    return list(db.scalars(select(Language).order_by(Language.name)))
@router.post("/sentences", response_model=SentenceRead, status_code=201)
def create_sentence(payload: SentenceCreate, db: Session=Depends(get_db)):
    if not db.get(Language,payload.language_id): raise HTTPException(404,"language not found")
    obj=Sentence(resource_type="sentence", editorial_status="draft", visibility="restricted", **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj
@router.get("/sentences", response_model=list[SentenceRead])
def list_sentences(language_id: str|None=None, db: Session=Depends(get_db)):
    q=select(Sentence).order_by(Sentence.sequence)
    if language_id: q=q.where(Sentence.language_id==language_id)
    return list(db.scalars(q))
