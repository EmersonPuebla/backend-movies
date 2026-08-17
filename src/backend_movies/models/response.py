from typing import Generic, TypeVar
from pydantic import BaseModel

from backend_movies.models.app_codes import AppCode

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    code: AppCode
    message: str
    data: T | None = None
