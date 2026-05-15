from pathlib import Path
from typing import List
from pydantic import AnyUrl
from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    database_url: str
    cors_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
