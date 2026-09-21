from fastapi import APIRouter, Depends

from backend_movies.auth import require_auth
from backend_movies.models.app_codes import AppCode
from backend_movies.models.movie import Movie, MovieData
from backend_movies.models.response import Response
from backend_movies.services.movies import (
    create_movie,
    delete_movie,
    find_all_movies,
    find_movie_by_id,
    update_movie,
)

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/movies")
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


@router.get("/movies/{movie_id}")
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


@router.post("/movies")
def add_movie(movie_data: MovieData) -> Response[Movie]:
    movie = create_movie(movie_data)

    return Response(
        code=AppCode.MOVIE_ADDED,
        message=f"Se ha añadido la pelicula {movie.title}",
        data=movie,
    )


@router.put("/movies/{movie_id}")
def edit_movie(movie_id: int, movie_data: MovieData) -> Response[Movie]:
    movie = update_movie(movie_id, movie_data)
    if movie is None:
        return Response(
            code=AppCode.MOVIE_NOT_UPDATED,
            message=f"No se ha encontrado la pelicula con id {movie_id}",
        )

    return Response(
        code=AppCode.MOVIE_UPDATED,
        message=f"Se ha actualizado la pelicula {movie.title}",
        data=movie,
    )


@router.delete("/movies/{movie_id}")
def remove_movie(movie_id: int) -> Response[None]:
    if not delete_movie(movie_id):
        return Response(
            code=AppCode.MOVIE_NOT_DELETED,
            message=f"No se ha encontrado la pelicula con id {movie_id}",
        )

    return Response(
        code=AppCode.MOVIE_DELETED,
        message=f"Se ha eliminado la pelicula con id {movie_id}",
    )
