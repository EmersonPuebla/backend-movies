import sqlite3
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

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

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


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
    try:
        movie = create_movie(movie_data)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El slug ya existe",
        )

    return Response(
        code=AppCode.MOVIE_ADDED,
        message=f"Se ha añadido la pelicula {movie.title}",
        data=movie,
    )


@router.put("/movies/{movie_id}")
def edit_movie(movie_id: int, movie_data: MovieData) -> Response[Movie]:
    try:
        movie = update_movie(movie_id, movie_data)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El slug ya existe",
        )

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


@router.post("/movies/upload")
async def upload_movie_image(
    file: Annotated[UploadFile, File()],
) -> Response[dict]:
    extension = ALLOWED_IMAGE_TYPES.get(file.content_type or "")
    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de imagen no permitido",
        )

    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen supera el límite de {MAX_IMAGE_SIZE_MB} MB",
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    (STATIC_DIR / filename).write_bytes(contents)

    return Response(
        code=AppCode.SUCCESS,
        message="Imagen subida correctamente",
        data={"url": f"/static/{filename}"},
    )
