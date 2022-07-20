const fs = require('fs')
// Import tensorflow
const tf = require('@tensorflow/tfjs');
// Load the binding:
require('@tensorflow/tfjs-node');


// From Buffer to ArrauBuffer
function fromBufferToArrayBuffer(buf) {
    const ab = new ArrayBuffer(buf.length);
    const view = new Uint8Array(ab);
    for (let i = 0; i < buf.length; ++i) {
        view[i] = buf[i];
    }
    return ab;
}

// From ArrayBuffer to Buffer
function fromArrayBufferToBuffer(ab) {
    const buf = Buffer.alloc(ab.byteLength);
    const view = new Uint8Array(ab);
    for (let i = 0; i < buf.length; ++i) {
        buf[i] = view[i];
    }
    return buf;
}

async function read_h5_jsfive(file) {
    // Import library
    const hdf5 = await import("jsfive");
    const Buffer = require('node:buffer');
    // PArsing req
    const filename = file.originalname;
    const buffer = await Buffer.Buffer.from(file.buffer);
    const arrayBuf = fromBufferToArrayBuffer(buffer);
    console.log(`Array buffer created.`)
    let f = new hdf5.File(arrayBuf, filename);
    console.log(`Opened file ${filename};\nKeys: ${f.keys}`);

    // Get dataset
    let data = await f.get("img");//.value
    console.log(`Got dataset;\nattrs:`)
    console.log(data.attrs);
    console.log(`\nGot dataset;\nvalues:`);
    console.log(data.dataobjects);

    console.log(data)
    


    return data.to_array();
} 

async function read_h5_h5wasm(file) {
    // Import library
    const hdf5 = await import("h5wasm");
    await hdf5.ready;
    const Buffer = require('node:buffer');
    // PArsing req
    const data_filename = file.originalname;
    const buffer = await Buffer.Buffer.from(file.buffer);
    const ab = buffer;
    //Init h5 file
    hdf5.FS.writeFile(data_filename, new Uint8Array(ab));
    let f = new hdf5.File(data_filename, "r");
    
    // Get dataset
    let data = await f.get("img");
    console.log(`Got dataset;\nMetadata:`)
    const metadata = data.metadata
    console.log(metadata);
    console.log(`\nshape: ${metadata.shape}`);
    const data_shape = await metadata.shape;
    const data_arr   = await new Float32Array(data.value);
    //console.log(data_arr);

    //console.log(data)

    console.log('Creating TF tensor');

    const xrf = tf.tensor(
        value=data_arr,
        shape=data_shape
    );
    console.log('Returning')

    await f.close()
    // remove file
    fs.unlinkSync(data_filename)
    // Return tensor
    return xrf;
} 

exports.read_h5 = read_h5_h5wasm;