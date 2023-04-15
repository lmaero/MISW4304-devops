from dotenv import load_dotenv
from flask import Flask, request

from src.endpoints.blacklist import post_add_email_to_blacklist, blackmail_info_get
from src.startup.app_config import config_app
from src.startup.app_env import APP_DEBUG, APP_PORT
from src.startup.db_connection import init_db, database

# Load environment variables
load_dotenv()

# App configuration
app = Flask(__name__)
config_app(app)

# Database initialization
init_db(app)


@app.route("/blacklists", methods=["POST"])
def add_email_to_blacklist():
    return post_add_email_to_blacklist(database, request)


@app.route("/blacklists/<string:email>", methods=["GET"])
def get_email_status(email):
    return blackmail_info_get(email, database, request)

@app.route("/health", methods=["GET"])
def check_service():
    return {"msg": "Healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=APP_DEBUG, port=APP_PORT)
