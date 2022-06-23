from flask_app import server
from settings import config

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT)