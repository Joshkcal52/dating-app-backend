from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
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
        return jsonify({"message": "User created", "user": user_schema.dump(new_user)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500


def get_users(req):
    user_query = Users.query.all()

    return jsonify({'message': 'Users found', 'users': users_schema.dump(user_query)}), 200


def update_user(req, user_id):
    post_data = request.json
    user_query = Users.query.get(user_id)

    if not user_query:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    populate_object(user_query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully', 'user': user_schema.dump(user_query)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to update user: {str(e)}"}), 500


def delete_user(req, user_id):
    user_query = Users.query.get(user_id)

    if not user_query:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    try:
        db.session.delete(user_query)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to delete user: {str(e)}"}), 500
