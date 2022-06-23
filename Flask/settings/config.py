import os
from dotenv import load_dotenv
load_dotenv()

HOST = os.environ.get('FLASK_HOST')
PORT = int(os.environ.get("FLASK_PORT", 5999))