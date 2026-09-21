from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend_movies.config import BASE_DIR, STATIC_DIR
from backend_movies.db import init_db
from backend_movies.endpoints.movies import router as movies_router


def ensure_seed_images() -> None:
    """Copia las imágenes de ejemplo al STATIC_DIR si no existen.

    Necesario cuando STATIC_DIR apunta a un volumen montado (Docker) que
    arranca vacío; en local STATIC_DIR ya contiene las imágenes.
    """
    seed_dir = BASE_DIR / "static"
    if STATIC_DIR == seed_dir:
        return
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    for source in seed_dir.iterdir():
        if not source.is_file():
            continue
        target = STATIC_DIR / source.name
        if not target.exists():
            target.write_bytes(source.read_bytes())


init_db()
ensure_seed_images()

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
