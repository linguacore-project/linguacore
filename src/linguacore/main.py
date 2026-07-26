from fastapi import FastAPI
from linguacore.api.routes import router
from linguacore.db import Base, engine
Base.metadata.create_all(bind=engine)
app=FastAPI(title="LinguaCore API", version="0.3.0", description="Evidence-first infrastructure for language documentation")
app.include_router(router)
