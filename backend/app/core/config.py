from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "Bulk Certificate Generator"
    database_url: str = f"sqlite:///{BASE_DIR / 'certificates.db'}"
    storage_dir: Path = BASE_DIR / "generated_certificates"
    organization_name: str = "Example Academy"
    certificate_footer: str = "Presented for successful completion"
    max_batch_size: int = 100
    background_processing: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def ensure_storage(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
