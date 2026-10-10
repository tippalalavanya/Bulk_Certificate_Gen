from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal, get_db
from app.models.job import Job
from app.models.recipient import RecipientResult
from app.schemas.job import JobCreate, JobResponse, RecipientResponse, ResultsResponse
from app.services.processing_service import process_job
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/certificate-jobs", tags=["certificate-jobs"])
def response_for(job: Job, request: Request) -> JobResponse:
    counts = {s: sum(1 for r in job.recipients if r.status == s) for s in ("completed", "failed", "pending", "processing")}
    total = len(job.recipients); progress = round((counts["completed"] + counts["failed"]) * 100 / total, 2) if total else 0
    return JobResponse(job_id=job.id, status=job.status, created_at=job.created_at, started_at=job.started_at, completed_at=job.completed_at, total_count=total, successful_count=counts["completed"], failed_count=counts["failed"], pending_count=counts["pending"], processing_count=counts["processing"], progress_percentage=progress, results_url=str(request.url_for("list_results", job_id=job.id)))

@router.post("", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
def create_job(payload: JobCreate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if len(payload.recipients) > settings.max_batch_size: raise HTTPException(413, detail={"code":"BATCH_TOO_LARGE", "message":f"maximum batch size is {settings.max_batch_size}"})
    emails = [str(r.email).lower() for r in payload.recipients]
    if len(emails) != len(set(emails)): raise HTTPException(422, detail={"code":"DUPLICATE_RECIPIENT", "message":"recipient emails must be unique within a job"})
    now = datetime.now(timezone.utc); job = Job(course_name=payload.course_name, issue_date=payload.issue_date, created_at=now)
    job.recipients = [RecipientResult(name=r.name, email=str(r.email).lower(), created_at=now) for r in payload.recipients]
    db.add(job); db.commit(); db.refresh(job)
    background_tasks.add_task(process_job, job.id, SessionLocal)
    return response_for(job, request)

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, request: Request, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job: raise HTTPException(404, detail={"code":"JOB_NOT_FOUND", "message":"job not found"})
    return response_for(job, request)

@router.get("/{job_id}/results", response_model=ResultsResponse, name="list_results")
def list_results(job_id: str, offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    if not db.get(Job, job_id): raise HTTPException(404, detail={"code":"JOB_NOT_FOUND", "message":"job not found"})
    total = db.scalar(select(func.count()).select_from(RecipientResult).where(RecipientResult.job_id == job_id)) or 0
    rows = db.scalars(select(RecipientResult).where(RecipientResult.job_id == job_id).order_by(RecipientResult.created_at).offset(offset).limit(limit)).all()
    return ResultsResponse(items=[RecipientResponse(result_id=r.id, name=r.name, status=r.status, certificate_id=r.certificate_id, failure_code=r.failure_code, failure_message=r.failure_message) for r in rows], total=total, offset=offset, limit=limit)
