# Assumptions and decisions

- One fixed certificate template and local PDF storage are sufficient for local/interview workloads.
- Email is required for recipient identity and is normalized to lowercase.
- Duplicate normalized email addresses in one request reject the entire request.
- FastAPI BackgroundTasks is intentionally used: simple and dependency-free, but not durable.
- No authentication is included because it was not requested; private deployments must add it.
- Job creation is not idempotent; clients should not assume retries return the same job.
- Failed recipients are recorded and remaining recipients continue.
- SQLite is the default, with migration files as schema authority.
