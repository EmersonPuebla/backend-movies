import sqlite3

from backend_movies.db import connect
from backend_movies.models.movie import Movie, MovieData


def _row_to_movie(row: sqlite3.Row) -> Movie:
    return Movie(**dict(row))


def find_movie_by_id(movie_id: int) -> Movie | None:
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    finally:
        conn.close()
    return _row_to_movie(row) if row else None


def find_all_movies() -> list[Movie] | None:
    conn = connect()
    try:
        rows = conn.execute("SELECT * FROM movies").fetchall()
    finally:
        conn.close()
    movies = [_row_to_movie(row) for row in rows]
    return movies if movies else None


def create_movie(movie_data: MovieData) -> Movie:
    conn = connect()
    try:
        cursor = conn.execute(
            "INSERT INTO movies (title, duration, release_date, director, synopsis, image_src, slug) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                movie_data.title,
                movie_data.duration,
                movie_data.release_date.isoformat(),
                movie_data.director,
                movie_data.synopsis,
                movie_data.image_src,
                movie_data.slug,
            ),
        )
        conn.commit()
        movie_id = cursor.lastrowid
    finally:
        conn.close()
    return Movie(id=movie_id, **movie_data.model_dump())


def update_movie(movie_id: int, movie_data: MovieData) -> Movie | None:
    conn = connect()
    try:
        cursor = conn.execute(
            "UPDATE movies SET title = ?, duration = ?, release_date = ?, director = ?, synopsis = ?, image_src = ?, slug = ? WHERE id = ?",
            (
                movie_data.title,
                movie_data.duration,
                movie_data.release_date.isoformat(),
                movie_data.director,
                movie_data.synopsis,
                movie_data.image_src,
                movie_data.slug,
                movie_id,
            ),
        )
        conn.commit()
        updated = cursor.rowcount > 0
    finally:
        conn.close()
    return Movie(id=movie_id, **movie_data.model_dump()) if updated else None


def delete_movie(movie_id: int) -> bool:
    conn = connect()
    try:
        cursor = conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
    finally:
        conn.close()
    return deleted
