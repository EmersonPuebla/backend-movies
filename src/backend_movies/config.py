import os
from pathlib import Path

# Raíz del paquete: src/backend_movies/
BASE_DIR = Path(__file__).resolve().parent

# Rutas configurables para poder montarlas como volúmenes en Docker.
# En local los valores por defecto reproducen el comportamiento anterior.
STATIC_DIR = Path(os.environ.get("STATIC_DIR", BASE_DIR / "static"))
DB_PATH = Path(os.environ.get("DB_PATH", BASE_DIR.parent.parent / "movies.db"))
