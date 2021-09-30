.PHONY: install run debug test lint

APP="whiteboard"
DIR="whiteboard/"

default: debug

debug:
	FLASK_APP=$(APP) FLASK_ENV=development flask run

build:
	@docker build --pull -t $(APP) .

run: build
	docker-compose up -d

clean:
	@docker-compose down || true
	@docker stop $(APP) || true
	@docker rm $(APP) || true

test:
	python -m pytest

lint:
	python -m flake8
	python -m mypy --exclude instance/ .

coverage:
	python -m pytest --cov --cov-fail-under=100

pre-commit:
	pre-commit run --all-files

install:
	pip3 install -r requirements.txt

install-dev: install
	pip3 install -r requirements_dev.txt

init_db:
	FLASK_APP=$(APP) FLASK_ENV=development flask init-db

scss:
	pyscss whiteboard/assets/scss/style.scss > whiteboard/static/css/style.css
