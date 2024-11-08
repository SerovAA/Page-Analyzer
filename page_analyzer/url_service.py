import psycopg2
import requests
from flask import render_template, flash, redirect, url_for
from typing import List, Optional, Tuple, Dict, Union
from .database import (add_url, find_by_name, find_by_id, add_check)
from .url_check import validate_url, normalize_url
from .parser import get_seo_data


def process_url(url_from_request: str, cursor) \
        -> Tuple[Optional[dict], Optional[list]]:
    """
    Processes the URL, checking it for errors and adding it to the database.
    """
    result = validate_url(url_from_request)
    if not result.is_valid():
        return None, result.errors

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
        -> Tuple[List[str], bool, Optional[int]]:
    """
    Processes the submitted URL, checking it
    and adding it to the database if there are no duplicates.
    """
    result = validate_url(url_from_request)
    url_id = None
    is_duplicate = False

    if result.is_valid():
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

    return result.errors, is_duplicate, url_id


def handle_flash_messages(errors: List[str],
                          is_duplicate: bool,
                          url_id: Optional[int]) -> None:
    """Handles flash messages for URL submission."""
    if errors:
        for error in errors:
            flash(error, 'alert-danger')
    elif is_duplicate:
        flash('Страница уже существует', 'alert-warning')
    elif url_id:
        flash('Страница успешно добавлена', 'alert-success')
    else:
        flash('Произошла ошибка при добавлении URL', 'alert-danger')


def set_flash_messages(cursor, form_data: dict) -> Tuple[str, int]:
    """
    Process the URL submission, handle flash messages, and return response.
    """
    url_from_request = form_data.get('url', '')
    errors, is_duplicate, url_id = (
        process_url_submission(cursor, url_from_request))

    handle_flash_messages(errors, is_duplicate, url_id)

    if errors:
        return render_template('index.html'), 422
    if is_duplicate or url_id:
        return redirect(url_for('get_one_url', id=url_id))

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
