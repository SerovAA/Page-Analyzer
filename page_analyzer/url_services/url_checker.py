from page_analyzer.db_operators.database import URLRepository
from page_analyzer.db_operators.db_decorators import DatabaseConnection
from page_analyzer.parser import get_seo_data
import requests
from typing import Tuple, Dict, Union


def check_url_status(url) -> Tuple[int, str, str, str]:
    """Checks the status of the passed URL, returning SEO data."""
    response = requests.get(url.name)
    response.raise_for_status()
    h1, title, description = get_seo_data(response.text)
    return response.status_code, h1, title, description


def check_and_add_url_check(db_connection: DatabaseConnection, id: int) \
        -> Dict[str, Union[str, int]]:
    """Checks and adds a check for the URL with the passed ID."""
    url_repo = URLRepository(db_connection)
    url = url_repo.find_by_id(id)
    if not url:
        return {'error': 'URL not found'}

    try:
        status_code, h1, title, description = check_url_status(url)
        url_repo.add_check(id, status_code, h1, title, description)
        return {
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
