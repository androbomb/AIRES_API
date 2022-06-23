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
PATH_TO_AIRES_MODEL_2D= './AIRES_MODELS/' + os.environ.get('NAME_AIRES_MODEL_2D') 

def handle_2d_recoloring(received_file):
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
        rgb = recolor_2d(xrf)

        # return rgb
        return rgb

    except Exception as e:
        err=e
        print(f'Error while loading hdf5\n{e}')
    
    # return error message
    return f'Error;\n{err}\n'

def recolor_2d(xrf):

    try:
        print('Importing model')
        path_to_model = PATH_TO_AIRES_MODEL_2D
        print(f'Path to model exists? {os.path.exists(path_to_model)}')
        model = keras.models.load_model(path_to_model)
        
        try:
            print('Padding')
            try:
                print('Retrieving input size for loaded model\n')
                _config = model.get_config() # Returns pretty much every information about your model
                _, max_h, max_w, n_bins = _config["layers"][0]["config"]["batch_input_shape"]

                # get model name
                _model_name = _config['name']
                print(f'Using model {_model_name}')
            except:
                print('Not found. Getting from hardcoded\n')
                max_h = 384
                max_w = 288
                n_bins = 500
                _model_name = ''
                
            # Apply same transformation as training dataset images
            img = np.moveaxis(xrf, 1, 0)

            # Rebin if needed
            if xrf.shape[-1] > n_bins:
                
                rebinned = np.zeros([img.shape[0], img.shape[1], n_bins])
                divisor = int(
                    xrf.shape[-1] // n_bins
                )
                from tqdm import trange 
                for step in trange(divisor, desc="Rebinning"):
                    rebinned += img[:,:,step::divisor]
                
                xrf_to_recolor = tf.image.resize_with_pad(
                    rebinned,
                    target_height=max_h, target_width=max_w
                ).numpy()
            elif xrf.shape[-1] == n_bins:
                xrf_to_recolor = tf.image.resize_with_pad(
                    img,
                    target_height=max_h, target_width=max_w
                ).numpy()

            # Add dummy direction for batch size
            xrf_to_recolor = np.array([xrf_to_recolor])

            # Preprocess data   
            try: 
                preprocessor = Preprocessor2D(xrf_to_recolor)
                xrf_to_recolor = preprocessor.transform(xrf_to_recolor)
            except Exception as e:
                print('Error while preprocessing XRF.\n')
                print(e)
            

            print('Recoloring')
            predicted_rgb = model.predict(xrf_to_recolor)[0]
            print(f'Prediction obtained; {predicted_rgb.shape}\n')

            # return rgb
            return predicted_rgb

        except:
            print('Error while recoloring.\n')
    except:
        print('Error while importing model.\n')