const fs = require('fs');

/* function range(size, startAt = 0) {
    return [...Array(size).keys()].map(i => i + startAt);
} */

function range(stopAt, startAt = 0, _step = 1) {
    return Array(Math.ceil((stopAt - startAt) / _step)).fill(startAt).map((x, y) => x + y * _step)
}

function storeUintArr(arr, myFilePath='./arr') {
    fs.writeFile(
        myFilePath, 
        JSON.stringify(arr), 
        {
            encoding: "utf8",
            flag: "w",
            mode: 0o666
        },
        (err) => {
            if (err)
                console.log(err);
            else {
                console.log("File written successfully\n");
            }
        }
    );
}

exports.range = range;
exports.storeUintArr = storeUintArr;
