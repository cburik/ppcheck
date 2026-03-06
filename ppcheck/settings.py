from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ppcheck_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # app settings
    app_home: Path = Field(default=Path.home() / ".ppcheck", description="Application home directory")
    db_loc: Path = Field(default=Path.home() / ".ppcheck" / "ppcheck.db", description="Database file location")
    api_url: str = Field(default="https://api.pwnedpasswords.com/range", description="HIBP API URL")

    # Encryption settings
    pbkdf2_iterations: int = Field(default=200_000, description="PBKDF2 KDF iterations")
    master_password: Optional[str] = Field(default=None, description="Master password for encryption")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
