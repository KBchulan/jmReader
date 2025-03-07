from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path
from typing import List, Set, Optional

class Settings(BaseSettings):
    # 基本配置
    debug: bool = False
    log_level: str = "info"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 3000
    
    # 跨域配置
    cors_origins: List[str] = ["http://localhost:5173"]
    
    # 缓存配置
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 缓存时间，单位秒
    
    # 限流配置
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100  # 每个IP每分钟最大请求数
    
    # 安全配置
    security_enabled: bool = True
    max_request_size: int = 10485760  # 10MB
    
    # 漫画下载配置
    download_path: Optional[str] = None
    download_timeout: Optional[int] = None
    max_concurrent_downloads: Optional[int] = None
    
    # JWT配置
    jwt_secret: Optional[str] = None
    jwt_algorithm: Optional[str] = None
    jwt_expires_in: Optional[str] = None
    
    # 图片处理配置
    image_quality: Optional[int] = None
    image_max_size: Optional[int] = None
    allowed_image_types: Optional[List[str]] = None
    
    class Config:
        env_file = os.getenv("ENV_FILE", ".env.development")
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # 忽略额外的配置项

@lru_cache()
def get_settings():
    return Settings() 