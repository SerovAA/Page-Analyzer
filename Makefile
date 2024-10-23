PORT ?= 8000
start:
	poetry run gunicorn --workers=5 --bind=0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app --debug run