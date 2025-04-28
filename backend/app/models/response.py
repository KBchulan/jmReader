from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """API响应模型"""
    code: int = 200
    data: Optional[T] = None
    message: str = "操作成功"
    success: bool = True