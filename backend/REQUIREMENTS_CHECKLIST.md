# Requirements checklist

- [x] FastAPI, Pydantic, SQLAlchemy 2, SQLite, Alembic, ReportLab, pytest/TestClient
- [x] Versioned create/status/results/download endpoints and health check
- [x] Batch, date, name, email, duplicate, and identifier validation
- [x] Persisted job and recipient state with derived progress
- [x] Per-recipient failure isolation and atomic temporary PDF replacement
- [x] Safe identifier-only file retrieval and no static file mount
- [x] Migration, isolated tests, README, configuration
- [x] Honest in-process BackgroundTasks durability limitation
- [ ] Authentication/authorization (explicitly out of scope)
- [ ] Durable queue/restart recovery (future production enhancement)
- [ ] Idempotency keys (limitation documented)
