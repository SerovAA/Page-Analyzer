from flask import Flask, request, render_template, flash, redirect, url_for
from .config import SECRET_KEY
from .database import find_all_urls, find_checks
from .db_decorators import use_connection
from .url_service import (handle_get_one_url,
                          check_and_add_url_check,
                          process_url_submission)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
@use_connection
def get_urls_post(cursor):
    url_from_request = request.form.to_dict().get('url', '')
    return process_url_submission(cursor, url_from_request)


@app.route('/urls', methods=['GET'])
def get_urls():
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int):
    url = handle_get_one_url(id)
    if url is None:
        return redirect(url_for('get_index'))

    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=find_checks(id))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int):
    check_and_add_url_check(id, flash)
    return redirect(url_for('get_one_url', id=id))
