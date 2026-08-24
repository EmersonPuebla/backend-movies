`backend-movies` es una API de peliculas programada en Python utilizando la libreria `FastAPI`

Requisitos para ejecutar
---
* Tener instalado [Python](https://www.python.org/)
* Tener instalado [UV](https://docs.astral.sh/uv/)

Si ya tienes instalado Python puedes instalar UV con el siguiente comando
```bash
pip install uv
```

Una vez tengas tanto python como UV instalado puedes abrir el proyecto con tu IDE favorito (ej. VSCode) y ejecutar el siguiente comando para instalar las dependencias del proyecto
```bash
uv sync
```

Finalmente para correr la API debes ejecutar el siguiente comando:
```bash
uv run fastapi dev src/backend_movies/main.py
```
