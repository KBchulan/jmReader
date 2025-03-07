from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import os
from pathlib import Path

app = FastAPI(title="简化版漫画下载API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = Path("../src/assets/mock")
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 下载脚本路径
download_script = Path(__file__).parent / "download_and_process.py"

def download_comic_task(comic_id: str):
    """后台任务：下载漫画"""
    try:
        # 执行下载脚本
        subprocess.run(["python3", str(download_script), comic_id], check=True)
    except Exception as e:
        print(f"下载漫画 {comic_id} 时出错: {e}")

@app.get("/")
def read_root():
    return {"message": "简化版漫画下载API"}

@app.get("/download/{comic_id}")
async def download_comic(comic_id: str, background_tasks: BackgroundTasks):
    """下载漫画API"""
    # 验证漫画ID是否为6位数字
    if not comic_id.isdigit() or len(comic_id) != 6:
        raise HTTPException(status_code=400, detail="漫画ID必须是6位数字")
    
    # 检查下载脚本是否存在
    if not download_script.exists():
        raise HTTPException(status_code=500, detail="下载脚本不存在")
    
    # 将下载任务添加到后台任务
    background_tasks.add_task(download_comic_task, comic_id)
    
    return {"message": f"已开始下载漫画 {comic_id}，请稍后刷新页面查看"}

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"} 