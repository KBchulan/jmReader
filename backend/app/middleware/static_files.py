"""静态文件中间件"""
import logging
from fastapi import Request
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

async def static_files_middleware(request: Request, call_next):
    """处理静态文件的中间件，添加适当的响应头"""
    response = await call_next(request)

    if request.url.path.startswith(settings.STATIC_PATH):
        logger.debug(f"处理静态文件请求: {request.url.path}")

        response.headers["Cache-Control"] = "public, max-age=86400"

        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"

        if "content-type" not in response.headers:
            path = request.url.path.lower()
            if path.endswith(".jpg") or path.endswith(".jpeg"):
                response.headers["content-type"] = "image/jpeg"
            elif path.endswith(".png"):
                response.headers["content-type"] = "image/png"
            elif path.endswith(".webp"):
                response.headers["content-type"] = "image/webp"
            elif path.endswith(".gif"):
                response.headers["content-type"] = "image/gif"

    return response