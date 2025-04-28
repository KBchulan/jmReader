from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path
from typing import List, Optional

class Settings(BaseSettings):
    debug: bool = False
    log_level: str = "info"

    host: str = "0.0.0.0"
    port: int = 3000

    BASE_URL: str = os.environ.get("BASE_URL", "http://localhost:3000")
    STATIC_PATH: str = "/static"
    TARGET_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'mock')

    cors_origins: List[str] = ["http://0.0.0.0:5173", "http://localhost:5173", "*"]

    cache_enabled: bool = True
    cache_ttl: int = 3600

    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100

    security_enabled: bool = True
    max_request_size: int = 10485760 * 3

    download_path: Optional[str] = None
    download_timeout: Optional[int] = None
    max_concurrent_downloads: Optional[int] = None

    jwt_secret: Optional[str] = None
    jwt_algorithm: Optional[str] = None
    jwt_expires_in: Optional[str] = None

    image_quality: Optional[int] = None
    image_max_size: Optional[int] = None
    allowed_image_types: Optional[List[str]] = None

    class Config:
        env_file = os.getenv("ENV_FILE", ".env.development")
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()