from fastapi import APIRouter, Query
from typing import List, Optional

from app.services.comic_service import comic_service
from app.models.comic import PaginatedResult
from app.models.response import ApiResponse
from app.models.search import SearchParams

router = APIRouter(tags=["search"])

@router.get("/comics/search", response_model=ApiResponse[PaginatedResult])
async def search_comics(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("newest", regex="^(newest|popular)$"),
    tags: Optional[List[str]] = Query(None)
):
    """搜索漫画"""
    result = await comic_service.search_comics(
        keyword=keyword,
        page=page,
        page_size=page_size,
        sort=sort,
        tags=tags
    )
    return ApiResponse(data=result) 