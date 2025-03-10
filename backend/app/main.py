from fastapi import FastAPI, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
from pathlib import Path
import json
import os
from typing import List, Optional, Dict
from pydantic import BaseModel
from app.config.settings import get_settings

# 获取配置
settings = get_settings()

# 配置项
BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")
STATIC_PATH = "/static"  # 静态资源路径前缀

# 定义目标路径常量
TARGET_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/mock')

app = FastAPI(title="漫画阅读API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # 使用settings中的配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录 - 使用目标路径常量
static_dir = TARGET_DIR
print(f"静态文件目录: {static_dir.absolute()}")
static_dir.mkdir(parents=True, exist_ok=True)
app.mount(STATIC_PATH, StaticFiles(directory=str(static_dir)), name="static")

# 下载脚本路径
download_script = Path(__file__).parent / "download_and_process.py"

# 定义数据模型
class Page(BaseModel):
    id: str
    chapterId: str
    order: int
    url: str

class Chapter(BaseModel):
    id: str
    comicId: str
    title: str
    order: int
    updateTime: str
    pageCount: int
    cover: Optional[str] = None

class Comic(BaseModel):
    id: str
    title: str
    cover: str
    author: str
    description: str
    tags: List[str]
    updateTime: str
    status: str
    chapters: Optional[List[Chapter]] = None

class PaginatedResult(BaseModel):
    items: List[Comic]
    total: int
    page: int
    pageSize: int
    hasMore: bool

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"广播消息时出错: {e}")

manager = ConnectionManager()

# 创建API路由前缀
api_router = FastAPI()

async def notify_clients(action: str, comic_id: str = None):
    """通知所有连接的客户端数据已更新"""
    message = {
        "action": action,
        "comic_id": comic_id
    }
    await manager.broadcast(message)

def download_comic_task(comic_id: str):
    """后台任务：下载漫画"""
    try:
        print(f"开始下载漫画 {comic_id}...")
        print(f"下载脚本路径: {download_script.absolute()}")
        
        if not download_script.exists():
            print(f"错误: 下载脚本不存在: {download_script.absolute()}")
            return
        
        # 准备环境变量
        env = os.environ.copy()
        # 确保BASE_URL被正确传递
        env["BASE_URL"] = BASE_URL
        print(f"传递给下载脚本的BASE_URL: {BASE_URL}")
        
        # 执行下载脚本
        result = subprocess.run(
            ["python3", str(download_script.absolute()), comic_id], 
            check=False,
            capture_output=True,
            text=True,
            env=env  # 传递环境变量
        )
        
        if result.returncode != 0:
            print(f"下载脚本执行失败，返回码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
        else:
            print(f"下载脚本执行成功: {result.stdout}")
            # 下载完成后通知客户端
            import asyncio
            asyncio.run(notify_clients("comic_added", comic_id))
    except Exception as e:
        print(f"下载漫画 {comic_id} 时出错: {e}")
        import traceback
        traceback.print_exc()

@app.get("/")
async def root():
    return {
        "message": "漫画阅读API服务正在运行",
        "api_docs": f"{BASE_URL}/docs",
        "endpoints": {
            "api_root": f"{BASE_URL}/api",
            "static_files": f"{BASE_URL}/static",
            "websocket": f"{BASE_URL}/ws",
            "download": f"{BASE_URL}/download"
        }
    }

@api_router.get("/")
def read_root():
    return {"message": "漫画阅读API"}

@api_router.get("/download/{comic_id}")
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

@app.get("/download/{comic_id}")
async def root_download_comic(comic_id: str, background_tasks: BackgroundTasks):
    """根路径下的下载漫画API，重定向到/api/download/{comic_id}"""
    return await download_comic(comic_id, background_tasks)

@api_router.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"}

# 新增API：获取漫画列表
@api_router.get("/comics", response_model=PaginatedResult)
def get_comics(page: int = 1, pageSize: int = 20):
    """获取漫画列表"""
    try:
        comics_file = TARGET_DIR / "comics.json"
        if not comics_file.exists():
            return PaginatedResult(items=[], total=0, page=page, pageSize=pageSize, hasMore=False)
        
        with open(comics_file, "r", encoding="utf-8") as f:
            comics = json.load(f)
        
        # 处理封面URL
        for comic in comics:
            if comic.get("cover") and not comic["cover"].startswith(("http://", "https://")):
                comic["cover"] = get_static_url(comic["cover"])
        
        # 计算分页
        start = (page - 1) * pageSize
        end = start + pageSize
        paginated_comics = comics[start:end]
        
        return PaginatedResult(
            items=paginated_comics,
            total=len(comics),
            page=page,
            pageSize=pageSize,
            hasMore=end < len(comics)
        )
    except Exception as e:
        print(f"获取漫画列表出错: {e}")
        return PaginatedResult(items=[], total=0, page=page, pageSize=pageSize, hasMore=False)

# 新增API：搜索漫画
@api_router.get("/comics/search", response_model=PaginatedResult)
def search_comics(keyword: str = "", page: int = 1, pageSize: int = 20):
    """搜索漫画"""
    try:
        comics_file = TARGET_DIR / "comics.json"
        if not comics_file.exists():
            return PaginatedResult(items=[], total=0, page=page, pageSize=pageSize, hasMore=False)
        
        with open(comics_file, "r", encoding="utf-8") as f:
            comics = json.load(f)
        
        # 处理封面URL
        for comic in comics:
            if comic.get("cover") and not comic["cover"].startswith(("http://", "https://")):
                comic["cover"] = get_static_url(comic["cover"])
        
        # 如果有关键词，进行过滤
        if keyword:
            filtered_comics = [
                c for c in comics 
                if keyword.lower() in c["title"].lower() or 
                   keyword.lower() in c["description"].lower() or
                   any(keyword.lower() in tag.lower() for tag in c["tags"])
            ]
        else:
            filtered_comics = comics
        
        # 计算分页
        start = (page - 1) * pageSize
        end = start + pageSize
        paginated_comics = filtered_comics[start:end]
        
        return PaginatedResult(
            items=paginated_comics,
            total=len(filtered_comics),
            page=page,
            pageSize=pageSize,
            hasMore=end < len(filtered_comics)
        )
    except Exception as e:
        print(f"搜索漫画出错: {e}")
        return PaginatedResult(items=[], total=0, page=page, pageSize=pageSize, hasMore=False)

# 新增API：获取最新漫画
@api_router.get("/comics/latest", response_model=List[Comic])
def get_latest_comics(limit: int = 10):
    """获取最新更新的漫画"""
    try:
        comics_file = TARGET_DIR / "comics.json"
        if not comics_file.exists():
            return []
        
        with open(comics_file, "r", encoding="utf-8") as f:
            comics = json.load(f)
        
        # 处理封面URL
        for comic in comics:
            if comic.get("cover") and not comic["cover"].startswith(("http://", "https://")):
                comic["cover"] = get_static_url(comic["cover"])
        
        # 按更新时间排序
        sorted_comics = sorted(
            comics, 
            key=lambda c: c.get("updateTime", ""), 
            reverse=True
        )
        
        # 返回指定数量
        return sorted_comics[:limit]
    except Exception as e:
        print(f"获取最新漫画出错: {e}")
        return []

# 新增API：获取推荐漫画
@api_router.get("/comics/recommended", response_model=List[Comic])
def get_recommended_comics(limit: int = 6):
    """获取推荐漫画"""
    try:
        comics_file = TARGET_DIR / "comics.json"
        if not comics_file.exists():
            return []
        
        with open(comics_file, "r", encoding="utf-8") as f:
            comics = json.load(f)
        
        # 处理封面URL
        for comic in comics:
            if comic.get("cover") and not comic["cover"].startswith(("http://", "https://")):
                comic["cover"] = get_static_url(comic["cover"])
        
        # 随机打乱顺序
        import random
        shuffled_comics = list(comics)
        random.shuffle(shuffled_comics)
        
        # 返回指定数量
        return shuffled_comics[:limit]
    except Exception as e:
        print(f"获取推荐漫画出错: {e}")
        return []

# 新增API：获取漫画详情
@api_router.get("/comics/{comic_id}", response_model=Optional[Comic])
def get_comic_detail(comic_id: str):
    """获取漫画详情"""
    try:
        # 读取漫画列表
        comics_file = TARGET_DIR / "comics.json"
        if not comics_file.exists():
            raise HTTPException(status_code=404, detail="漫画列表不存在")
        
        with open(comics_file, "r", encoding="utf-8") as f:
            comics = json.load(f)
        
        # 查找指定ID的漫画
        comic = next((c for c in comics if c["id"] == comic_id), None)
        if not comic:
            raise HTTPException(status_code=404, detail=f"找不到ID为{comic_id}的漫画")
        
        # 处理封面URL
        if comic.get("cover") and not comic["cover"].startswith(("http://", "https://")):
            comic["cover"] = get_static_url(comic["cover"])
        
        # 读取章节列表
        chapters_file = TARGET_DIR / "chapters.json"
        if chapters_file.exists():
            with open(chapters_file, "r", encoding="utf-8") as f:
                all_chapters = json.load(f)
            
            # 过滤出属于该漫画的章节
            comic_chapters = [ch for ch in all_chapters if ch["comicId"] == comic_id]
            
            # 处理章节封面URL
            for chapter in comic_chapters:
                if chapter.get("cover") and not chapter["cover"].startswith(("http://", "https://")):
                    chapter["cover"] = get_static_url(chapter["cover"])
            
            comic["chapters"] = comic_chapters
        
        return comic
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取漫画详情出错: {e}")
        raise HTTPException(status_code=500, detail=f"获取漫画详情出错: {str(e)}")

# 新增API：获取章节页面
@api_router.get("/chapters/{chapter_id}/pages", response_model=List[Page])
def get_chapter_pages(chapter_id: str):
    """获取章节页面"""
    try:
        # 解析章节ID，获取漫画ID
        parts = chapter_id.split("-")
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="无效的章节ID格式")
        
        comic_id, chapter_order = parts
        
        # 读取章节信息
        chapters_file = TARGET_DIR / "chapters.json"
        if not chapters_file.exists():
            raise HTTPException(status_code=404, detail="章节列表不存在")
        
        with open(chapters_file, "r", encoding="utf-8") as f:
            chapters = json.load(f)
        
        # 查找指定ID的章节
        chapter = next((ch for ch in chapters if ch["id"] == chapter_id), None)
        if not chapter:
            raise HTTPException(status_code=404, detail=f"找不到ID为{chapter_id}的章节")
        
        # 生成页面数据
        page_count = chapter.get("pageCount", 0)
        pages = []
        
        for i in range(1, page_count + 1):
            padded_num = f"{i:05d}"
            # 使用辅助函数生成URL
            url = get_static_url(f"{comic_id}/{padded_num}.webp")
            
            pages.append({
                "id": f"{chapter_id}-{i}",
                "chapterId": chapter_id,
                "order": i,
                "url": url
            })
        
        return pages
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取章节页面出错: {e}")
        raise HTTPException(status_code=500, detail=f"获取章节页面出错: {str(e)}")

# 删除漫画API
@api_router.delete("/comics/{comic_id}")
async def delete_comic(comic_id: str):
    """删除漫画"""
    try:
        # 读取漫画列表
        comics_file = TARGET_DIR / "comics.json"
        if not comics_file.exists():
            raise HTTPException(status_code=404, detail="漫画列表不存在")
        
        with open(comics_file, "r", encoding="utf-8") as f:
            comics = json.load(f)
        
        # 查找并删除指定ID的漫画
        comics = [c for c in comics if c["id"] != comic_id]
        
        # 保存更新后的漫画列表
        with open(comics_file, "w", encoding="utf-8") as f:
            json.dump(comics, f, ensure_ascii=False, indent=2)
        
        # 读取章节列表
        chapters_file = TARGET_DIR / "chapters.json"
        if chapters_file.exists():
            with open(chapters_file, "r", encoding="utf-8") as f:
                chapters = json.load(f)
            
            # 过滤出不属于该漫画的章节
            chapters = [ch for ch in chapters if ch["comicId"] != comic_id]
            
            # 保存更新后的章节列表
            with open(chapters_file, "w", encoding="utf-8") as f:
                json.dump(chapters, f, ensure_ascii=False, indent=2)
        
        # 删除漫画目录
        comic_dir = TARGET_DIR / comic_id
        if comic_dir.exists():
            import shutil
            shutil.rmtree(comic_dir)
        
        # 通知客户端
        await notify_clients("comic_deleted", comic_id)
        
        return {"message": f"漫画 {comic_id} 已成功删除"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"删除漫画出错: {e}")
        raise HTTPException(status_code=500, detail=f"删除漫画出错: {str(e)}")

# WebSocket连接
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        print(f"WebSocket客户端已连接")
        try:
            while True:
                # 等待消息，但我们不处理客户端消息
                data = await websocket.receive_text()
                print(f"收到WebSocket消息: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            print(f"WebSocket客户端已断开连接")
    except Exception as e:
        print(f"WebSocket处理出错: {e}")
        if websocket in manager.active_connections:
            manager.disconnect(websocket)

# 将API路由挂载到主应用，添加/api前缀
app.mount("/api", api_router)

# 辅助函数：生成静态资源URL
def get_static_url(path: str) -> str:
    """生成静态资源的完整URL"""
    # 确保path不以/开头
    if path.startswith('/'):
        path = path[1:]
    return f"{BASE_URL}{STATIC_PATH}/{path}"
