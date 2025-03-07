import logging
import os
import json
import subprocess
import sys
import shutil
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from app.models.comic import Comic, Chapter, Page, PaginatedResult
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class LocalComicService:
    """本地漫画服务"""
    
    def __init__(self):
        print('LocalComicService init')
    
    async def download_comic(self, comic_id: str) -> Optional[Comic]:
        """下载漫画"""
        try:
            # 检查漫画是否已存在
            comic_path = self.mock_data_path / comic_id
            if comic_path.exists():
                logger.info(f"漫画 {comic_id} 已存在，跳过下载")
                return await self.get_comic_detail(comic_id)
            
            # 检查下载脚本是否存在
            script_path = Path("./download_and_process.py")
            if not script_path.exists():
                logger.error(f"下载脚本 {script_path} 不存在")
                return None
            
            # 运行下载脚本
            logger.info(f"开始下载漫画 {comic_id}")
            result = subprocess.run(
                [sys.executable, str(script_path), comic_id],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"下载漫画 {comic_id} 失败: {result.stderr}")
                return None
            
            logger.info(f"下载漫画 {comic_id} 成功: {result.stdout}")
            
            # 检查漫画是否已下载
            if not comic_path.exists():
                logger.error(f"下载后找不到漫画目录 {comic_path}")
                return None
            
            # 读取漫画信息
            info_path = comic_path / "info.json"
            if not info_path.exists():
                logger.error(f"找不到漫画信息文件 {info_path}")
                return None
            
            with open(info_path, "r", encoding="utf-8") as f:
                comic_info = json.load(f)
            
            # 创建漫画对象
            comic = Comic(
                id=comic_info["id"],
                title=comic_info["title"],
                cover=comic_info["cover"],
                author=comic_info["author"],
                description=comic_info["description"],
                tags=comic_info["tags"],
                update_time=comic_info["update_time"],
                status=comic_info["status"],
                chapters=[
                    Chapter(
                        id=chapter["id"],
                        comic_id=chapter["comic_id"],
                        title=chapter["title"],
                        order=chapter["order"],
                        update_time=chapter["update_time"],
                        page_count=chapter["page_count"]
                    )
                    for chapter in comic_info["chapters"]
                ]
            )
            
            return comic
        except Exception as e:
            logger.exception(f"下载漫画 {comic_id} 时出错: {e}")
            return None
    
    async def get_comics(self, page: int = 1, page_size: int = 20) -> PaginatedResult:
        """获取漫画列表"""
        try:
            # 获取所有漫画目录
            comic_dirs = [d for d in self.mock_data_path.iterdir() if d.is_dir()]
            
            # 读取每个漫画的信息
            comics = []
            for comic_dir in comic_dirs:
                info_path = comic_dir / "info.json"
                if info_path.exists():
                    with open(info_path, "r", encoding="utf-8") as f:
                        comic_info = json.load(f)
                    
                    comic = Comic(
                        id=comic_info["id"],
                        title=comic_info["title"],
                        cover=comic_info["cover"],
                        author=comic_info["author"],
                        description=comic_info["description"],
                        tags=comic_info["tags"],
                        update_time=comic_info["update_time"],
                        status=comic_info["status"],
                        chapters=[]  # 不需要加载章节信息
                    )
                    comics.append(comic)
            
            # 按更新时间排序
            comics.sort(key=lambda x: x.update_time, reverse=True)
            
            # 分页
            total = len(comics)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            comics_page = comics[start_idx:end_idx]
            
            return PaginatedResult(
                items=comics_page,
                total=total,
                page=page,
                page_size=page_size
            )
        except Exception as e:
            logger.exception(f"获取漫画列表时出错: {e}")
            return PaginatedResult(
                items=[],
                total=0,
                page=page,
                page_size=page_size
            )
    
    async def get_comic_detail(self, comic_id: str) -> Optional[Comic]:
        """获取漫画详情"""
        try:
            # 检查漫画是否存在
            comic_path = self.mock_data_path / comic_id
            if not comic_path.exists():
                logger.error(f"漫画 {comic_id} 不存在")
                return None
            
            # 读取漫画信息
            info_path = comic_path / "info.json"
            if not info_path.exists():
                logger.error(f"找不到漫画信息文件 {info_path}")
                return None
            
            with open(info_path, "r", encoding="utf-8") as f:
                comic_info = json.load(f)
            
            # 创建漫画对象
            comic = Comic(
                id=comic_info["id"],
                title=comic_info["title"],
                cover=comic_info["cover"],
                author=comic_info["author"],
                description=comic_info["description"],
                tags=comic_info["tags"],
                update_time=comic_info["update_time"],
                status=comic_info["status"],
                chapters=[
                    Chapter(
                        id=chapter["id"],
                        comic_id=chapter["comic_id"],
                        title=chapter["title"],
                        order=chapter["order"],
                        update_time=chapter["update_time"],
                        page_count=chapter["page_count"]
                    )
                    for chapter in comic_info["chapters"]
                ]
            )
            
            return comic
        except Exception as e:
            logger.exception(f"获取漫画 {comic_id} 详情时出错: {e}")
            return None
    
    async def search_comics(self, keyword: str, page: int = 1, page_size: int = 20, 
                           sort: str = "newest", tags: Optional[List[str]] = None) -> PaginatedResult:
        """搜索漫画"""
        try:
            # 获取所有漫画
            all_comics = await self.get_comics(page=1, page_size=1000)
            comics = all_comics.items
            
            # 根据关键词过滤
            if keyword:
                comics = [
                    comic for comic in comics
                    if keyword.lower() in comic.title.lower() or
                       keyword.lower() in comic.description.lower() or
                       keyword.lower() in comic.author.lower()
                ]
            
            # 根据标签过滤
            if tags:
                comics = [
                    comic for comic in comics
                    if any(tag in comic.tags for tag in tags)
                ]
            
            # 排序
            if sort == "newest":
                comics.sort(key=lambda x: x.update_time, reverse=True)
            elif sort == "oldest":
                comics.sort(key=lambda x: x.update_time)
            
            # 分页
            total = len(comics)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            comics_page = comics[start_idx:end_idx]
            
            return PaginatedResult(
                items=comics_page,
                total=total,
                page=page,
                page_size=page_size
            )
        except Exception as e:
            logger.exception(f"搜索漫画时出错: {e}")
            return PaginatedResult(
                items=[],
                total=0,
                page=page,
                page_size=page_size
            )
    
    async def get_chapter_pages(self, chapter_id: str) -> List[Page]:
        """获取章节页面"""
        try:
            # 解析章节ID
            parts = chapter_id.split("_")
            if len(parts) != 2:
                logger.error(f"无效的章节ID: {chapter_id}")
                return []
            
            comic_id, chapter_order = parts
            
            # 检查漫画是否存在
            comic_path = self.mock_data_path / comic_id
            if not comic_path.exists():
                logger.error(f"漫画 {comic_id} 不存在")
                return []
            
            # 检查章节是否存在
            chapter_path = comic_path / chapter_order
            if not chapter_path.exists():
                logger.error(f"章节 {chapter_id} 不存在")
                return []
            
            # 获取所有图片文件
            image_files = []
            for ext in ['.jpg', '.png', '.webp']:
                image_files.extend(chapter_path.glob(f"*{ext}"))
            
            # 按文件名排序
            def extract_page_number(path):
                # 尝试从文件名中提取数字
                import re
                numbers = re.findall(r'\d+', path.stem)
                return int(numbers[0]) if numbers else 0
            
            image_files.sort(key=extract_page_number)
            
            # 创建页面对象
            pages = []
            for i, image_file in enumerate(image_files):
                page = Page(
                    id=f"{chapter_id}_{i+1}",
                    chapter_id=chapter_id,
                    order=i + 1,
                    url=f"/api/static/{comic_id}/{chapter_order}/{image_file.name}"
                )
                pages.append(page)
            
            return pages
        except Exception as e:
            logger.exception(f"获取章节 {chapter_id} 页面时出错: {e}")
            return [] 