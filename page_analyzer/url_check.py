import validators

from urllib.parse import urlparse

MAX_URL_LEN = 255


def validate_url(url):
    errors = []
    if not validators.url(url) or len(url) > MAX_URL_LEN:
        errors.append('Некорректный URL')
    return errors


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
