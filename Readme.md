# Artificial Intelligence for digital REStoration of Cultural Heritage (AIRES) API

This is the GitHub repository of the code employed in Section 5 of the Article

>**A cloud-native application for digital restoration of Cultural Heritage using nuclear imaging: the AIRES-CH project App**,
Alessandro Bombini, Fernando Garcìa Avello-Bofìas, Chiara Ruberto, Francesco Taccetti

submitted to MDPI/computers as extended version of the conference paper:

>Bombini, A., Anderlini, L., dell’Agnello, L., Giacomini, F., Ruberto, C., Taccetti, F. (2022). **Hyperparameter Optimisation of Artificial Intelligence for Digital REStoration of Cultural Heritages (AIRES-CH) Models**. In: Gervasi, O., Murgante, B., Misra, S., Rocha, A.M.A.C., Garau, C. (eds) Computational Science and Its Applications – ICCSA 2022 Workshops. ICCSA 2022. Lecture Notes in Computer Science, vol 13377. Springer, Cham. https://doi.org/10.1007/978-3-031-10536-4_7

winner of the best paper award at the *Workshop on Advancements in Applied Machine-learning and Data Analytics* (AAMDA) workshop at the the *22nd International Conference on Computational Science and Its Applications* (ICCSA 2022).

This repository build the RESTful API for serving the trained AIRES-CH DNN models. 

The AIRES-CH DNNs are accessible for inference via the THESPIAN-XRF web app; the DNNs are furnished via a RESTful API offering three routes:
1. `/1D/`, to perform the recolouring inference using the 1D model described in sec. 3.3.2; 
2. `/2D/`, to perform the recolouring inference using the 2D model described in sec. 3.2; 
3. `/pixel/`, to perform single-pixel inference; this branch was developed for the goal of offering real-time recolouring during measurements. 

Getting started
Veloci Raptor
03/14/15
As easily understandable,  one of the main features we expect from our
RESTful API (and DNN models) is a fast reply time (a short inference time). In order to optimise this aspect, we developed three APIs, with three different frameworks: FastAPI, Flask and NodeJS. 

For more details, we refer to the aforementioned papers.

------------------

## Extra: Deployement infos

### Env variables


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