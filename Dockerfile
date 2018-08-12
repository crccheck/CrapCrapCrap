FROM python:3.7-alpine
LABEL maintainer="c@crccheck.com"

RUN apk add --no-cache \
  # psycopg2
  postgresql-dev gcc musl-dev \
  # staticfiles build
  nodejs nodejs-npm make

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY package.json /app/package.json
RUN npm install --production
COPY . /app
RUN make build
RUN env $(cat example.env | xargs) ./manage.py collectstatic --noinput

EXPOSE 8000
HEALTHCHECK CMD nc -z localhost 8000
CMD waitress-serve --port=8000 crap.wsgi:application
