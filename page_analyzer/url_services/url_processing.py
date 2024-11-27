from page_analyzer.db_operators.database_queries import add_url, find_by_name
from page_analyzer.url_validate import validate_url, normalize_url
from page_analyzer.exceptions import URLError
from psycopg2.extensions import connection
from typing import Tuple


def handle_url_submission(conn: connection, url: str) -> Tuple[str, int]:
    """
    Validates, normalizes, and processes a URL submission,
    returning a structured result.
    """
    validate_url(url)
    normalized_url = normalize_url(url)

    existing_url = find_by_name(conn, normalized_url)
    if existing_url:
        return 'exists', existing_url.id
    new_url = add_url(conn, normalized_url)
    if not new_url:
        raise URLError
    return 'success', new_url.id
