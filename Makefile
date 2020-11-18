.PHONY: install run debug test lint

APP="whiteboard"
DIR="whiteboard/"

default: run

run:
	FLASK_APP=$(APP) FLASK_ENV=production flask run

debug:
	FLASK_APP=$(APP) FLASK_ENV=development flask run

test:
	PYTHONPATH=. pytest

coverage:
	coverage run -m pytest
	coverage report

lint:
	flake8 $(DIR)
