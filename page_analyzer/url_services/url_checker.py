from page_analyzer.parser import get_seo_data
from page_analyzer.db_operators.database_queries import (find_by_id, add_check)
from typing import Tuple, Dict, Union, Optional
from page_analyzer.exceptions import URLError
from psycopg2.extensions import connection
import requests


def check_url_status(url: Dict[str, int]) \
        -> Tuple[int, str, str, str]:
    """Checks the status of the passed URL, returning SEO data"""
    response = requests.get(url.name)
    response.raise_for_status()
    h1, title, description = get_seo_data(response.text)
    return response.status_code, h1, title, description


def check_and_add_url_check(conn: connection, id: int) \
        -> Dict[str, Union[int, Optional[str]]]:
    """ Verifies a URL by ID and adds a check record to the database"""
    url = find_by_id(conn, id)
    try:
        status_code, h1, title, description = check_url_status(url)
        add_check(conn, id, status_code, h1, title, description)
        return {
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description
        }
    except requests.exceptions.RequestException:
        raise URLError


def handle_get_one_url(id: int, conn: connection) -> Optional[Dict[str, int]]:
    """Returns a URL by ID or notifies if the URL is not found"""
    url = find_by_id(conn, id)
    if url is None:
        return None
    return url
