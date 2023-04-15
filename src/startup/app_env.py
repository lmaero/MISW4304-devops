import os

# App variables
APP_DEBUG = os.environ.get("FLASK_DEBUG") or 0
APP_PORT = os.environ.get("CONFIG_PORT") or 5000

# Database variables
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_HOST = os.environ.get("POSTGRES_HOST")
STATIC_TOKEN = os.environ.get("STATIC_TOKEN")
