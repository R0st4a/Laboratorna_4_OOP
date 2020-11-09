from flask import Flask
from wsgiref.simple_server import make_server
app = Flask(__name__)

@app.route('/api/v1/hello-world-27')
def hello_world():
    return 'Hello, World 27!'

with make_server('',5000,app)as server:
    print("Port 127.0.0.1:5000")

    server.serve_forever()