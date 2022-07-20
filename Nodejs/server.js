const http = require('http');
const debug = require('debug')("node-angular");
// Import the exported app object from the the app.js
const app = require('./node_aires/app');

// Import dotenv
require('dotenv').config();
/**
 * SERVER PORT NUMBER
 */
// Standard port during development is 3000; if we are in development mode we inherit it into process.env.PORT
const portNumber = process.env.NODE_PORT || 8081; 

// We will thus add an extra security step through a function that checks if the port is valid;
const normalizePort = val => {
    var port = parseInt(val, 10);

    if(isNaN(port)) {
        // named pipe; it is triggered if the pipe called by val IS NOT A NUMBER
        return val; 
    }

    if (port>=0) {
        // port number
        return port;
    }

    // If neither the previous two are triggered, raise an error.
    return false;
};

// set the port
const port = normalizePort(portNumber);
app.set("port", port);



// We now add two functions that handles the error and listening;
// ONERROR
const onError = error => {
    // We check if the system raises an error via the Node.js error.syscall ethod
    if (error.syscall !== "listen") {
        throw error; // generate the error
    }

    const bind = typeof port === "string" ? ("pipe " + port) : ("port " + port); // Checks wheter we have a port number or a stringed pipe

    // We make two cases more readable: if we have an user with not enough privileges, or if we are trying to use an already used port/pipe
    switch (error.code) {
        case "EACCES":
            console.error(bind + " requires elevated privileges"); 
            process.exit(1);
            break;
        case "EADDRINUSE":
            console.error(bind + " is already in use");
            process.exit(1);
            break;
        default:
            throw error;
    }
};
// ONLISTENING
const onListening = () => {
    const addr = server.address();
    const bind = typeof port === "string" ? ("pipe " + port) : ("port " + port); // Checks wheter we have a port number or a stringed pipe
    debug("Listening on " + bind);
};



// Instead of creating it here, we employ the express from app.js and call it via
const server = http.createServer(app);

// Set the way server handles error and listening
server.on("error", onError);
server.on("listening", onListening);

// To activate the server, you have to call the .listen() method specifyng the port number
server.listen(portNumber); 
