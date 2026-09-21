from datetime import date

from pydantic import BaseModel


class MovieData(BaseModel):
    title: str
    duration: int
    release_date: date
    director: str
    synopsis: str
    image_src: str
    slug: str


class Movie(MovieData):
    id: int
