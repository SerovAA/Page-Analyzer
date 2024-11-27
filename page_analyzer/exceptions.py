class URL_Error(Exception):
    """Base class for URL-related exceptions."""
    pass


class InvalidURLError(URL_Error):
    """Raised when the URL is invalid."""
    def __init__(self, message="Invalid Url"):
        super().__init__(message)


class URLTooLongError(URL_Error):
    """Raised when the URL exceeds the maximum allowed length."""
    def __init__(self, message="URL too long"):
        super().__init__(message)


class URLError(URL_Error):
    """Raised for general URL-related errors."""
    def __init__(self, message="Error processing URL"):
        super().__init__(message)
