import validators
from urllib.parse import urlparse
from typing import List

MAX_URL_LEN = 255
ERROR_INVALID_URL = "Некорректный URL"
ERROR_TOO_LONG_URL = "Слишком длинный URL"


def validate_url(url: str) -> List[str]:
    """Validates URL correctness and length, returning error codes."""
    errors = []
    if not validators.url(url):
        errors.append(ERROR_INVALID_URL)
    elif len(url) > MAX_URL_LEN:
        errors.append(ERROR_TOO_LONG_URL)
    return errors


def normalize_url(url: str) -> str:
    """Converts URL to standard form."""
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
