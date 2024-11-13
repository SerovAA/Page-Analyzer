from flask import flash
from typing import Optional, Dict, Union
from page_analyzer.db_operators.database import find_by_id


def handle_flash_messages(error_message: Optional[str],
                          is_duplicate: bool,
                          url_id: Optional[int]) -> None:
    """Handles flash messages for URL submission."""
    if error_message:
        flash('Некорректный URL', 'alert-danger')
    elif is_duplicate:
        flash('Страница уже существует', 'alert-warning')
    elif url_id:
        flash('Страница успешно добавлена', 'alert-success')
    else:
        flash('Произошла ошибка при добавлении URL', 'alert-danger')


def handle_get_one_url(id: int) -> Optional[dict]:
    """Returns a URL by ID or notifies if the URL is not found."""
    url = find_by_id(id)
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
