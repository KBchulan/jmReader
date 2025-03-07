import logging
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from bson.objectid import ObjectId
from jmcomic import JmcomicClient
import os
from pathlib import Path

from app.db.mongodb import mongodb
from app.models.comic import Comic, Chapter, Page, PaginatedResult, ComicInDB
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ComicService:
    """漫画服务"""
    
    def __init__(self):
        self.db = mongodb.db
        self.jm_client = JmcomicClient()
        self.download_path = Path(settings.download_path)
        self.download_path.mkdir(parents=True, exist_ok=True)
    
    async def get_comics(self, page: int = 1, page_size: int = 20) -> PaginatedResult:
        """获取漫画列表"""
        skip = (page - 1) * page_size
        
        # 查询总数
        total = await self.db.comics.count_documents({})
        
        # 查询漫画列表
        cursor = self.db.comics.find().sort("updated_at", -1).skip(skip).limit(page_size)
        comics = []
        
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            comics.append(Comic(**doc))
        
        return PaginatedResult(
            items=comics,
            total=total,
            page=page,
            page_size=page_size,
            has_more=total > skip + len(comics)
        )
    
    async def get_comic_detail(self, comic_id: str) -> Optional[Comic]:
        """获取漫画详情"""
        # 尝试从数据库获取
        doc = await self.db.comics.find_one({"_id": ObjectId(comic_id)})
        
        if doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            
            # 获取章节信息
            chapters_cursor = self.db.chapters.find({"comic_id": comic_id}).sort("order", 1)
            chapters = []
            
            async for chapter_doc in chapters_cursor:
                chapter_doc["id"] = str(chapter_doc["_id"])
                del chapter_doc["_id"]
                chapters.append(Chapter(**chapter_doc))
            
            doc["chapters"] = chapters
            return Comic(**doc)
        
        # 如果数据库中没有，尝试从JM漫画获取
        try:
            # 假设comic_id是JM漫画的ID
            jm_comic = await self.jm_client.get_album_detail(comic_id)
            
            if jm_comic:
                # 转换为我们的模型
                comic = Comic(
                    id=str(ObjectId()),
                    title=jm_comic.name,
                    cover=jm_comic.cover_url,
                    author=jm_comic.author or "未知",
                    description=jm_comic.description or "",
                    tags=jm_comic.tags,
                    update_time=datetime.now(),
                    status="ongoing",
                    chapters=[]
                )
                
                # 保存到数据库
                comic_in_db = ComicInDB(**comic.dict())
                result = await self.db.comics.insert_one(comic_in_db.dict(exclude={"id", "chapters"}))
                
                # 处理章节
                chapters = []
                for i, jm_chapter in enumerate(jm_comic.chapters):
                    chapter = Chapter(
                        id=str(ObjectId()),
                        comic_id=str(result.inserted_id),
                        title=jm_chapter.name,
                        order=i + 1,
                        update_time=datetime.now(),
                        page_count=jm_chapter.page_count
                    )
                    chapters.append(chapter)
                    await self.db.chapters.insert_one(chapter.dict())
                
                comic.id = str(result.inserted_id)
                comic.chapters = chapters
                return comic
            
            return None
        except Exception as e:
            logger.error(f"从JM漫画获取漫画详情失败: {e}")
            return None
    
    async def search_comics(self, keyword: str, page: int = 1, page_size: int = 20, 
                           sort: str = "newest", tags: Optional[List[str]] = None) -> PaginatedResult:
        """搜索漫画"""
        skip = (page - 1) * page_size
        query: Dict[str, Any] = {}
        
        # 构建查询条件
        if keyword:
            # 尝试将keyword解析为JM漫画ID
            if keyword.isdigit():
                # 先查询本地数据库
                query["$or"] = [
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"author": {"$regex": keyword, "$options": "i"}},
                    {"description": {"$regex": keyword, "$options": "i"}}
                ]
                
                # 如果本地数据库没有，尝试从JM漫画获取
                db_total = await self.db.comics.count_documents(query)
                if db_total == 0:
                    try:
                        jm_comic = await self.jm_client.get_album_detail(keyword)
                        if jm_comic:
                            # 转换并保存到数据库
                            await self.get_comic_detail(keyword)
                    except Exception as e:
                        logger.error(f"从JM漫画搜索失败: {e}")
            else:
                query["$or"] = [
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"author": {"$regex": keyword, "$options": "i"}},
                    {"description": {"$regex": keyword, "$options": "i"}}
                ]
        
        if tags:
            query["tags"] = {"$in": tags}
        
        # 确定排序方式
        sort_field = "updated_at" if sort == "newest" else "created_at"
        
        # 查询总数
        total = await self.db.comics.count_documents(query)
        
        # 查询漫画列表
        cursor = self.db.comics.find(query).sort(sort_field, -1).skip(skip).limit(page_size)
        comics = []
        
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            comics.append(Comic(**doc))
        
        return PaginatedResult(
            items=comics,
            total=total,
            page=page,
            page_size=page_size,
            has_more=total > skip + len(comics)
        )
    
    async def get_chapter_pages(self, chapter_id: str) -> List[Page]:
        """获取章节页面"""
        # 从数据库获取章节信息
        chapter_doc = await self.db.chapters.find_one({"_id": ObjectId(chapter_id)})
        
        if not chapter_doc:
            return []
        
        chapter_doc["id"] = str(chapter_doc["_id"])
        del chapter_doc["_id"]
        chapter = Chapter(**chapter_doc)
        
        # 查询是否已有页面数据
        pages_cursor = self.db.pages.find({"chapter_id": chapter_id}).sort("order", 1)
        pages = []
        
        async for page_doc in pages_cursor:
            page_doc["id"] = str(page_doc["_id"])
            del page_doc["_id"]
            pages.append(Page(**page_doc))
        
        # 如果已有页面数据，直接返回
        if pages:
            return pages
        
        # 否则从JM漫画获取
        try:
            # 获取漫画信息
            comic_doc = await self.db.comics.find_one({"_id": ObjectId(chapter.comic_id)})
            
            if not comic_doc:
                return []
            
            # 假设我们存储了原始JM漫画ID
            jm_comic_id = comic_doc.get("jm_id") or chapter.comic_id
            
            # 获取章节图片
            jm_images = await self.jm_client.get_images(jm_comic_id, chapter.order)
            
            if not jm_images:
                return []
            
            # 创建漫画目录
            comic_dir = self.download_path / chapter.comic_id
            comic_dir.mkdir(exist_ok=True)
            
            # 创建章节目录
            chapter_dir = comic_dir / chapter_id
            chapter_dir.mkdir(exist_ok=True)
            
            # 下载图片
            tasks = []
            for i, img_url in enumerate(jm_images):
                page = Page(
                    id=str(ObjectId()),
                    chapter_id=chapter_id,
                    url=img_url,
                    order=i + 1,
                    local_path=f"/api/static/{chapter.comic_id}/{chapter_id}/{i + 1}.jpg"
                )
                pages.append(page)
                
                # 保存到数据库
                await self.db.pages.insert_one(page.dict(exclude={"id"}))
                
                # 下载图片
                tasks.append(self._download_image(img_url, chapter_dir / f"{i + 1}.jpg"))
            
            # 并发下载图片
            await asyncio.gather(*tasks)
            
            return pages
        except Exception as e:
            logger.error(f"获取章节页面失败: {e}")
            return []
    
    async def _download_image(self, url: str, path: Path):
        """下载图片"""
        try:
            # 如果文件已存在，跳过下载
            if path.exists():
                return
            
            # 下载图片
            response = await self.jm_client.session.get(url, timeout=settings.download_timeout)
            response.raise_for_status()
            
            # 保存图片
            with open(path, "wb") as f:
                f.write(await response.read())
                
            logger.debug(f"图片下载成功: {url} -> {path}")
        except Exception as e:
            logger.error(f"图片下载失败: {url} -> {path}, 错误: {e}")

# 创建服务实例
comic_service = ComicService() 