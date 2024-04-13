from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from sasi_controller import sasi_bp


app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
app.register_blueprint(sasi_bp)


@app.route('/')
def hello():
    return "SASI V0.1"


if __name__ == '__main__':
    app.run(debug=True, port=8000)
