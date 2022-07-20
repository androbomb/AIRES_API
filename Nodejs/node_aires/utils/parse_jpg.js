const sharp = require('sharp')

function uint8ClampedArrayToImage(input, _width, _height, _channels) {
    const image = sharp(input, {
        // because the input does not contain its dimensions or how many channels it has
        // we need to specify it in the constructor options
        raw: {
            width: _width,
            height: _height,
            channels: _channels
        }
    });

    return image
}

function storeImg(img) {
    img.toFile(__dirname + '/recolored.jpg')
}

exports.uint8ClampedArrayToImage = uint8ClampedArrayToImage;
exports.storeImg = storeImg;