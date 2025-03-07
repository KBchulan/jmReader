from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path
from typing import List, Set

class Settings(BaseSettings):
    # 基本配置
    debug: bool = False
    log_level: str = "info"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 3000
    
    # MongoDB配置
    mongo_uri: str = "mongodb://localhost:27017/comic_db"
    
    # 漫画下载配置
    download_path: str = "./downloads"
    download_timeout: int = 120
    max_concurrent_downloads: int = 3
    
    # JWT配置
    jwt_secret: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expires_in: str = "7d"
    
    # 跨域配置
    cors_origins: List[str] = ["http://localhost:5173"]
    
    # 缓存配置
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 缓存时间，单位秒
    
    # 图片处理配置
    image_quality: int = 85
    image_max_size: int = 5242880  # 5MB
    allowed_image_types: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # 限流配置
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100  # 每个IP每分钟最大请求数
    
    # 安全配置
    security_enabled: bool = True
    max_request_size: int = 10485760  # 10MB
    
    class Config:
        env_file = os.getenv("ENV_FILE", ".env.development")
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（使用缓存）"""
    return Settings() 