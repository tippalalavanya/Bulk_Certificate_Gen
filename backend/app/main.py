import logging
from fastapi import FastAPI
from sqlalchemy import text
from app.api.routes import jobs, certificates
from app.core.config import settings
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
app = FastAPI(title=settings.app_name, version="1.0.0", description="Asynchronous bulk PDF certificate generation API")
app.include_router(jobs.router); app.include_router(certificates.router)
@app.get("/health", tags=["health"])
def health():
    with SessionLocal() as db: db.execute(text("SELECT 1"))
    return {"status": "ok"}
