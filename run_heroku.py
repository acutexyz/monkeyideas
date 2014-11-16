from app.factory import create_app
import os

app = create_app(os.getcwd() + '/config.py')