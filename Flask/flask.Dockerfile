# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

LABEL maintainer="bombini@fi.infn.it"

ENV WORKDIR_PATH /flask_app
WORKDIR $WORKDIR_PATH

RUN apt update && apt install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools 

# Upgrade pip & Install gunicorn 
RUN pip3 -q install pip --upgrade

COPY requirements.txt requirements.txt
#Installing python packages 
RUN pip3 install -r requirements.txt

COPY . .

#
ENV FLASK_PORT 5000
ENV GUNICORN_WORKERS_PER_CORE 1
ENV GUNICORN_WORKER_CLASS gthread
ENV GUNICORN_THREADS 4

CMD gunicorn -w ${GUNICORN_WORKERS_PER_CORE} --worker-class=${GUNICORN_WORKER_CLASS} --threads=${GUNICORN_THREADS} --limit-request-line=0 --access-logfile=- --log-file=- -b :${FLASK_PORT} wsgi:server

