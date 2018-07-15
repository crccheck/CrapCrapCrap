FROM python:3.6-alpine
LABEL maintainer="c@crccheck.com"

RUN apk add --no-cache \
  # psycopg2
  postgresql-dev gcc musl-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
RUN ./manage.py collectstatic --noinput

EXPOSE 8000
HEALTHCHECK CMD nc -z localhost 8000
CMD waitress-serve --port=8000 crap.wsgi:application
