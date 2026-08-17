from datetime import date

from pydantic import BaseModel

class MovieMeta(BaseModel):
    director: str
    release_date: date
    duration: int

class Movie(BaseModel):
    id: int
    name: str
    meta: MovieMeta
