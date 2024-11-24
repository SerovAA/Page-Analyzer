from page_analyzer.db_operators.database_queries import add_url, find_by_name
from page_analyzer.url_check import validate_url, normalize_url
from page_analyzer.exceptions import URL_Error, URLError
from typing import Tuple, Any, Optional


def validate_and_normalize_url(url: str) -> str:
    """Validates and normalizes the given URL"""
    validate_url(url)
    return normalize_url(url)


def handle_url_in_database(conn: Any, url: str) -> Tuple[str, int]:
    """Handles adding or retrieving a URL from the database"""
    existing_url = find_by_name(conn, url)
    if existing_url:
        return 'exists', existing_url.id

    new_url = add_url(conn, url)
    if new_url is None:
        raise URLError
    return 'success', new_url.id


def process_url_submission(conn: Any, url: str) \
        -> Tuple[str, Optional[str], Optional[int]]:
    """
    Processes a URL submission by validating, normalizing,
    and adding or checking its presence in the database.
    """
    try:
        normalized_url = validate_and_normalize_url(url)
        result, url_id = handle_url_in_database(conn, normalized_url)
        return result, None, url_id
    except URL_Error as e:
        return 'error', str(e), None


def handle_url_submission(conn: Any, url: str) \
        -> Tuple[str, Optional[str], Optional[int]]:
    """Handles the submission of a URL and provides feedback on the result"""
    result, message, url_id = process_url_submission(conn, url)
    if result == 'error':
        return 'error', message, None
    return result, None, url_id
