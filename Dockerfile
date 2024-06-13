FROM python:3.11-slim-buster

WORKDIR /app

RUN pip install poetry==1.4.2

COPY  pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

ENV PYTHONPATH /app 

COPY . .

RUN poetry install --no-interaction --no-ansi

