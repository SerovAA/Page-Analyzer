import psycopg2
from .config import DATABASE_URL
from psycopg2.extras import NamedTupleCursor


def get_connection():
    """Создает подключение к базе данных."""
    return psycopg2.connect(DATABASE_URL)


def use_connection(func):
    """Декоратор для предоставления подключения и курсора."""
    def wrapper(*args, **kwargs):
        with (get_connection() as connection,
              connection.cursor(cursor_factory=NamedTupleCursor) as cursor):
            return func(cursor, *args, **kwargs)

    return wrapper
