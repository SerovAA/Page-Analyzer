class URL_Error(Exception):
    """Base class for URL-related exceptions."""
    pass


class InvalidURLError(URL_Error):
    """Raised when the URL is invalid."""
    def __init__(self, message="Некорректный URL"):
        super().__init__(message)


class URLTooLongError(URL_Error):
    """Raised when the URL exceeds the maximum allowed length."""
    def __init__(self, message="Слишком длинный URL"):
        super().__init__(message)


class URLError(URL_Error):
    """Raised for general URL-related errors."""
    def __init__(self, message="Ошибка при обработке URL"):
        super().__init__(message)
