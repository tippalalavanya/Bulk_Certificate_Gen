import logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.job import Job
from app.models.recipient import RecipientResult
from app.services.certificate_service import CertificateService

logger = logging.getLogger(__name__)
ALLOWED_JOB_TRANSITIONS = {"queued": {"processing", "failed"}, "processing": {"completed", "completed_with_errors", "failed"}}
ALLOWED_RECIPIENT_TRANSITIONS = {"pending": {"processing"}, "processing": {"completed", "failed"}}

def transition(current: str, target: str, allowed: dict[str, set[str]]) -> None:
    if target not in allowed.get(current, set()): raise ValueError(f"invalid state transition: {current} -> {target}")

def process_job(job_id: str, session_factory, certificate_service: CertificateService | None = None) -> None:
    db: Session = session_factory(); service = certificate_service or CertificateService()
    try:
        job = db.get(Job, job_id)
        if not job: return
        transition(job.status, "processing", ALLOWED_JOB_TRANSITIONS); job.status = "processing"; job.started_at = datetime.now(timezone.utc); db.commit()
        for recipient in db.scalars(select(RecipientResult).where(RecipientResult.job_id == job_id, RecipientResult.status == "pending")).all():
            now = datetime.now(timezone.utc); transition(recipient.status, "processing", ALLOWED_RECIPIENT_TRANSITIONS); recipient.status = "processing"; recipient.started_at = now; db.commit()
            try:
                cert_id, key = service.generate(name=recipient.name, course_name=job.course_name, issue_date=job.issue_date.isoformat(), organization=settings.organization_name, footer=settings.certificate_footer)
                recipient.certificate_id = cert_id; recipient.storage_key = key; recipient.status = "completed"; recipient.completed_at = datetime.now(timezone.utc); db.commit()
                logger.info("recipient_completed job_id=%s result_id=%s", job.id, recipient.id)
            except Exception:
                db.rollback(); recipient = db.get(RecipientResult, recipient.id); recipient.status = "failed"; recipient.failure_code = "GENERATION_FAILED"; recipient.failure_message = "Certificate generation failed"; recipient.completed_at = datetime.now(timezone.utc); db.commit(); logger.exception("recipient_failed job_id=%s result_id=%s", job.id, recipient.id)
        db.refresh(job); statuses = [r.status for r in job.recipients]
        target = "completed" if all(s == "completed" for s in statuses) else "completed_with_errors" if any(s == "completed" for s in statuses) else "failed"
        transition(job.status, target, ALLOWED_JOB_TRANSITIONS); job.status = target; job.completed_at = datetime.now(timezone.utc); db.commit(); logger.info("job_completed job_id=%s status=%s", job.id, target)
    except Exception:
        db.rollback(); job = db.get(Job, job_id)
        if job and job.status == "processing": job.status = "failed"; job.completed_at = datetime.now(timezone.utc); db.commit()
        logger.exception("job_failed job_id=%s", job_id)
    finally: db.close()
