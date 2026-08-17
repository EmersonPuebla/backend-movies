from fastapi import FastAPI

from backend_movies.models.app_codes import AppCode
from backend_movies.models.movie import Movie
from backend_movies.models.response import Response
from backend_movies.services.movies import (
    create_movie,
    find_all_movies,
    find_movie_by_id,
)

app = FastAPI()

@app.get("/movies")
def get_movies_catalog() -> Response[list[Movie] | None]:

    movies = find_all_movies()

    if not movies:
        return Response(
            code=AppCode.MOVIE_EMPTY,
            message="No existen peliculas disponibles",
        )

    return Response(
        code=AppCode.MOVIE_FOUND,
        message=f"Se han encontrado {len(movies)} peliculas",
        data=movies,
    )

@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int) -> Response[Movie]:

    movie = find_movie_by_id(movie_id)

    if not movie:
        return Response(
            code=AppCode.MOVIE_NOT_FOUND,
            message=f"No se ha encontrado la pelicula con id {movie_id}",
            data=movie,
        )

    return Response(
        code=AppCode.MOVIE_FOUND,
        message="Pelicula encontrada",
        data=movie,
    )

@app.post("/movies")
def add_movie(movie: Movie) -> Response[None]:

    if not create_movie(movie):
        return Response(
            code=AppCode.MOVIE_NOT_ADDED,
            message="No se ha podido añadir la pelicula",
        )

    return Response(
        code=AppCode.MOVIE_ADDED,
        message=f"Se ha añadido la pelicula {movie.name}",
    )
