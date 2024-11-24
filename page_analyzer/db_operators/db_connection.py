from contextlib import contextmanager
import psycopg2
from page_analyzer.config import DATABASE_URL
from psycopg2.extras import NamedTupleCursor


@contextmanager
def get_connection():
    """"Context manager for database connection"""
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=NamedTupleCursor)
        yield conn
        conn.commit()
    except Exception as error:
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()
