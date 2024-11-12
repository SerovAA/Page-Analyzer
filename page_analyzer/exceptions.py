class InvalidURLError(Exception):
    """Raised when the URL is invalid."""
    pass


class URLTooLongError(Exception):
    """Raised when the URL exceeds the maximum allowed length."""
    pass
