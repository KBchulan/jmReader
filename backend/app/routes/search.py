from fastapi import APIRouter, Query
from typing import List, Optional

from app.models.comic import PaginatedResult
from app.services import local_comic_service

router = APIRouter(tags=["search"])

@router.get("/comics/search", response_model=PaginatedResult)
async def search_comics(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("newest", regex="^(newest|oldest|popular)$"),
    tags: Optional[List[str]] = Query(None)
):
    """搜索漫画"""
    result = await local_comic_service.search_comics(keyword, page, page_size, sort, tags)
    return result 