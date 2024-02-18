FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/sqlalchemy

RUN apt-get update \
  && apt-get install -y --no-install-recommends postgresql-client libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY ./requirements.txt usr/src/requirements.txt

RUN pip install -r usr/src/requirements.txt

COPY . /usr/src/sqlalchemy
