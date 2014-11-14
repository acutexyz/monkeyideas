from app.factory import create_app
import os

app = create_app(os.getcwd() + '/config.py')

app.run(host='0.0.0.0', port=3000, debug=True)