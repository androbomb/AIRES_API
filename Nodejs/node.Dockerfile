# https://malcoded.com/posts/angular-docker/
FROM node:18.5 AS node 

LABEL maintainer="bombini@fi.infn.it"

WORKDIR /home/node/app
COPY package*.json ./

RUN npm install jsfive debug express cors dotenv multer numjs @tensorflow/tfjs @tensorflow/tfjs-node h5wasm sharp

# For development
RUN npm install -g nodemon

CMD nodemon -L server.js
# For deployement
#CMD [ "node", "server.js"]
