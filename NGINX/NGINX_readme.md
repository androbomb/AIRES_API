## Use env vars in NGINX 

define the ```default.conf.template```, so that we can insert the ENV vars through docker-compose (since NGINX:1.19, [1]);

Use the 
```nginx
    location ${SUBROUTE}/ {

        proxy_pass ${NGINX_PROXY_PASS};

        ...
    }
```
Where ```NGINX_PROXY_PASS``` is the env variable for the public IP of the Host machine.


## Include multiple paths in NGINX

[2]

## How To Create a Self-Signed SSL Certificate for Nginx in Ubuntu

[3]

### Create the SSL Certificate


TLS/SSL works by using a combination of a public certificate and a private key. The SSL key is kept secret on the server. It is used to encrypt content sent to clients. The SSL certificate is publicly shared with anyone requesting the content. It can be used to decrypt the content signed by the associated SSL key.

We can create a self-signed key and certificate pair with OpenSSL in a single command:
```bash
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048  \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt
```

or, in our case
```bash
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./cert/privkey.pem -out ./cert/cert.pem
```

You will be asked a series of questions. Before we go over that, let’s take a look at what is happening in the command we are issuing:

    - openssl: This is the basic command line tool for creating and managing OpenSSL certificates, keys, and other files.
    - req: This subcommand specifies that we want to use X.509 certificate signing request (CSR) management. The “X.509” is a public key infrastructure standard that SSL and TLS adheres to for its key and certificate management. We want to create a new X.509 cert, so we are using this subcommand.
    - -x509: This further modifies the previous subcommand by telling the utility that we want to make a self-signed certificate instead of generating a certificate signing request, as would normally happen.
    - -nodes: This tells OpenSSL to skip the option to secure our certificate with a passphrase. We need Nginx to be able to read the file, without user intervention, when the server starts up. A passphrase would prevent this from happening because we would have to enter it after every restart.
    - -days 365: This option sets the length of time that the certificate will be considered valid. We set it for one year here.
    - -newkey rsa:2048: This specifies that we want to generate a new certificate and a new key at the same time. We did not create the key that is required to sign the certificate in a previous step, so we need to create it along with the certificate. The rsa:2048 portion tells it to make an RSA key that is 2048 bits long.
    - -keyout: This line tells OpenSSL where to place the generated private key file that we are creating.
    - -out: This tells OpenSSL where to place the certificate that we are creating.

As we stated above, these options will create both a key file and a certificate. We will be asked a few questions about our server in order to embed the information correctly in the certificate.

Fill out the prompts appropriately. The most important line is the one that requests the Common Name (e.g. server FQDN or YOUR name). You need to enter the domain name associated with your server or, more likely, your server’s public IP address.

-----
Refs. 

[1] https://github.com/docker-library/docs/tree/master/nginx#using-environment-variables-in-nginx-configuration

[2] http://nginx.org/en/docs/ngx_core_module.html#include, https://serverfault.com/questions/707955/nginx-split-large-configuration-file

[3] https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04