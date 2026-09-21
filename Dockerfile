# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# 1) Dependencias: copia solo los metadatos para cachear esta capa.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 2) Código fuente.
COPY src ./src

# PYTHONPATH apunta a src para que el paquete backend_movies sea importable
# sin instalarlo en el venv (así __file__ resuelve a /app/src/... y los
# paths de sqlite/static quedan correctos).
ENV PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "backend_movies.main:app", "--host", "0.0.0.0", "--port", "8000"]
