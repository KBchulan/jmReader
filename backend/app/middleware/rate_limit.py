from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
import logging
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# 使用内存存储请求计数（生产环境应该使用Redis）
request_counts = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    """限流中间件"""
    if not settings.rate_limit_enabled:
        return await call_next(request)
    
    # 获取客户端IP
    client_ip = request.client.host
    current_time = time.time()
    
    # 清理过期的请求记录（1分钟前的记录）
    request_counts[client_ip] = [t for t in request_counts[client_ip] if current_time - t < 60]
    
    # 检查请求次数是否超过限制
    if len(request_counts[client_ip]) >= settings.rate_limit_requests:
        logger.warning(f"IP {client_ip} 请求频率超过限制")
        return JSONResponse(
            status_code=429,
            content={
                "message": "请求频率过高，请稍后再试",
                "success": False
            }
        )
    
    # 记录当前请求
    request_counts[client_ip].append(current_time)
    
    return await call_next(request) 