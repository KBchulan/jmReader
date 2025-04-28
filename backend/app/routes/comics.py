from fastapi import APIRouter, HTTPException, Query, Path
from typing import List

from app.models.comic import Comic, PaginatedResult
from app.services import local_comic_service

router = APIRouter(tags=["comics"])

@router.get("/comics", response_model=PaginatedResult)
async def get_comics(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    """获取漫画列表"""
    result = await local_comic_service.get_comics(page, page_size)
    return result

@router.get("/comics/{comic_id}", response_model=Comic)
async def get_comic_detail(comic_id: str = Path(...)):
    """获取漫画详情"""
    comic = await local_comic_service.get_comic_detail(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="漫画不存在")
    return comic

@router.get("/comics/download/{comic_id}", response_model=Comic)
async def download_comic(comic_id: str = Path(...)):
    """下载漫画"""
    comic = await local_comic_service.download_comic(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="下载漫画失败")
    return comic

@router.get("/comics/latest", response_model=List[Comic])
async def get_latest_comics(limit: int = Query(10, ge=1, le=50)):
    """获取最新漫画"""
    result = await local_comic_service.get_comics(1, limit)
    return result.items

@router.get("/comics/recommended", response_model=List[Comic])
async def get_recommended_comics(limit: int = Query(6, ge=1, le=20)):
    """获取推荐漫画"""
    result = await local_comic_service.get_comics(1, limit)
    return result.items