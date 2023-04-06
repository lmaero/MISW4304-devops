from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models.blacklisted import Blacklisted


class BlacklistedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklisted
        load_instance = True

    email = fields.String()
    app_id = fields.String()
    cause = fields.String()
    ip_address = fields.String()
    time = fields.String()
