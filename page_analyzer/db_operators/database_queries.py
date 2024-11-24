from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any


def find_all_urls(conn) \
        -> List[Tuple[int, str, Optional[datetime], Optional[int]]]:
    """
    Returns all URLs from the database
    with information about the last check.
    """
    query = """
        SELECT urls.id, urls.name,
               MAX(url_checks.created_at) AS check_time,
               url_checks.status_code
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, url_checks.status_code
        ORDER BY urls.id DESC;
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def find_by_id(conn, id: int) -> Optional[Dict[str, Any]]:
    """Finds a URL by its ID."""
    query = "SELECT * FROM urls WHERE id = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (id,))
        return cursor.fetchone()


def find_by_name(conn, name: str) -> Optional[Dict[str, Any]]:
    """Finds a URL by its name."""
    query = "SELECT * FROM urls WHERE name = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (name,))
        return cursor.fetchone()


def find_checks(conn, url_id: int) -> List[Dict[str, Any]]:
    """Returns all checks for the specified URL by ID."""
    query = """
        SELECT * FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (url_id,))
        return cursor.fetchall()


def add_check(conn, id: int, status_code: int,
              h1: str, title: str, description: str) -> None:
    """Adds a check record for a URL into the database."""
    query = """
        INSERT INTO url_checks (url_id, status_code, h1,
        title, description, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW()::timestamp(0))
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (id, status_code, h1, title, description))


def add_url(conn, new_url: str) -> Optional[Dict[str, Any]]:
    """Adds a new URL to the database and returns its ID."""
    query = """
        INSERT INTO urls (name, created_at)
        VALUES (%s, NOW()::timestamp(0)) RETURNING id
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (new_url,))
        return cursor.fetchone()
