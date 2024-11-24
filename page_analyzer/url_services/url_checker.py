from page_analyzer.parser import get_seo_data
from page_analyzer.db_operators.database_queries import (find_by_id, add_check)
from typing import Tuple, Dict, Union, Any, Optional
import requests


def check_url_status(url: Any) \
        -> Tuple[int, Optional[str], Optional[str], Optional[str]]:
    """Checks the status of the passed URL, returning SEO data"""
    response = requests.get(url.name)
    response.raise_for_status()
    h1, title, description = get_seo_data(response.text)
    return response.status_code, h1, title, description


def check_and_add_url_check(conn: Any, id: int) \
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
        raise


def handle_get_one_url(id: int, conn: Any) -> Optional[Dict[str, Any]]:
    """Returns a URL by ID or notifies if the URL is not found"""
    url = find_by_id(conn, id)
    if url is None:
        return None
    return url
