from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.comic_service import comic_service
from app.models.comic import Comic, PaginatedResult
from app.models.response import ApiResponse

router = APIRouter(tags=["comics"])

@router.get("/comics", response_model=ApiResponse[PaginatedResult])
async def get_comics(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """获取漫画列表"""
    result = await comic_service.get_comics(page, page_size)
    return ApiResponse(data=result)

@router.get("/comics/{comic_id}", response_model=ApiResponse[Comic])
async def get_comic_detail(comic_id: str):
    """获取漫画详情"""
    comic = await comic_service.get_comic_detail(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="漫画不存在")
    return ApiResponse(data=comic)

@router.get("/comics/latest", response_model=ApiResponse[List[Comic]])
async def get_latest_comics(limit: int = Query(10, ge=1, le=50)):
    """获取最新更新的漫画"""
    result = await comic_service.get_comics(1, limit)
    return ApiResponse(data=result.items)

@router.get("/comics/recommended", response_model=ApiResponse[List[Comic]])
async def get_recommended_comics(limit: int = Query(6, ge=1, le=20)):
    """获取推荐漫画"""
    # 简单实现，直接返回最新的几部漫画作为推荐
    result = await comic_service.get_comics(1, limit)
    return ApiResponse(data=result.items) 