from flask import Flask, request, render_template, redirect, url_for
from .config import SECRET_KEY
from page_analyzer.db_operators.database_queries import (find_all_urls,
                                                         find_checks)
from page_analyzer.url_services.url_processing import (handle_url_submission)
from page_analyzer.url_services.url_checker import (check_and_add_url_check,
                                                    handle_get_one_url)
from page_analyzer.db_operators.db_connection import get_connection
from flask import flash
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def get_index() -> str:
    """Displays the main page."""
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def get_urls_post():
    url = request.form['url']
    with get_connection() as conn:
        result, message, url_id = handle_url_submission(conn, url)

    if result == 'error':
        flash(message, 'alert-danger')
        return render_template('index.html'), 422

    if result == 'exists':
        flash_message = ("Страница уже существует", 'alert-warning')
    else:
        flash_message = ("Страница успешно добавлена", 'alert-success')

    flash(*flash_message)
    return redirect(url_for('get_one_url', id=url_id))


@app.route('/urls', methods=['GET'])
def get_urls() -> str:
    """Displays a list of all URLs from the db_operators."""
    with get_connection() as conn:
        urls = find_all_urls(conn)
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int) -> str:
    """Displays information about a specific URL by its ID."""
    with get_connection() as conn:
        url = handle_get_one_url(id, conn)
        if url is None:
            flash('Такой страницы не существует', 'alert-warning')
            return redirect(url_for('get_index'))

        checks = find_checks(conn, id)
    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int) -> str:
    """
    Runs a URL availability check and adds the result to the db_operators.
    """
    with get_connection() as conn:
        try:
            check_and_add_url_check(conn, id)
            flash('Страница успешно проверена', 'alert-success')
        except requests.exceptions.RequestException:
            flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('get_one_url', id=id))
