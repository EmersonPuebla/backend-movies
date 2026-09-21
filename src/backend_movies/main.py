from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend_movies.db import init_db
from backend_movies.endpoints.movies import router as movies_router

init_db()

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Movie posters are served publicly from the backend (loaded via <img src>),
# while the movie data itself remains protected by the movies router below.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(movies_router)
