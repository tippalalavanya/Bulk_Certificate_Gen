from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.recipient import RecipientResult

router = APIRouter(prefix="/api/v1/certificates", tags=["certificates"])
@router.get("/{certificate_id}")
def download_certificate(certificate_id: str, db: Session = Depends(get_db)):
    result = db.query(RecipientResult).filter(RecipientResult.certificate_id == certificate_id, RecipientResult.status == "completed").first()
    if not result: raise HTTPException(404, detail={"code":"CERTIFICATE_NOT_FOUND", "message":"certificate not found"})
    storage = settings.storage_dir.resolve(); path = (storage / (result.storage_key or "")).resolve()
    if path.parent != storage or path.suffix.lower() != ".pdf" or not path.is_file(): raise HTTPException(404, detail={"code":"CERTIFICATE_FILE_NOT_FOUND", "message":"certificate file not found"})
    return FileResponse(path, media_type="application/pdf", filename=f"certificate-{certificate_id}.pdf")
