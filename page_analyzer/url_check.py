import requests
from typing import Dict, Union, Tuple
from .database import add_check, find_by_id
from .parser import get_seo_data


def check_url_status(url) -> Tuple[int, str, str, str]:
    """Checks the status of the passed URL, returning SEO data."""
    response = requests.get(url.name)
    response.raise_for_status()
    h1, title, description = get_seo_data(response.text)
    return response.status_code, h1, title, description


def check_and_add_url_check(id: int) -> Dict[str, Union[str, int]]:
    """Checks and adds a check for the URL with the passed ID."""
    url = find_by_id(id)
    try:
        status_code, h1, title, description = check_url_status(url)
        add_check(id, status_code, h1, title, description)
        return {
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
