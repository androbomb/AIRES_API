# Base flask imports
import imp
from flask import Flask
from flask import request, send_file, make_response, jsonify
from flask_cors import CORS

# Standard inputs
import PIL
import numpy as np
from io import BytesIO, StringIO

# Env import
import os
from dotenv import load_dotenv
load_dotenv()

# File utils
import base64
import datetime
import io

# Custom utils
from utils.wsgi_middleware import PrefixMiddleware
from utils.function_2d import handle_2d_recoloring
from utils.function_1d import handle_1d_recoloring
from utils.other_functions import np_to_pil, create_response



##################################
# app definition
server = Flask(__name__)
# Allow CORS (Cross Origin Resources Sharing)
CORS(server)

"""Subrouting
StackOverflow https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes/18969161#18969161

# Proxying requests to the app

If you will be running your Flask application at the root of its WSGI container and proxying requests to it 
(for example, if it's being FastCGI'd to, or if nginx is proxy_pass-ing requests for a sub-endpoint
to your stand-alone uwsgi / gevent server) then you can either:

    1. Use a Blueprint
    2. or use the DispatcherMiddleware from werkzeug to sub-mount your application in the stand-alone WSGI server you're using.

Officlal docs: https://flask.palletsprojects.com/en/2.1.x/config/#builtin-configuration-values

    APPLICATION_ROOT

        Inform the application what path it is mounted under by the application / web server. 
        This is used for generating URLs outside the context of a request (inside a request, 
        the dispatcher is responsible for setting SCRIPT_NAME instead; 
        see Application Dispatching for examples of dispatch configuration).

        Will be used for the session cookie path if SESSION_COOKIE_PATH is not set.

        Default: '/'

"""
##################################
# subrouting
BASE_URL = str( os.environ.get('FLASK_BASE_URL') )
server.config['APPLICATION_ROOT'] = BASE_URL
server.wsgi_app = PrefixMiddleware(app=server.wsgi_app, prefix=BASE_URL)

@server.route('/')
def hello_world():
    return 'hello world from flask_aires!'

#####################################à
# Three API routes

# 2D 
@server.route('/color2D', methods=['POST'])
def color_2d():
    if request.method =='POST':
        try:
            print('File Arrived')

            f = request.files['file'].read()
            decoded = f
            # set filename
            try:
                file_name = request.files['file'].filename
            except:
                file_name = ''
            print('File Decoded')

            # obtain recolored
            rgb = handle_2d_recoloring(decoded)
            print('File recolored')

            # np to pil
            rgb = np_to_pil(rgb)
            print('File jpg created')

            # create response to return
            response = create_response(rgb=rgb, file_name=file_name)
            print('Created response;')

            return response

        except Exception as e:
            print(f'Error;\n{e}\n\n')
            error_text_to_return = f"""
            Error while recoloring:
            {e}
            """
            return error_text_to_return

    return 'Error'

# 1D 
@server.route('/color1D', methods=['POST'])
def color_1d():
    if request.method =='POST':
        try:
            print('File Arrived')

            f = request.files['file'].read()
            decoded = f
            # set filename
            try:
                file_name = request.files['file'].filename
            except:
                file_name = ''
            print('File Decoded')

            # obtain recolored
            rgb = handle_1d_recoloring(decoded)
            print('File recolored')

            # np to pil
            rgb = np_to_pil(rgb)
            print('File jpg created')

            # create response to return
            response = create_response(rgb=rgb, file_name=file_name)
            print('Created response;')

            return response

        except Exception as e:
            print(f'Error;\n{e}\n\n')
            error_text_to_return = f"""
            Error while recoloring:
            {e}
            """
            return error_text_to_return

    return 'Error'

# Single Pixel
@server.route('/colorpixel', methods=['POST'])
def color_singlepixel():
    if request.method =='POST':
        try:
            print('File Arrived')

            f = request.files['file'].read()
            decoded = f
            # set filename
            try:
                file_name = request.files['file'].filename
            except:
                file_name = ''
            print('File Decoded')

            # obtain recolored
            rgb = handle_1d_recoloring(decoded, single_pixel=True)
            print('File recolored')

            response = make_response(
                    jsonify(
                        R=rgb[0],
                        G=rgb[1],
                        B=rgb[2]
                ),
                200
            )

            return response

        except Exception as e:
            print(f'Error;\n{e}\n\n')
            error_text_to_return = f"""
            Error while recoloring:
            {e}
            """
            return error_text_to_return

    return 'Error'