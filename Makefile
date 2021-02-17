.PHONY: install run debug test lint

APP="whiteboard"
DIR="whiteboard/"

default: debug

debug:
	FLASK_APP=$(APP) FLASK_ENV=development flask run

test:
	pytest

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
	@docker-compose down || true
	@docker stop $(APP) || true
	@docker rm $(APP) || true

create-venv:
	python3 -m venv venv

recreate-venv:
	rm -r ./venv
	python3 -m venv venv

install:
	pip3 install -r requirements.txt

install-dev: install
	pip3 install -r requirements_dev.txt

init_db:
	FLASK_APP=$(APP) FLASK_ENV=development flask init-db

scss:
	pyscss whiteboard/assets/scss/style.scss > whiteboard/static/css/style.css
