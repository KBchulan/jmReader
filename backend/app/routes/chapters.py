from fastapi import APIRouter, HTTPException
from typing import List

from app.services.comic_service import comic_service
from app.models.comic import Page
from app.models.response import ApiResponse

router = APIRouter(tags=["chapters"])

@router.get("/chapters/{chapter_id}/pages", response_model=ApiResponse[List[Page]])
async def get_chapter_pages(chapter_id: str):
    """获取章节页面"""
    pages = await comic_service.get_chapter_pages(chapter_id)
    if not pages:
        raise HTTPException(status_code=404, detail="章节不存在或无法获取页面")
    return ApiResponse(data=pages) 