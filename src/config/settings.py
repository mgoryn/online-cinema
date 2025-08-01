# src/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Base settings, provides common configurations."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BASE_DIR: Path = Path(__file__).parent.parent.parent

    # Paths to email templates
    PATH_TO_EMAIL_TEMPLATES_DIR: Path = BASE_DIR / "notifications" / "templates"
    ACTIVATION_EMAIL_TEMPLATE_NAME: str = "activation_request.html"
    PASSWORD_RESET_TEMPLATE_NAME: str = "password_reset_request.html"

    # Common application settings
    LOGIN_TIME_DAYS: int = 7


class AppSettings(BaseAppSettings):
    """Main application settings for Development/Production."""

    # PostgreSQL settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_DB_PORT: int

    # JWT settings
    # IMPORTANT: These must be set in the .env file for production
    SECRET_KEY_ACCESS: str
    SECRET_KEY_REFRESH: str
    JWT_SIGNING_ALGORITHM: str

    # Email settings from .env
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_USE_TLS: bool

    # MinIO (S3) settings from .env
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_STORAGE: str

    @property
    def database_url(self) -> str:
        """Constructs PostgreSQL connection string."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def s3_storage_endpoint(self) -> str:
        """Constructs S3 storage endpoint URL."""
        return f"http://{self.MINIO_HOST}:{self.MINIO_PORT}"


class TestSettings(BaseAppSettings):
    """Settings for testing purposes."""

    # Use a fast in-memory SQLite database for tests
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    # Fixed keys for predictable test results
    SECRET_KEY_ACCESS: str = "test_secret_key_access"
    SECRET_KEY_REFRESH: str = "test_secret_key_refresh"
    JWT_SIGNING_ALGORITHM: str = "HS256"


# Instantiate the main settings
settings = AppSettings()
