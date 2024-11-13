from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
from page_analyzer.db_operators.db_decorators import DatabaseConnection


class URLRepository:
    """Repository class for interacting with the URL database."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def find_all_urls(self) -> List[Tuple[
        int,
        str,
        Optional[datetime],
        Optional[int]
    ]]:

        cursor = self.db_connection.get_cursor()
        try:
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
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            cursor.close()

    def find_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute("SELECT * FROM urls WHERE name = %s", (name,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def find_checks(self, url_id: int) -> List[Dict[str, Any]]:
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                """
                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                """,
                (url_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def add_check(self, id: int, status_code: int, h1: str,
                  title: str, description: str) -> None:
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id, status_code, h1,
                title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW()::timestamp(0))
                """,
                (id, status_code, h1, title, description)
            )
            self.db_connection.commit()
        finally:
            cursor.close()

    def add_url(self, new_url: str) -> Optional[Dict[str, Any]]:
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%s, NOW()::timestamp(0)) RETURNING id
                """,
                (new_url,)
            )
            self.db_connection.commit()
            return cursor.fetchone()
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            cursor.close()
