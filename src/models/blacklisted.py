from datetime import datetime

from sqlalchemy import DateTime

from src.startup.db_connection import database


def get_time():
    return datetime.now().isoformat()


class Blacklisted(database.Model):
    __tablename__ = "blacklisted"
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, unique=True, nullable=False)
    app_id = database.Column(database.Integer, nullable=False)
    cause = database.Column(database.String(255), nullable=True)
    ip_address = database.Column(database.String, nullable=False)
    time = database.Column(DateTime, default=get_time(), nullable=False)

    def __init__(
        self,
        email,
        app_id,
        cause,
        ip_address,
        time,
    ):
        self.email = email
        self.app_id = app_id
        self.cause = cause
        self.ip_address = ip_address
        self.time = time
