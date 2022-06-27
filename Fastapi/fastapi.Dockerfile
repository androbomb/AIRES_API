FROM python:3.9-slim-buster

LABEL maintainer="bombini@fi.infn.it"

ENV FASTAPI_WORKDIR_PATH /fastapi_app
WORKDIR $FASTAPI_WORKDIR_PATH

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
ENV FASTAPI_PORT 5998
ENV UVICORN_WORKERS 1
ENV FASTAPI_BASE_URL /fastapi_aires

# If running behind a proxy like Nginx or Traefik add --proxy-headers
#CMD uvicorn main:app --host 0.0.0.0 --port ${FASTAPI_PORT} --proxy-headers --workers ${UVICORN_WORKERS} --root-path ${FASTAPI_BASE_URL}
CMD uvicorn main:app --host 0.0.0.0 --port ${FASTAPI_PORT} --proxy-headers --workers ${UVICORN_WORKERS} 