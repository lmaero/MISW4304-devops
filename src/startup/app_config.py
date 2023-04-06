from flask_cors import CORS

from src.startup.db_connection import DATABASE_URL


def config_app(app):
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app_context = app.app_context()
    app_context.push()
