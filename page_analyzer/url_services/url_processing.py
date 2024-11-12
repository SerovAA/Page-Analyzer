import psycopg2
from flask import render_template, redirect, url_for
from typing import Optional, Tuple
from page_analyzer.db_operators.database import add_url, find_by_name
from page_analyzer.url_check import validate_url, normalize_url
from page_analyzer.url_services.flash_messages import handle_flash_messages
from page_analyzer.exceptions import InvalidURLError, URLTooLongError


def process_url_submission(cursor, url_from_request: str) \
        -> Tuple[Optional[str], bool, Optional[int]]:
    """
    Processes the submitted URL, validating it
    and attempting to add it to the database if unique.
    """
    try:
        validate_url(url_from_request)
        new_url = normalize_url(url_from_request)
        add_url(cursor, new_url)
        cursor.execute("SELECT * FROM urls WHERE name = %s", (new_url,))
        url_info = cursor.fetchone()
        if url_info:
            return None, url_info.id, False

    except InvalidURLError as e:
        return str(e), None, False

    except URLTooLongError as e:
        return str(e), None, False

    except psycopg2.errors.UniqueViolation:
        url = find_by_name(new_url)
        if url:
            return None, url.id, True


def set_flash_messages(cursor, form_data: dict) -> Tuple[str, int]:
    """
    Handles URL submission, sets flash messages
    and determines the appropriate response
    """
    url_from_request = form_data.get('url', '')
    error_message, url_id, is_duplicate = (
        process_url_submission(cursor, url_from_request))

    handle_flash_messages(error_message, is_duplicate, url_id)

    if error_message:
        return render_template('index.html'), 422
    elif is_duplicate or url_id:
        return redirect(url_for('get_one_url', id=url_id))
    else:
        return render_template('index.html'), 500
