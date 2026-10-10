import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_model import Base
from app.db.session import get_db
from app.main import app
from app.core import config

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", connect_args={"check_same_thread":False})
    Base.metadata.create_all(db_engine); Session = sessionmaker(bind=db_engine, expire_on_commit=False)
    storage = tmp_path / "certificates"; storage.mkdir()
    monkeypatch.setattr(config.settings, "storage_dir", storage)
    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr("app.api.routes.jobs.SessionLocal", Session)
    with TestClient(app) as test_client: yield test_client
    app.dependency_overrides.clear(); Base.metadata.drop_all(db_engine)
