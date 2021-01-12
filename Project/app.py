from flask import Flask 
from flask_httpauth import HTTPBasicAuth
from blueprints import blpr

app = Flask(__name__)
auth = HTTPBasicAuth()
app.register_blueprint(blpr, url_prefix="/courses")


if __name__ == '__main__':
    app.run(debug = True)
