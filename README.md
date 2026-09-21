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

Endpoints disponibles
---
* `GET /movies`: listar todas las peliculas.
* `GET /movies/{movie_id}`: consultar una pelicula por id.
* `POST /movies`: crear una pelicula. El ID se genera automaticamente.
* `PUT /movies/{movie_id}`: reemplazar una pelicula existente usando el ID de la ruta.
* `DELETE /movies/{movie_id}`: eliminar una pelicula.

El almacenamiento se realiza en SQLite (libreria estandar `sqlite3`) en el archivo `movies.db`.

## Autenticacion

Todos los endpoints exigen un access token de Amazon Cognito en la cabecera `Authorization: Bearer <token>`.

Configura las variables `COGNITO_REGION`, `COGNITO_USER_POOL_ID` y `COGNITO_CLIENT_ID` (ver `.env.example`) y arranca con:

```bash
uv run --env-file .env fastapi dev src/backend_movies/main.py
```
