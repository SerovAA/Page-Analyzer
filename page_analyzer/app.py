from flask import Flask, request, render_template, redirect, url_for
from .config import SECRET_KEY
from .database import find_all_urls, find_checks
from .db_decorators import use_connection
from .flash_messages import flash_message, handle_get_one_url
from .url_check import check_and_add_url_check
from .url_processing import set_flash_messages

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def get_index() -> str:
    """Displays the main page."""
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
@use_connection
def get_urls_post(cursor) -> str:
    """
    Handles the URL submission and redirects
    or renders based on the result.
    """
    return set_flash_messages(cursor, request.form.to_dict())


@app.route('/urls', methods=['GET'])
def get_urls() -> str:
    """Displays a list of all URLs from the database."""
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int) -> str:
    """Displays information about a specific URL by its ID."""
    url = handle_get_one_url(id)
    if url is None:
        return redirect(url_for('get_index'))

    checks = find_checks(id)
    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int) -> str:
    """
    Runs a URL availability check and adds the result to the database.
    """
    result = check_and_add_url_check(id)
    flash_message(result)
    return redirect(url_for('get_one_url', id=id))
