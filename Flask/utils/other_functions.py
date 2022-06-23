from io import StringIO, BytesIO
import PIL
import numpy as np
from flask import send_file, make_response

# utils
import base64

def np_to_pil(matrix):
    # Normalize data
    matrix = matrix/np.max(matrix)
    # return to 255
    matrix = matrix*255
    # Convert to uint8
    matrix = matrix.astype('uint8')
    #return obj
    matrix = PIL.Image.fromarray(
        matrix
    )

    # Fix problem in wrinting matrix image in PIL
    if matrix.mode != 'RGB':
        matrix = matrix.convert('RGB')

    return matrix

def create_response(rgb, file_name='recolored'):
    # send jpeg
    img_io = BytesIO()
    rgb.save(img_io, 'JPEG', quality=95)
    # actual binaries
    img_bytes = img_io.getvalue()
    #base64 encoded object to use in response
    image = base64.b64encode(img_bytes).decode("utf-8")

    # creating response
    response = make_response(image)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename=f'recolored_{file_name}.jpg')

    return response