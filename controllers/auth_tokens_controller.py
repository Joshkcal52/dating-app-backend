from flask import jsonify, request
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db  
from models.auth_tokens import AuthTokens, auth_token_schema 
from models.users import Users  


def auth_token_add(req):
    post_data = request.json
    email = post_data.get('email')
    password = post_data.get('password')

    if not email or not password:
        return jsonify({'message': 'Invalid login'}), 401

    now_datetime = datetime.utcnow()
    expiration_datetime = now_datetime + timedelta(hours=12)

    user_data = Users.query.filter_by(email=email).first()

    if user_data:
        is_password_valid = check_password_hash(user_data.password, password)
        if not is_password_valid:
            return jsonify({'message': 'Invalid password'}), 401

        existing_tokens = AuthTokens.query.filter_by(user_id=user_data.user_id).all()

        for token in existing_tokens:
            if token.expiration < now_datetime:
                db.session.delete(token)

        new_token = AuthTokens(user_data.user_id, expiration_datetime)
        db.session.add(new_token)
        db.session.commit()

        return jsonify({"message": "Authentication success", "auth_info": auth_token_schema.dump(new_token)})

    return jsonify({'message': 'Invalid user'}), 401


def auth_token_remove(req):
    post_data = request.json
    auth_token = post_data.get("auth_token")

    auth_record = AuthTokens.query.filter_by(auth_token=auth_token).first()

    if auth_record:
        db.session.delete(auth_record)
        db.session.commit()
        return jsonify({"message": "Authentication token removed"}), 200
    else:
        return jsonify({"error": "Authentication token not found"}), 404


def auth_token_remove_expired(req):
    expired_auth_tokens = AuthTokens.query.filter(AuthTokens.expiration < datetime.utcnow()).all()

    for auth_token in expired_auth_tokens:
        db.session.delete(auth_token)

    db.session.commit()

    return jsonify({"message": f"Removed {len(expired_auth_tokens)} expired authentication tokens"}), 200
