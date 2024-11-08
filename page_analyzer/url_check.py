import validators
from urllib.parse import urlparse
from typing import List
from dataclasses import dataclass


@dataclass
class URLValidationResult:
    max_url_len: int = 255
    error_invalid_url: str = "Некорректный URL"
    error_too_long_url: str = "Слишком длинный URL"
    errors: List[str] = None

    def __init__(self, max_url_len: int = 255,
                 error_invalid_url: str = "Некорректный URL",
                 error_too_long_url: str = "Слишком длинный URL"):
        self.max_url_len = max_url_len
        self.error_invalid_url = error_invalid_url
        self.error_too_long_url = error_too_long_url
        self.errors = []

    def add_error(self, error: str):
        self.errors.append(error)

    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_url(url: str) -> URLValidationResult:
    """Validates URL correctness and length, returning error codes."""
    result = URLValidationResult()

    if not validators.url(url):
        result.add_error(result.error_invalid_url)

    if len(url) > result.max_url_len:
        result.add_error(result.error_too_long_url)

    return result


def normalize_url(url: str) -> str:
    """Converts URL to standard form."""
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
