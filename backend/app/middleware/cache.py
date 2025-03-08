from fastapi import Request, Response
import hashlib
from typing import Dict, Any
import time
import logging
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# 使用内存缓存（生产环境应该使用Redis）
cache_store: Dict[str, Any] = {}

def get_cache_key(request: Request) -> str:
    """生成缓存键"""
    # 使用请求方法、路径和查询参数生成缓存键
    content = f"{request.method}:{request.url.path}:{str(request.query_params)}"
    return hashlib.md5(content.encode()).hexdigest()

async def cache_middleware(request: Request, call_next):
    """缓存中间件"""
    if not settings.cache_enabled:
        return await call_next(request)
    
    # 只缓存GET请求
    if request.method != "GET":
        return await call_next(request)
    
    cache_key = get_cache_key(request)
    current_time = time.time()
    
    # 检查缓存
    if cache_key in cache_store:
        cached_data = cache_store[cache_key]
        if current_time - cached_data["timestamp"] < settings.cache_ttl:
            logger.debug(f"从缓存返回数据: {cache_key}")
            return Response(
                content=cached_data["content"],
                media_type="application/json",
                headers=cached_data["headers"]
            )
    
    # 执行请求
    response = await call_next(request)
    
    # 缓存响应
    if response.status_code == 200:
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        cache_store[cache_key] = {
            "content": response_body,
            "headers": dict(response.headers),
            "timestamp": current_time
        }
        
        return Response(
            content=response_body,
            media_type=response.media_type,
            headers=dict(response.headers),
            status_code=response.status_code
        )
    
    return response 