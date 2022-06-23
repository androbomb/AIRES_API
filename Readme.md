# Artificial Intelligence for digital REStoration of Cultural Heritage (AIRES) API


## Env variables


#### NGINX
NGINX_HOST_PORT=8443
NGINX_CERT=./NGINX/cert
NGINX_ROOT=./NGINX

##### Flask4NGINX vars
FLASK_BASE_URL=/flask_aires
NGINX_PROXY_PASS_FLASK=http://ip

##### CROW4NGINX vars


#### FLASK

##### In App
FLASK_PORT=5999
FLASK_HOST=0.0.0.0

NAME_OF_IMAGE_IN_FILE='img'

##### In Dockers
FLASK_ROOT_DIR=./Flask
WORKDIR_PATH=/flask_app

GUNICORN_WORKERS_PER_CORE=1
GUNICORN_WORKER_CLASS=gthread
GUNICORN_THREADS=4

#### CROW

#### AIRES MODELS
PATH_TO_AIRES_MODELS=./AIRES_MODELS/
NAME_AIRES_MODEL_1D=model_1D_multi_input.h5
NAME_AIRES_MODEL_2D=model_2D.h5