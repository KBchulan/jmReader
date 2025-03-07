from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Chapter(BaseModel):
    """章节模型"""
    id: str
    comic_id: str
    title: str
    order: int
    update_time: datetime = Field(default_factory=datetime.now)
    page_count: int = 0

class Page(BaseModel):
    """页面模型"""
    id: str
    chapter_id: str
    url: str
    order: int
    local_path: Optional[str] = None

class Comic(BaseModel):
    """漫画模型"""
    id: str
    title: str
    cover: str
    author: str
    description: str
    tags: List[str] = []
    update_time: datetime = Field(default_factory=datetime.now)
    status: str = "ongoing"  # ongoing, completed
    chapters: Optional[List[Chapter]] = None
    
class ComicInDB(Comic):
    """存储在数据库中的漫画模型"""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class PaginatedResult(BaseModel):
    """分页结果模型"""
    items: List[Comic]
    total: int
    page: int
    page_size: int
    has_more: bool 