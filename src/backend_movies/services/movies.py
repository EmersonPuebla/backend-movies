from backend_movies.data.mock import movies_db
from backend_movies.models.movie import Movie, MovieData

next_movie_id = 1

def find_movie_by_id(movie_id: int) -> Movie | None:
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    return None

def find_all_movies() -> list[Movie] | None:
    if len(movies_db) == 0:
        return None

    return movies_db

def create_movie(movie_data: MovieData) -> Movie:
    global next_movie_id

    while find_movie_by_id(next_movie_id) is not None:
        next_movie_id += 1

    movie = Movie(id=next_movie_id, **movie_data.model_dump())
    movies_db.append(movie)
    next_movie_id += 1
    return movie

def update_movie(movie_id: int, movie_data: MovieData) -> Movie | None:
    for index, stored_movie in enumerate(movies_db):
        if stored_movie.id == movie_id:
            movie = Movie(id=movie_id, **movie_data.model_dump())
            movies_db[index] = movie
            return movie

    return None

def delete_movie(movie_id: int) -> bool:
    for index, movie in enumerate(movies_db):
        if movie.id == movie_id:
            del movies_db[index]
            return True

    return False
