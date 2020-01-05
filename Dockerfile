FROM python:3.8-alpine
LABEL maintainer="c@crccheck.com"

RUN apk add --no-cache \
  # psycopg2
  postgresql-dev gcc musl-dev \
  # staticfiles build
  nodejs nodejs-npm make \
  # Python dep: cryptography
  libffi-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip --disable-pip-version-check install -r requirements.txt
COPY package.json /app/package.json
RUN npm install
COPY . /app
RUN make build
RUN env $(cat example.env | xargs) ./manage.py collectstatic --noinput

EXPOSE 8000
HEALTHCHECK CMD nc -z localhost 8000
CMD daphne --port=8000 crap.wsgi:application
