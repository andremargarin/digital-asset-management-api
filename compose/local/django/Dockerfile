FROM python:3.7-alpine
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev zlib-dev jpeg-dev \
    && apk add postgresql-dev	    && apk add postgresql-dev \
    && apk add ffmpeg
WORKDIR /app
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt
COPY . /app
