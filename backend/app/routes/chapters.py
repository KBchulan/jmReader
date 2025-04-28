from fastapi import APIRouter, HTTPException, Path
from typing import List

from app.models.comic import Page
from app.services import local_comic_service

router = APIRouter(tags=["chapters"])

@router.get("/chapters/{chapter_id}/pages", response_model=List[Page])
async def get_chapter_pages(chapter_id: str = Path(...)):
    """获取章节页面"""
    pages = await local_comic_service.get_chapter_pages(chapter_id)
    if not pages:
        raise HTTPException(status_code=404, detail="章节不存在或没有页面")
    return pages