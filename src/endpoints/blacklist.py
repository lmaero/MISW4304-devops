import json
import os

from datetime import datetime

import jwt

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


def blackmail_info_get(db, request):
    try:
        bearer = request.headers.get('Authorization')
        if bearer is None or bearer == '':
            return {"msg": "Authorization header is not in the headers or bearer value is wrong"}, 400
        if len(bearer.split()) < 2:
            return {"msg": "Token is not in the headers"}, 400
        token = bearer.split()[1]
        try:
            data_decoded = jwt.decode(token, os.environ['SECRET_KEY'], algorithms='HS256')
        except Exception as e:
            return {"msg": "Token is not valid or has already expired"}, 401
        blackmail = db.session.query(Blacklisted).filter_by(id=data_decoded["id"]).first()
        return {"id": int(blackmail.id), "email": str(blackmail.email), "cause": str(blackmail.cause)}, 200
    except Exception as e:
        return {"msg": str(e)}, 500

