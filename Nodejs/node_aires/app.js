// Import express
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs')
const stream = require('stream');

// Import dotenv
require('dotenv').config();

// Import multer for handling files
const multer = require('multer');

// Import tensorflow
const tf = require('@tensorflow/tfjs');
// Load the binding:
require('@tensorflow/tfjs-node');

// Load model
const pathToModels = '/home/node/app/aires_models';
//const model1D = await tf.loadLayersModel(`${pathToModels}/model_1D_multi_input_js/model.json`);
//const model2D = await tf.loadLayersModel(`${pathToModels}/model_2D/model.json`);

// CORS policy
const cors = require('cors');

// Custom imports
const read_h5 = require('./utils/read_hdf5');
const function_1D = require('./utils/function_1d');
const parse_jpg = require('./utils/parse_jpg');
const utils = require('./utils/other_functions');


// Instantiate the express app
const app = express(); 
var router = express.Router();

// Use CORS
app.use(cors());

// Set in-memory storage
// https://github.com/expressjs/multer#memorystorage
const storage = multer.memoryStorage();
const upload = multer({ storage: storage }).single('file');

// BASE URL
const baseUrl = process.env.NODE_BASE_URL || '/node_aires'; 

// Using bodyParser to parse the body
/** 
 * In order to parse the file upload request posted to the file handler route, you need to make use of the body-parser module. 
 * So, require the body-parser module and use it across the application.
*/
app.use(bodyParser.urlencoded({extended: true})); 
app.use(bodyParser.json());


// Method for handling and allowing the request TO the server
app.use(
    (req, res, next) => {
        res.setHeader('Access-Control-Allow-Origin', "*"); // Allow all items

        res.setHeader(
            "Allow-Control-Allow-Headers", 
            "Origin, X-Requested-With, Access-Control-Allow-Headers, Content-Type, Accept"
            ); // Allow certain headers; disabled for now

        res.setHeader(
            'Access-Control-Allow-Methods', 
            "POST, GET"
            ); // Allow certain HTTP request. We use PUT in upload.service.ts to upload data to server

        next(); // we must call it! otherwise we block the whole server
    }
);


/*
    ROUTES
*/
// Home route
router.get('/', 
    (req, res, next) => { 
        
        console.log("Server ready...");

        res.status(200).send("Hello from node_aires"); 
        next();   
    }
);

// 2D
router.post('/color2D', 
    upload, 
    async (req, res, err) => { 
        // Error handling
        /* if (err instanceof multer.MulterError) {
            // A Multer error occurred when uploading.
            res.status(400).send(`Multer Error while uploading file;\n${err}\nHave you sent the file as 'file'?\n`);
            return;
        } else if (err) {
            // An unknown error occurred when uploading.
            res.status(400).send(`Node Error while uploading file;\n${err}\n`);
            return ;
        } */
        
        // No error; continue;
        console.log('1D Path;\n\n')
        // Read file
        let _f; 
        let _filename;

        if (req.file) {
            _f = req.file;            
        } else if (req.files) {
            _f = req.files[0];
        } else {
            // No files
            res.status(200).send("No files sent");
        }
        // File name
        _filename = _f.originalname;
        console.log(`Analysing file ${_filename}`)

        console.log(`Uploaded ${_filename}; start processing...`)
        
        // Parse hdf5 
        try {
            const xrf = await read_h5.read_h5(_f);
            console.log(xrf);
            try {
                console.log('Applying TF model')
            } catch (error) {
                console.log(`Error while interpreting tensor;\n${error}\n`)
                res.status(400).send(`Error while interpreting tensor;\n${error}\n`);
                return;
            }

        } catch (error) {
            console.log(`Error while parsing hdf5;\n${error}\n`)
            res.status(400).send(`Error while parsing hdf5;\n${error}\n`);
            return;
        }
        
        /* let xrf = tf.tensor(
            
        ); */
        // obtain recolored


        // remove in the end
        res.status(200).send("Done!\n");
    }
)

// 1D
router.post('/color1D', 
    upload, 
    async (req, res, err) => { 
        console.log('1D Path;\n\n')
        // Read file
        let _f; 
        let _filename;

        if (req.file) {
            _f = req.file;            
        } else if (req.files) {
            _f = req.files[0];
        } else {
            // No files
            res.status(200).send("No files sent");
            return;
        }
        // File name
        _filename = _f.originalname;
        console.log(`Analysing file ${_filename}`)

        console.log(`Uploaded ${_filename}; start processing...`)
        
        // Handle 1D
        let img = await function_1D.handle_1d_recoloring(_f);
        img_shape = img.shape;
        console.log(`Returing img of shape ${img.shape}`)
        console.log(typeof img)
        console.log(`Average color: ${img.mean()}\nin 255 scale: ${tf.mul(255, img.mean())}`)
        
        // If img is a string, IT IS AN ERROR
        if (typeof img == "string") {
            res.status(400).send(`${img}`);
            return;
        }   
        
        // Store tensor -- DEBUG ONLY --
        //function_1D.storeTfTensor(img); // <<<<< OK

        let content = await tf.browser.toPixels(img);
        
        // Store arr -- DEBUG ONLY --
        //utils.storeUintArr(content);

        content = parse_jpg.uint8ClampedArrayToImage(
            input     = content, 
            _width    = img_shape[1], 
            _height   = img_shape[0], 
            _channels = 4, 
        );


        // Store image -- DEBUG ONLY --
        //parse_jpg.storeImg(content);

        // Create reply
        try {
            let img_filename = _filename.split('.')[0] + '.jpg';
            console.log(`Returning ${img_filename}`)
            let mimetype = 'image/jpeg';
            res.status(200);
            res.set({
                'Content-Type': mimetype,
                'Content-disposition': 'attachment;filename=' + img_filename,
                'Content-Length': content.length
            });
            // Send file as base64 
            const fileContents = content.jpeg().toBuffer()
            .then(
                (data) => {
                    const base64Data = data.toString('base64');

                    res.send(base64Data);
                    return;
                }
            ).catch(
                (error) => {
                    let err_mess = `Error while sending file;\n${error}`;
                    console.log(err_mess)
                    res.status(400).send(err_mess);
                    return;
                }
            );
            
        } catch (error) {
            let err_mess = `Error while sending file;\n${error}`;
            console.log(err_mess)
            res.status(400).send(err_mess);
            return;
        }
        
        console.log('Done.')
        return;
    }
)

// Set up router
app.use(baseUrl, router);

// Export it to server.js; we need to call the module.exports
module.exports = app; 
