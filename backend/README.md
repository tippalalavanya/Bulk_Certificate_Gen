# Bulk Certificate Generator API

Interview-ready FastAPI service that accepts a validated batch, persists job/recipient state in SQLite, and generates one ReportLab PDF per successful recipient.

## Run

Python 3.11+ is supported (tested with 3.13). From `backend/`:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
pytest -q
```

Swagger: `http://127.0.0.1:8000/docs`. Copy `.env.example` to `.env` to configure `DATABASE_URL`, `STORAGE_DIR`, `ORGANIZATION_NAME`, `CERTIFICATE_FOOTER`, and `MAX_BATCH_SIZE`.

## API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/certificate-jobs -H 'content-type: application/json' -d '{"coursename":"Python Backend Development","issuedate":"2026-10-10","recipients":[{"name":"Aarav Sharma","email":"aarav@example.com"}]}'
curl http://127.0.0.1:8000/api/v1/certificate-jobs/JOB_ID
curl 'http://127.0.0.1:8000/api/v1/certificate-jobs/JOB_ID/results?limit=50'
curl -OJ http://127.0.0.1:8000/api/v1/certificates/CERTIFICATE_ID
```

POST returns 202: processing is executed with FastAPI `BackgroundTasks`, which is not a durable queue. A process crash can lose accepted work; use a durable worker/queue and stronger database for production. Certificates are not authenticated in this sample; protect the API before deploying private certificates.

Jobs: `queued -> processing -> completed|completed_with_errors|failed`. Recipients: `pending -> processing -> completed|failed`. Progress is persisted terminal recipients divided by total, rounded to two decimals. Duplicate normalized emails are rejected. Errors use `{code, message}` details and never expose paths or stack traces.

## Architecture

Routes handle HTTP contracts; services own processing and atomic PDF writes; SQLAlchemy models persist a job-to-many-recipient relationship. Each recipient is committed after entering processing and after success/failure, so one recipient failure does not erase another. PDFs use identifier-based filenames and are resolved beneath the configured storage directory.

## Migrations and limitations

Alembic migration `0001_initial` is the source of schema truth. No authentication, idempotency key, template editor, retry worker, or email delivery is implemented. Future production work should add authentication/authorization, idempotency, durable queueing, metrics, and a Unicode font asset strategy.
