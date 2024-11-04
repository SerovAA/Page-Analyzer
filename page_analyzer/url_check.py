import validators

from urllib.parse import urlparse

MAX_URL_LEN = 255


def validate_url(url: str) -> str:
    """Checks URL for correctness and length."""
    errors = []
    if not validators.url(url) or len(url) > MAX_URL_LEN:
        errors.append('Некорректный URL')
    return errors


def normalize_url(url: str) -> str:
    """Converts URL to standard form."""
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
