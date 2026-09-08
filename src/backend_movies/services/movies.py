from backend_movies.data.mock import movies_db
from backend_movies.models.movie import Movie

def find_movie_by_id(movie_id: int) -> Movie | None:
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    return None

def find_all_movies() -> list[Movie] | None:
    if len(movies_db) == 0:
        return None

    return movies_db

def create_movie(movie: Movie) -> bool:
    for stored_movie in movies_db:
        if stored_movie.id == movie.id:
            return False

    movies_db.append(movie)
    return True

def update_movie(movie_id: int, movie: Movie) -> bool:
    for index, stored_movie in enumerate(movies_db):
        if stored_movie.id == movie_id:
            movies_db[index] = movie
            return True

    return False

def delete_movie(movie_id: int) -> bool:
    for index, movie in enumerate(movies_db):
        if movie.id == movie_id:
            del movies_db[index]
            return True

    return False
