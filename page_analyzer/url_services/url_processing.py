from page_analyzer.db_operators.database import add_url, find_by_name
from page_analyzer.url_check import validate_url, normalize_url
from page_analyzer.exceptions import URL_Error, URLError


def validate_and_normalize_url(url):
    validate_url(url)
    return normalize_url(url)


def handle_url_in_database(conn, url):
    existing_url = find_by_name(conn, url)
    if existing_url:
        return 'exists', existing_url.id

    new_url = add_url(conn, url)
    if new_url is None:
        raise URLError
    return 'success', new_url.id


def process_url_submission(conn, url):
    try:
        normalized_url = validate_and_normalize_url(url)
        result, url_id = handle_url_in_database(conn, normalized_url)
        return result, None, url_id
    except URL_Error as e:
        return 'error', str(e), None


def handle_url_submission(conn, url):
    result, message, url_id = process_url_submission(conn, url)
    if result == 'error':
        return 'error', message, None
    return result, None, url_id