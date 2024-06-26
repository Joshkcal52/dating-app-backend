import functools
from flask import request, jsonify
from datetime import datetime, timezone
from uuid import UUID

from db import db
from models.users import Users, user_schema
from models.auth_tokens import AuthTokens


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except:
        return False


def validate_token(request):
    auth_token = request.headers['auth']

    if not auth_token or not validate_uuid4(auth_token):
        print("Invalid or missing token")
        return False

    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now(timezone.utc).replace(tzinfo=None):
            print("Token expired or not found")
            return existing_token

    else:
        return False


def fail_response():
    return jsonify({"message": "authentication required"}), 401


def auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if auth_info:
            return func(*args, **kwargs)

        else:
            return fail_response()

    return wrapper_auth_return


def auth_admin(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(request)

        if auth_info:
            user_id = auth_info.user_id
            admin_query = db.session.query(Users).filter(Users.user_id == user_id).first()

            if admin_query and admin_query.role == "admin":
                return func(*args, **kwargs)

        return fail_response()

    return wrapper_auth_return
