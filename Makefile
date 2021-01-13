.PHONY: install run debug test lint

APP="whiteboard"
DIR="whiteboard/"

default: debug

debug:
	FLASK_APP=$(APP) FLASK_ENV=development flask run

test:
	PYTHONPATH=. pytest

coverage:
	coverage run -m pytest
	coverage report

lint:
	flake8 $(DIR)

build:
	@docker build --pull -t $(APP) .

run: build
	docker-compose up -d

clean:
	@docker stop $(APP) || true
	@docker rm $(APP) || true

create-venv:
	python3 -m venv venv

recreate-venv:
	rm -r ./venv
	python3 -m venv venv

install:
	pip3 install -r requirements_to_run.txt

install-dev:
	pip3 install -r requirements_to_dev.txt

init_db:
	FLASK_APP=$(APP) FLASK_ENV=development flask init-db
