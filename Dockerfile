FROM python:3.6-alpine
LABEL maintainer="c@crccheck.com"

RUN apk add --no-cache \
  # psycopg2
  postgresql-dev gcc musl-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000

# FIXME use a real web server
CMD python manage.py runserver
