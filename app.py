import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

# Environment variables
load_dotenv()

DEBUG = os.environ.get("FLASK_DEBUG") or 0
PORT = os.environ.get("CONFIG_PORT") or 5000

app = Flask(__name__)
cors = CORS(app)


@app.route("/blacklists", methods=["POST"])
def add_email_to_blacklist():
    return "<p>Endpoint for blacklisting an email</p>"


@app.route("/blacklists/<string:email>", methods=["GET"])
def get_email_status():
    return "<p>Endpoint to verify if an email is included in the blacklist</p>"


@app.route("/health", methods=["GET"])
def check_service():
    return {"msg": "Healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG, port=PORT)
