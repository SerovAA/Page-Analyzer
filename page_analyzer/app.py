import os
import psycopg2
import validators
import requests

from flask import Flask, render_template
from flask import flash, redirect, url_for, request
from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import NamedTupleCursor
from urllib.parse import urlparse

MAX_URL_LEN = 255

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)


def get_connected():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def urls_post():
    url_from_request = request.form.to_dict().get('url', '')
    errors = validate_url(url_from_request)

    if len(errors) != 0:
        flash('Некорректный URL', 'alert-danger')
        return render_template('index.html'), 422

    new_url = normalize_url(url_from_request)

    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            try:
                cursor.execute("INSERT INTO urls (name, created_at)\
                                VALUES (%s, %s) RETURNING id",
                               (new_url,
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                url_info = cursor.fetchone()
                url_id = url_info.id
                flash('Страница успешно добавлена', 'alert-success')

            except psycopg2.errors.UniqueViolation:
                url = find_by_name(new_url)
                url_id = url.id
                flash('Страница уже существует', 'alert-warning')

    return redirect(url_for('one_url', id=url_id))


def validate_url(url):
    errors = []
    if not validators.url(url) or len(url) > MAX_URL_LEN:
        errors.append('Некорректный URL')
    return errors


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def find_by_name(name: str):
    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE name = %s", (name, ))
            return cursor.fetchone()


@app.route('/urls', methods=['GET'])
def urls():
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


def find_all_urls():
    urls = []
    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                "SELECT urls.id, urls.name, \
                MAX(url_checks.created_at) AS check_time, \
                url_checks.status_code FROM urls \
                LEFT JOIN url_checks \
                ON urls.id = url_checks.url_id \
                GROUP BY urls.id, url_checks.status_code \
                ORDER BY urls.id DESC;"
            )
            urls.extend(cursor.fetchall())
    return urls


@app.route('/urls/<int:id>', methods=['GET'])
def one_url(id: int):
    url = find_by_id(id)

    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return redirect(url_for('index'))

    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=find_checks(id))


def find_by_id(id: int):
    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s", (id, ))
            return cursor.fetchone()


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id: int):
    url = find_by_id(id)

    try:
        with requests.get(url.name) as response:
            status_code = response.status_code
            response.raise_for_status()

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return render_template('show.html', ID=id, name=url.name,
                               created_at=url.created_at,
                               checks=find_checks(id)), 422

    with get_connected() as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO url_checks (url_id, status_code,\
                            created_at)\
                            VALUES (%s, %s, %s)",
                           (id, status_code,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            flash('Страница успешно проверена', 'alert-success')

    return redirect(url_for('one_url', id=id))


def find_checks(url_id: int):
    url_checks = []

    with get_connected() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("SELECT * FROM url_checks WHERE url_id = %s\
                           ORDER BY id DESC",
                           (url_id, ))
            url_checks.extend(cursor.fetchall())

    return url_checks
