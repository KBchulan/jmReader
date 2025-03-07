from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import logging
from pathlib import Path

from app.routes import comics, search, chapters
from app.config.settings import get_settings
from app.middleware import rate_limit_middleware, cache_middleware, security_middleware

# 获取配置
settings = get_settings()

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="漫画阅读API",
    description="漫画阅读网站的后端API",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加自定义中间件
app.middleware("http")(security_middleware)  # 安全中间件应该最先执行
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(cache_middleware)

# 注册路由
app.include_router(comics.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(chapters.router, prefix="/api")

# 确保mock_data目录存在
mock_data_path = Path("./mock_data")
mock_data_path.mkdir(parents=True, exist_ok=True)

# 挂载静态文件目录（用于提供漫画图片）
app.mount("/api/static", StaticFiles(directory=str(mock_data_path)), name="static")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误", "success": False},
    )

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info("应用启动完成")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用已关闭")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    ) 