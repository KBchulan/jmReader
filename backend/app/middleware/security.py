from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

async def security_middleware(request: Request, call_next):
    """安全中间件"""
    if not settings.security_enabled:
        return await call_next(request)
    
    # 检查请求大小
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.max_request_size:
        logger.warning(f"请求大小超过限制: {content_length} bytes")
        return JSONResponse(
            status_code=413,
            content={
                "message": "请求大小超过限制",
                "success": False
            }
        )
    
    # 检查文件上传类型（如果有）
    if request.headers.get("content-type", "").startswith("multipart/form-data"):
        form = await request.form()
        for field in form:
            if hasattr(field, "content_type") and field.content_type not in settings.allowed_image_types:
                logger.warning(f"不支持的文件类型: {field.content_type}")
                return JSONResponse(
                    status_code=415,
                    content={
                        "message": "不支持的文件类型",
                        "success": False
                    }
                )
    
    # 添加安全响应头
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response 