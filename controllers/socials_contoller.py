from flask import jsonify, request

from db import db
from models.socials import Socials, social_schema, socials_schema
from util.reflections import populate_object


def add_social(req):
    req_data = request.form if request.form else request.get_json()

    new_social = Socials(**req_data)

    try:
        db.session.add(new_social)
        db.session.commit()
        return jsonify({"message": "Social profile created", "social": social_schema.dump(new_social)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "Failed to create social profile"}), 400


def get_socials(req):
    social_query = Socials.query.all()

    return jsonify({'message': 'Social profiles found', 'socials': socials_schema.dump(social_query)}), 200


def update_social(req, social_id):
    post_data = request.json
    social_query = Socials.query.get(social_id)

    if not social_query:
        return jsonify({"message": "Social profile not found"}), 404

    populate_object(social_query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'Social profile updated successfully', 'social': social_schema.dump(social_query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to update social profile"}), 400


def delete_social(req, social_id):
    social_query = Socials.query.get(social_id)

    if not social_query:
        return jsonify({"message": "Social profile not found"}), 404

    try:
        db.session.delete(social_query)
        db.session.commit()
        return jsonify({'message': 'Social profile deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to delete social profile"}), 500
