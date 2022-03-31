FROM python:3-slim-bullseye

ENV PATH="/home/worker/.local/bin:${PATH}"

RUN adduser --disabled-password --gecos "" --home /home/worker --shell /bin/bash worker
USER worker

WORKDIR /home/worker

COPY --chown=worker:worker . .
RUN pip install --user --upgrade pip && pip install --user -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
