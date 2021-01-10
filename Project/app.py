from flask import Flask 
from flask_httpauth import HTTPBasicAuth
from blueprints import blpr

def database_error():
    return jsonify(
        {
            "code": 500,
            "type": "DATABASE_ERROR",
        }
    )

app = Flask(__name__)
auth = HTTPBasicAuth()
app.register_blueprint(blpr, url_prefix="/courses")

#app.register_error_handler(Exception, database_error)
    

if __name__ == '__main__':
    app.run(debug = True)

