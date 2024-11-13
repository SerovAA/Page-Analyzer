import psycopg2
from flask import render_template, redirect, url_for
from typing import Optional, Tuple, Dict, Any
from page_analyzer.db_operators.database import URLRepository
from page_analyzer.url_check import validate_url, normalize_url
from page_analyzer.url_services.flash_messages import handle_flash_messages
from page_analyzer.exceptions import InvalidURLError, URLTooLongError


def process_url_submission(url_repo: URLRepository, url_from_request: str) \
        -> Tuple[Optional[str], bool, Optional[int]]:
    try:
        validate_url(url_from_request)
        new_url = normalize_url(url_from_request)

        url_info = url_repo.add_url(new_url)
        if url_info:
            return None, url_info.id, False

    except InvalidURLError:
        return "Invalid URL", None, False
    except URLTooLongError:
        return "URL too long", None, False
    except psycopg2.errors.UniqueViolation:
        url = url_repo.find_by_name(new_url)
        if url:
            return None, url.id, True

    return "An error occurred", None, False


def set_flash_messages(url_repo: URLRepository, form_data: Dict[str, Any]) \
        -> Tuple[str, int]:
    """
    Handles URL submission, sets flash messages,
    and determines the appropriate response.
    """
    url_from_request = form_data.get('url', '')
    error_message, url_id, is_duplicate = (
        process_url_submission(url_repo, url_from_request))
    handle_flash_messages(error_message, is_duplicate, url_id)

    if error_message:
        return render_template('index.html'), 422
    elif is_duplicate or url_id:
        return redirect(url_for('get_one_url', id=url_id))
    else:
        return render_template('index.html'), 500
