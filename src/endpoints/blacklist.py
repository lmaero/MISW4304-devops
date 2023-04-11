import json
import os

from datetime import datetime
from src.models.blacklisted import Blacklisted
from src.schemas.blacklisted import BlacklistedSchema
def post_add_email_to_blacklist(db, request):
    try:
        data = request.get_json()
        new_blacklisted = Blacklisted(
            email=data["email"],
            app_id=data["app_id"],
            cause=data["reason"],
            ip_address=data["ip_address"],
            time=datetime.now().isoformat()
        )
        db.session.add(new_blacklisted)
        db.session.commit()
        BlacklistedSchema().dump(new_blacklisted)
        return {"id": new_blacklisted.id, "createdAt": new_blacklisted.time.isoformat()}, 201
    except Exception as e:
        print(e)
        return {"msg": "Invalid request"}, 500
