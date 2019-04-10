FROM python:3.7-alpine
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev
WORKDIR /app
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt
COPY . /app
