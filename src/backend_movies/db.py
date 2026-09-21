import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "movies.db"

SEED_MOVIES = [
    (
        "Harry potter",
        152,
        "2001-11-16",
        "Chris Columbus",
        "Harry Potter, un niño huérfano, descubre que es un mago y asiste a la escuela Hogwarts de Magia y Hechicería, donde hace amigos y enfrenta desafíos mientras lucha contra el malvado Lord Voldemort",
        "/static/harry_potter.jpg",
        "harry-potter",
    ),
    (
        "Yo Robot",
        123,
        "2004-07-16",
        "Alex Proyas",
        "En un futuro donde los robots son parte de la vida cotidiana, un detective investiga un posible asesinato cometido por un robot, desafiando las leyes de la robótica y cuestionando la relación entre humanos y máquinas",
        "/static/yorobot.jpg",
        "yo-robot",
    ),
    (
        "WALL-E",
        98,
        "2008-06-27",
        "Andrew Stanton",
        "WALL-E es un robot solitario en un futuro post-apocalíptico que se enamora de otro robot llamado EVE y emprende una aventura para salvar a la humanidad",
        "/static/walle.webp",
        "wall-e",
    ),
]


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                duration INTEGER NOT NULL,
                release_date TEXT NOT NULL,
                director TEXT NOT NULL,
                synopsis TEXT NOT NULL,
                image_src TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO movies (title, duration, release_date, director, synopsis, image_src, slug) VALUES (?, ?, ?, ?, ?, ?, ?)",
                SEED_MOVIES,
            )
        else:
            _migrate_image_srcs(conn)
        conn.commit()
    finally:
        conn.close()


def _migrate_image_srcs(conn: sqlite3.Connection) -> None:
    """Repoint legacy movie images to the backend's own static folder."""
    rows = conn.execute("SELECT id, image_src FROM movies").fetchall()
    for row in rows:
        image_src = row["image_src"]
        if not image_src or image_src.startswith(("/static/", "http://", "https://")):
            continue
        filename = image_src.lstrip("/")
        conn.execute(
            "UPDATE movies SET image_src = ? WHERE id = ?",
            (f"/static/{filename}", row["id"]),
        )
