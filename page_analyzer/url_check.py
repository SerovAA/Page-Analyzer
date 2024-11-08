import validators
from urllib.parse import urlparse
from typing import List
from dataclasses import dataclass

MAX_URL_LEN = 255
ERROR_INVALID_URL = "Некорректный URL"
ERROR_TOO_LONG_URL = "Слишком длинный URL"


@dataclass
class URLValidationResult:
    errors: List[str]

    def __init__(self):
        self.errors = []

    def add_error(self, error: str):
        self.errors.append(error)

    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_url(url: str) -> URLValidationResult:
    """Validates URL correctness and length, returning error codes."""
    result = URLValidationResult()

    if not validators.url(url):
        result.add_error(ERROR_INVALID_URL)

    if len(url) > MAX_URL_LEN:
        result.add_error(ERROR_TOO_LONG_URL)

    return result


def normalize_url(url: str) -> str:
    """Converts URL to standard form."""
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
