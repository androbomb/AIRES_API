const fs = require('fs');
// Import tensorflow
const tf = require('@tensorflow/tfjs');
// Load the binding:
require('@tensorflow/tfjs-node');
const pathToModels = '/home/node/app/aires_models';

const { performance } = require('node:perf_hooks');

// Numjs aka np for js = nj
const nj = require('numjs');

// Custo imports
const read_h5 = require('./read_hdf5');
const utils = require('./other_functions');
const preprocessor = require('./preprocessing');


async function recolor_2D(xrf) {
    try {
        console.log('Loading 2D TF model')
        const model = await tf.loadLayersModel(`file://aires_models/model_2D_js/model.json`);
        console.log('Retrieving input size for loaded model\n')

        let pixels;

        // Get info from model
        try {
            _config = model.getConfig();
            _inputs = model.inputs[0].shape;
            max_h = _inputs[1];
            max_w = _inputs[2];
            n_bins = _inputs[_inputs.length -1];
            
            // get model name
            _model_name = model.name;

            console.log(`Using model ${_model_name};`)
            console.log(`Inputs: ${_inputs}`)
            //console.log(`Number of bins in Model input: ${n_bins}`);
        } catch (error) {
            console.log('Model Configs not found. Getting from hardcoded\n')
            n_bins = 500;
            max_h = 384
            max_w = 288
            _model_name = ''
        }
        
        // Preprocessing
        try {
            const oldBins = xrf.shape[xrf.shape.length -1]
            console.log(`XRF Image has ${oldBins} Energy channels`)
            // rebin if needed
            if (oldBins > n_bins) {
                const original_shapes = [xrf.shape[0], xrf.shape[1], n_bins];
                let rebinned = tf.zeros(
                    original_shapes
                );
                //console.log(rebinned.shape)
                divisor = parseInt(
                    oldBins / n_bins
                );
                
                //console.log(`Divisor: ${divisor}`);
                
                const iter_range = utils.range(divisor);//[...Array(divisor).keys()];

                for (let step of iter_range) {
                    //_start = performance.now()
                    //console.log(`Step ${step}`)

                    let arr_idxs = utils.range(stopAt = oldBins, startAt = step, _step = divisor );
                    //console.log(arr_idxs.length)
                    //console.log(arr_idxs[arr_idxs.length-1])
                    let indices = tf.tensor1d(arr_idxs, 'int32');
                    let gathered = tf.gather(
                        xrf,
                        indices=indices,
                        axis=2
                    );
                    //console.log(gathered.shape)
                    rebinned = tf.add(rebinned, gathered);
                    //console.log(rebinned.shape)
                    

                    //console.log(`Step ${step} ended in ${(performance.now() - _start) } ms`)
                }

                pixels = await tf.image.resizeBilinear(
                    rebinned, 
                    size=[max_h, max_w]
                )
                
                pixels = await tf.expandDims(pixels)
                //console.log(pixels.shape)

                console.log('Rebinning done')
            } else {
                pixels = await tf.image.resizeBilinear(
                    xrf, 
                    size=[max_h, max_w]
                ) 
                pixels = await tf.expandDims(pixels)
                console.log('No Rebinning ')
            }

            console.log(`New pixels shape: ${pixels.shape}`);
            
            // Preprocessing
            try {
                console.log('Prerocessing')
                let pixels_normalized = await preprocessor.transform2D(pixels);
                
                console.log(`Avg pixels_normalized count: ${pixels_normalized.mean()}`)
                console.log(`New pixels_normalized shape: ${pixels_normalized.shape}`);

                try {
                    console.log('Predicting')
                    
                    rgb_pred = model.predict(pixels_normalized);
                    rgb_pred = await rgb_pred.reshape(
                        [
                            rgb_pred.shape[1], rgb_pred.shape[2], rgb_pred.shape[3]
                        ]
                    )
                    
                    console.log(`Prediction done. Image size ${rgb_pred.shape}`);
                    console.log(`Avg predicted color: ${rgb_pred.mean(axis=[0,1])}`)
                    return rgb_pred;

                } catch (error) {
                    message = `Error while predicting;\n${error}\n`
                    console.log(message)
                    return message;
                }

            } catch (error) {
                message = `Error while preprocessing rebinned tensor;\n${error}\n`
                console.log(message)
                return message;
            }

        } catch (error) {
            message = `Error while rebinning tensor;\n${error}\n`
            console.log(message)
            return message;
        }
        
    } catch (error) {
        message = `Error while loading model;\n${error}\n`
        console.log(message)
        return message;
    }
}

async function handle_2d_recoloring(_f) {
    // Parse hdf5 
    try {
        const xrf = await read_h5.read_h5(_f);
        console.log(xrf);

        let img = await recolor_2D(xrf);

        return img;

    } catch (error) {
        message = `Error while parsing hdf5;\n${error}\n`
        console.log(message)
        return message;
    }
}


exports.handle_2d_recoloring = handle_2d_recoloring;
