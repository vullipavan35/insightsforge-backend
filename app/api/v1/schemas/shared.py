from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: T


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int = 0
    page: int = 1
    limit: int = 20
    has_more: bool = False
