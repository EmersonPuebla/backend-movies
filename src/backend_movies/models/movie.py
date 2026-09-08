from datetime import date

from pydantic import BaseModel

class MovieMeta(BaseModel):
    director: str
    release_date: date
    duration: int

class MovieData(BaseModel):
    name: str
    meta: MovieMeta

class Movie(MovieData):
    id: int
