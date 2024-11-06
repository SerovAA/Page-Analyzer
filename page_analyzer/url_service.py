import psycopg2
import requests
from flask import render_template, flash, redirect, url_for
from typing import Optional, Tuple, Dict, Union
from .database import (add_url, find_by_name, find_by_id, add_check)
from .url_check import validate_url, normalize_url
from .parser import get_seo_data


def process_url(url_from_request: str, cursor) \
        -> Tuple[Optional[dict], Optional[list]]:
    """
    Processes the URL, checking it for
    errors and adding it to the database.
    """
    errors = validate_url(url_from_request)
    if errors:
        return None, errors

    new_url = normalize_url(url_from_request)

    try:
        url_info = add_url(cursor, new_url)
        return url_info, None
    except psycopg2.errors.UniqueViolation:
        return find_by_name(new_url), None


def check_url_status(url) -> Tuple[int, str, str, str]:
    """Checks the status of the passed URL, returning SEO data."""
    response = requests.get(url.name)
    response.raise_for_status()
    h1, title, description = get_seo_data(response.text)
    return response.status_code, h1, title, description


def process_url_submission(cursor, url_from_request: str) \
        -> Tuple[Union[str, None], int]:
    """
    Processes the submitted URL, checking it
    and adding it to the database if there are no duplicates.
    """
    has_errors = bool(validate_url(url_from_request))
    url_id = None
    is_duplicate = False

    if not has_errors:
        new_url = normalize_url(url_from_request)
        try:
            add_url(cursor, new_url)
            cursor.execute("SELECT * FROM urls WHERE name = %s", (new_url,))
            url_info = cursor.fetchone()
            if url_info:
                url_id = url_info.id
        except psycopg2.errors.UniqueViolation:
            is_duplicate = True
            url = find_by_name(new_url)
            if url:
                url_id = url.id

    return handle_flash_messages(has_errors, is_duplicate, url_id)


def handle_flash_messages(has_errors: bool, is_duplicate: bool,
                          url_id: Optional[int]) -> Tuple[str, int]:
    """Processes flash messages to notify about errors or success."""
    if has_errors:
        flash('Некорректный URL', 'alert-danger')
        return render_template('index.html'), 422

    if is_duplicate:
        flash('Страница уже существует', 'alert-warning')
        return redirect(url_for('get_one_url', id=url_id))

    if url_id:
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for('get_one_url', id=url_id))

    flash('Произошла ошибка при добавлении URL', 'alert-danger')
    return render_template('index.html'), 500


def handle_get_one_url(id: int) -> Optional[dict]:
    """Returns a URL by ID or notifies if the URL is not found."""
    url = find_by_id(id)
    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return None
    return url


def check_and_add_url_check(id: int) -> Dict[str, Union[str, int]]:
    """Checks and adds a check for the URL with the passed ID."""
    url = find_by_id(id)
    try:
        status_code, h1, title, description = check_url_status(url)
        add_check(id, status_code, h1, title, description)
        return {
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


def flash_message(result: Dict[str, Union[str, int]]) -> None:
    """Generates a flash message based on the result of the URL check."""
    if 'error' in result:
        flash(f'Произошла ошибка при проверке: '
              f'{result["error"]}', 'alert-danger')
    else:
        flash('Страница успешно проверена', 'alert-success')
