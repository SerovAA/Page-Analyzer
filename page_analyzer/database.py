from datetime import datetime
from .db_decorators import use_connection


@use_connection
def find_all_urls(cursor):
    cursor.execute(
        """
        SELECT urls.id, urls.name,
               MAX(url_checks.created_at) AS check_time,
               url_checks.status_code
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, url_checks.status_code
        ORDER BY urls.id DESC;
        """
    )
    return cursor.fetchall()


@use_connection
def find_by_id(cursor, id: int):
    cursor.execute("SELECT * FROM urls WHERE id = %s", (id,))
    return cursor.fetchone()


@use_connection
def find_by_name(cursor, name: str):
    cursor.execute("SELECT * FROM urls WHERE name = %s", (name,))
    return cursor.fetchone()


@use_connection
def find_checks(cursor, url_id: int):
    cursor.execute(
        """
        SELECT * FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC
        """,
        (url_id,)
    )
    return cursor.fetchall()


@use_connection
def add_check(cursor, id, status_code, h1, title, description):
    cursor.execute(
        """
        INSERT INTO url_checks (url_id, status_code, h1,
        title, description, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (id, status_code, h1, title, description,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def add_url(cursor, new_url):
    cursor.execute(
        """
        INSERT INTO urls (name, created_at)
        VALUES (%s, %s) RETURNING id
        """,
        (new_url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    return cursor.fetchone()
