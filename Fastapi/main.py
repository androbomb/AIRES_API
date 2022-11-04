from fastapi import FastAPI, Request,  File, UploadFile

# Env import
import os
from dotenv import load_dotenv
load_dotenv()

# File utils
import base64
import datetime
import io

# Custom utils
from utils.function_2d import handle_2d_recoloring
from utils.function_1d import handle_1d_recoloring
from utils.other_functions import np_to_pil, create_response

ROOT_PATH = os.environ.get("FASTAPI_BASE_URL")

# CORS
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*" # allow all
]

# App definition
app = FastAPI()

# CORS set
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST"
    ],
    allow_headers=["*"],
)

# Hello world part
@app.get(f"{ROOT_PATH}/")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

#####################################à
# Three API routes

# 2D 
@app.post(f"{ROOT_PATH}/color2D")
async def color_2d(file: UploadFile = File(...)):
    try:
        print('File Arrived')

        f = await file.read()
        decoded = f
        # set filename
        try:
            file_name = file.filename
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
@app.post(f"{ROOT_PATH}/color1D")
async def color_1d(file: UploadFile = File(...)):
    try:
        print('File Arrived')

        f = await file.read()
        decoded = f
        # set filename
        try:
            file_name = file.filename
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

# single pixel 
@app.post(f"{ROOT_PATH}/colorpixel")
async def color_singlepixel(file: UploadFile = File(...)):
    try:
        print('File Arrived')

        f = await file.read()
        decoded = f
        # set filename
        try:
            file_name = file.filename
        except:
            file_name = ''
        print('File Decoded')

        # obtain recolored
        rgb = handle_1d_recoloring(decoded, single_pixel=True)
        print('File recolored')

        return {
            "R": rgb[0],
            "G": rgb[1],
            "B": rgb[2]
        }

    except Exception as e:
        print(f'Error;\n{e}\n\n')
        error_text_to_return = f"""
        Error while recoloring:
        {e}
        """
        return error_text_to_return

    return 'Error'
