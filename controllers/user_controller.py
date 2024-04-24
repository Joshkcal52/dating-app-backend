from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from lib.authenticate import auth, auth_admin
from models.users import Users, user_schema, users_schema
from util.reflections import populate_object


def add_user(req):
    req_data = request.form if request.form else request.get_json()

    new_user = Users.get_new_user()

    populate_object(new_user, req_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "user created", "results": user_schema.dump(new_user)}), 200


@auth
def get_users(req):
    user_query = db.session.query(Users).all()

    return jsonify({'message': 'users found', 'result': users_schema.dump(user_query)}), 200


@auth_admin
def user_status(user_id):
    try:
        user = db.session.query(Users).filter(Users.user_id == user_id).first()
        if user:
            user.active = not user.active
            db.session.commit()
            return jsonify({'message': 'user status updated successfully', 'result': user_schema.dump(user)}), 200
        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'unable to update user status', 'error': str(e)}), 400


@auth_admin
def update_user(req, user_id):
    post_data = req.form if req.form else req.json
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    populate_object(user_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'user could not be updated'}), 400

    return jsonify({'message': 'user updated', 'result': user_schema.dump(user_query)}), 200


@auth_admin
def delete_user(req, user_id):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": f"user by id {user_id} does not exist"}), 400

    try:
        db.session.delete(user_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete user"}), 400

    return jsonify({"message": "user has been deleted"}), 200
