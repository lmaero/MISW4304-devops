import json
import os

from datetime import datetime

import jwt

from src.models.blacklisted import Blacklisted
from src.schemas.blacklisted import BlacklistedSchema
def post_add_email_to_blacklist(db, request):
    try:
        bearer = request.headers.get('Authorization')
        if bearer is None or bearer == '':
            return {"msg": "Authorization header is not in the headers or bearer value is wrong"}, 400
        if len(bearer.split()) < 2:
            return {"msg": "Token is not in the headers"}, 400

        email = request.args.get("email")
        if str(email) == '':
            return {"msg": "The email is missing, please provide a valid email"}, 400

        app_uuid = request.args.get("app_uuid")
        if str(app_uuid) == '':
            return {"msg": "The app_uuid is missing, please provide a valid app id"}, 400

        blocked_reason = request.args.get("blocked_reason")
        if len(blocked_reason) > 255:
            return {"msg": "The block reason has to be less than 255 characters"}, 400

        ip_address = str(request.remote_addr)

        new_blacklisted = Blacklisted(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip_address=ip_address,
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

