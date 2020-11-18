FROM python:slim

COPY requirements_to_run.txt /
RUN pip3 install -r /requirements_to_run.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]
