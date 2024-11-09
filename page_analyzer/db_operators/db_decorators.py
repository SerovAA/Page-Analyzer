import psycopg2
from page_analyzer.config import DATABASE_URL
from psycopg2.extras import NamedTupleCursor
from typing import Callable, Any


def get_connection() -> psycopg2.extensions.connection:
    """Creates a connection to a db_operators."""
    return psycopg2.connect(DATABASE_URL)


def use_connection(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to provide connection and cursor."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with (get_connection() as connection,
              connection.cursor(cursor_factory=NamedTupleCursor) as cursor):
            return func(cursor, *args, **kwargs)

    return wrapper
