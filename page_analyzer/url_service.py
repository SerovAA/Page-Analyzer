import psycopg2
import requests
from flask import render_template, flash, redirect, url_for
from .database import (add_url, find_by_name, find_by_id, add_check)
from .url_check import validate_url, normalize_url
from .parser import get_seo_data


def process_url(url_from_request: str, cursor):
    """Обрабатывает URL, проверяя его на ошибки и добавляя в базу."""
    errors = validate_url(url_from_request)
    if errors:
        return None, errors

    new_url = normalize_url(url_from_request)

    try:
        url_info = add_url(cursor, new_url)
        return url_info, None
    except psycopg2.errors.UniqueViolation:
        return find_by_name(new_url), None


def check_url_status(url):
    """Проверяет статус переданного URL, возвращая SEO-данные."""
    try:
        with requests.get(url.name) as response:
            response.raise_for_status()
            h1, title, description = get_seo_data(response.text)
            return response.status_code, h1, title, description, None
    except requests.exceptions.RequestException as e:
        return None, None, None, None, str(e)


def process_url_submission(cursor, url_from_request: str):
    """Обрабатывает отправленный URL, проверяя его и добавляя в базу, если нет дубликатов."""
    errors = validate_url(url_from_request)
    url_id = None
    is_duplicate = False

    if not errors:
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

    return handle_flash_messages(errors, is_duplicate, url_id)


def handle_flash_messages(errors: list, is_duplicate: bool, url_id: int):
    """"Обрабатывает flash-сообщения для уведомления пользователя об ошибках или успехе."""
    if errors:
        flash('Некорректный URL', 'alert-danger')
        return render_template('index.html'), 422

    if is_duplicate:
        flash('Страница уже существует', 'alert-warning')
        return redirect(url_for('get_one_url', id=url_id))

    if url_id is not None:
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for('get_one_url', id=url_id))

    flash('Произошла ошибка при добавлении URL', 'alert-danger')
    return render_template('index.html'), 500


def handle_get_one_url(id: int):
    """Возвращает URL по идентификатору или уведомляет, если URL не найден."""
    url = find_by_id(id)
    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return None
    return url


def check_and_add_url_check(id: int, flash):
    """Проверяет и добавляет проверку для URL с переданным идентификатором."""
    url = find_by_id(id)
    status_code, h1, title, description, error = check_url_status(url)

    if error:
        flash(f'Произошла ошибка при проверке: {error}', 'alert-danger')
        return None

    add_check(id, status_code, h1, title, description)
    flash('Страница успешно проверена', 'alert-success')
    return status_code, h1, title, description
