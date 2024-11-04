from flask import Flask, request, render_template, redirect, url_for
from .config import SECRET_KEY
from .database import find_all_urls, find_checks
from .db_decorators import use_connection
from .url_service import (handle_get_one_url,
                          check_and_add_url_check,
                          process_url_submission,
                          flash_message)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def get_index():
    """Displays the main page."""
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
@use_connection
def get_urls_post(cursor):
    """Processes the URL submission and adds it to the database."""
    url_from_request = request.form.to_dict().get('url', '')
    return process_url_submission(cursor, url_from_request)


@app.route('/urls', methods=['GET'])
def get_urls():
    """Displays a list of all URLs from the database."""
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int):
    """Displays information about a specific URL by its ID."""
    url = handle_get_one_url(id)
    if url is None:
        return redirect(url_for('get_index'))

    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=find_checks(id))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int):
    """
    Runs a URL availability check and adds the result to the database.
    """
    result = check_and_add_url_check(id)
    flash_message(result)
    return redirect(url_for('get_one_url', id=id))
