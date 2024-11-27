import validators
from urllib.parse import urlparse
from page_analyzer.exceptions import InvalidURLError, URLTooLongError

MAX_URL_LEN = 255


def validate_url(url: str) -> None:
    if len(url) > MAX_URL_LEN:
        raise URLTooLongError()
    if not validators.url(url):
        raise InvalidURLError()


def normalize_url(url: str) -> str:
    """Converts URL to standard form."""
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
