import os
import psycopg2
import requests

from flask import Flask, request, render_template, flash, redirect, url_for

from .database import (use_connection, find_all_urls, find_by_id,
                       find_by_name, add_check, find_checks, add_url)
from .url_check import validate_url, normalize_url
from .parser import get_seo_data


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
@use_connection
def get_urls_post(cursor):
    url_from_request = request.form.to_dict().get('url', '')
    errors = validate_url(url_from_request)
    url_info = ''

    if len(errors) != 0:
        flash('Некорректный URL', 'alert-danger')
        return render_template('index.html'), 422

    new_url = normalize_url(url_from_request)

    try:
        add_url(cursor, new_url)
        url_info = cursor.fetchone()

    except psycopg2.errors.UniqueViolation:
        url = find_by_name(new_url)
        url_id = url.id
        flash('Страница уже существует', 'alert-warning')

    if url_info:
        url_id = url_info.id
        flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_one_url', id=url_id))


@app.route('/urls', methods=['GET'])
def get_urls():
    urls = find_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_one_url(id: int):
    url = find_by_id(id)

    if url is None:
        flash('Такой страницы не существует', 'alert-warning')
        return redirect(url_for('index'))

    return render_template('show.html', ID=id, name=url.name,
                           created_at=url.created_at,
                           checks=find_checks(id))


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

    h1, title, description = get_seo_data(response.text)
    add_check(id, status_code, h1, title, description)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('get_one_url', id=id))
