import numpy as np
import keras
import tensorflow as tf
import h5py
from io import BytesIO

# utils
from utils.preprocessor_classes import Preprocessor, Preprocessor2D

# Env import
import os
from dotenv import load_dotenv
load_dotenv()

NAME_OF_IMAGE_IN_FILE = os.environ.get('NAME_OF_IMAGE_IN_FILE')
PATH_TO_AIRES_MODEL_1D= './AIRES_MODELS/' + os.environ.get('NAME_AIRES_MODEL_1D') 

def handle_1d_recoloring(received_file, single_pixel = False):
    rgb = np.array([])
    
    print(f'File type: {type(received_file)}')
    loaded_hf = h5py.File(
        BytesIO(received_file), 
        'r'
    )
    print(f'Keys: {loaded_hf.keys()}')

    try:
        # Create np from h5
        xrf = np.array(
            loaded_hf.get(NAME_OF_IMAGE_IN_FILE)
        )

        print(f'Shape of the uploaded XRF raw data: {xrf.shape}\n')
        
        # recolor xrf into rgb
        # if single pixel
        if single_pixel:
            rgb = recolor_pixel(xrf)
        # Normal image
        else: 
            rgb = recolor_1d(xrf)

        # return rgb
        return rgb

    except Exception as e:
        err=e
        print(f'Error while loading hdf5\n{e}')
    
    # return error message
    return f'Error;\n{err}\n'

def recolor_1d(xrf):
    try:
        print('Importing model')
        path_to_model = PATH_TO_AIRES_MODEL_1D
        print(f'Path to model exists? {os.path.exists(path_to_model)}')
        model = keras.models.load_model(path_to_model)

        try:
            print('Retrieving input size for loaded model\n')
            _config = model.get_config() # Returns pretty much every information about your model
            n_bins = _config["layers"][0]["config"]["batch_input_shape"][-1]

            # get model name
            _model_name = _config['name']
            print(f'Using model {_model_name}')
        except:
            print('Not found. Getting from hardcoded\n')
            n_bins = 500
            _model_name = ''

        try:
            # Rebin if needed
            if xrf.shape[-1] > n_bins:
                original_shapes = [xrf.shape[0], xrf.shape[1], n_bins]
                rebinned = np.zeros(original_shapes)
                divisor = int(
                    xrf.shape[-1] // n_bins
                )

                from tqdm import trange 
                for step in trange(divisor, desc="Rebinning"):
                    rebinned += xrf[:,:,step::divisor]
                
                pixels = rebinned.reshape ((-1, n_bins))
            else:
                pixels = xrf.reshape ((-1, n_bins))

            preprocessor = Preprocessor(pixels)
            pixels_normalized = preprocessor.transform(pixels)
            # Custom models
            if len(model.inputs)==2:
                rgb_pred = model.predict([pixels_normalized, pixels]).reshape (xrf[:,:,:3].shape)
            # Normal models
            else:
                rgb_pred = model.predict(pixels_normalized).reshape (xrf[:,:,:3].shape)

            return rgb_pred
        except Exception as e:
            print(f'Error in recoloring process;\n{e}\n')

    except Exception as e:
        print('Error while importing model.\n{e}\n')

def recolor_pixel(xrf):
    try:
        print('Importing model')
        path_to_model = PATH_TO_AIRES_MODEL_1D
        print(f'Path to model exists? {os.path.exists(path_to_model)}')
        model = keras.models.load_model(path_to_model)

        try:
            print('Retrieving input size for loaded model\n')
            _config = model.get_config() # Returns pretty much every information about your model
            n_bins = _config["layers"][0]["config"]["batch_input_shape"][-1]

            # get model name
            _model_name = _config['name']
            print(f'Using model {_model_name}')
        except:
            print('Not found. Getting from hardcoded\n')
            n_bins = 500
            _model_name = ''
        
        try:
            # Rebin if needed
            if len(xrf) > n_bins:
                rebinned = np.zeros(n_bins)

                divisor = int(
                    len(xrf) // n_bins
                )

                from tqdm import trange 
                for step in trange(divisor, desc="Rebinning"):
                    rebinned += xrf[step::divisor]
                
                pixels = rebinned.reshape ((-1, n_bins))
            else:
                pixels = xrf.reshape ((-1, n_bins))

            preprocessor = Preprocessor(pixels)
            pixels_normalized = preprocessor.transform(pixels)
            # Custom models
            if len(model.inputs)==2:
                rgb_pred = model.predict([pixels_normalized, pixels])[0]
            # Normal models
            else:
                rgb_pred = model.predict(pixels_normalized)[0]

            return rgb_pred

        except Exception as e:
            print(f'Error in recoloring process;\n{e}\n')

    except Exception as e:
        print('Error while importing model.\n{e}\n')
