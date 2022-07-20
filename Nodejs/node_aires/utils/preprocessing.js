const tf = require('@tensorflow/tfjs');
// Load the binding:
require('@tensorflow/tfjs-node');

function transform1D(X) {
    let _X = X.transpose();
    const _mean = _X.mean(axis=0)
    const _std  = tf.moments(_X, axis=0).variance.sqrt(); //_X.std(axis=0)
    const _divisor = tf.add( _std, tf.ones(_std.shape) );
    
    //console.log(`Mean: ${_mean}`)
    //console.log(`Divisor: ${_divisor}`)
    // ((_X - _mean)/(_std + 1));
    _X = tf.sub(_X, _mean) 
    //console.log(`Transposed subtracted: ${_X}`);
    _X = _X.div( _divisor );
    //console.log(`Transposed normalized: ${_X}`);

    return _X.transpose();
}

exports.transform1D = transform1D;