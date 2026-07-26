import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("LINGUACORE_DATABASE_URL", "sqlite:///./linguacore.db")
kwargs = {}
if DATABASE_URL == "sqlite:///:memory:":
    kwargs = {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
elif DATABASE_URL.startswith("sqlite"):
    kwargs = {"connect_args": {"check_same_thread": False}}
engine = create_engine(DATABASE_URL, **kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
