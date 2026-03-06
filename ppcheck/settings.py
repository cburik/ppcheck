from functools import lru_cache
from pathlib import Path
from typing import Optional

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
    app_home: Path = Path.home() / ".ppcheck"
    db_loc: Path = Path.home() / ".ppcheck" / "ppcheck.db"
    api_url: str = "https://api.pwnedpasswords.com/range"

    # Encryption settings
    field_iterations: int = 200_000
    master_iterations: int = 2_000_000
    master_password: Optional[str] = None
    master_salt_loc: Path = Path.home() / ".ppcheck" / "salt.bin"
    magic_string: str = "it's magic"
    magic_file: Path = Path.home() / ".ppcheck" / "magic.bin"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
