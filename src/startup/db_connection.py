from flask_sqlalchemy import SQLAlchemy

from src.startup.app_env import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = (
    f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
database = SQLAlchemy()


def init_db(app):
    try:
        database.init_app(app)
        database.create_all()
    except Exception as e:
        print(e)
