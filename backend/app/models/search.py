from pydantic import BaseModel
from typing import List, Optional

class SearchParams(BaseModel):
    """搜索参数模型"""
    keyword: str
    page: int = 1
    page_size: int = 20
    sort: Optional[str] = "newest"  # newest, popular
    tags: Optional[List[str]] = None 