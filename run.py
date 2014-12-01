from app.factory import create_app
import os

app = create_app(os.getcwd() + '/config.py')

app.run(host='127.0.0.1', port=3000, debug=True)
