from flask import flash
from typing import Optional, Dict, Union


def handle_flash_messages(error_message: Optional[str],
                          is_duplicate: bool,
                          url_id: Optional[int]) -> None:
    """Handles flash messages for URL submission."""
    if error_message == "Invalid URL":
        flash('Некорректный URL', 'alert-danger')
    elif error_message == "URL too long":
        flash('URL слишком длинный', 'alert-danger')
    elif is_duplicate:
        flash('Страница уже существует', 'alert-warning')
    elif url_id:
        flash('Страница успешно добавлена', 'alert-success')
    else:
        flash('Произошла ошибка при добавлении URL', 'alert-danger')


def handle_get_one_url(url: Optional[dict]) -> Optional[dict]:
    """Returns a URL by ID or notifies if the URL is not found."""
    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return None
    return url


def flash_message(result: Dict[str, Union[str, int]]) -> None:
    """Generates a flash message based on the result of the URL check."""
    if 'error' in result:
        flash('Произошла ошибка при проверке', 'alert-danger')
    else:
        flash('Страница успешно проверена', 'alert-success')
