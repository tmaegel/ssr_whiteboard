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
	@docker build -t $(APP) .

run:
	@docker run --rm --name $(APP) -p 127.0.0.1:8080:8080 -v ${PWD}/instance/:/app/instance/ -d $(APP)

clean:
	@docker stop $(APP) || true
	@docker rm $(APP) || true
