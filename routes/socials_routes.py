from flask import Blueprint, jsonify, request
import controllers

socials = Blueprint('socials', __name__)


@socials.route('/social', methods=['POST'])
def add_social():
    return controllers.add_social(request)


@socials.route('/socials', methods=['GET'])
def get_socials():
    return controllers.get_socials(request)

@socials.route('/social/status/<id>', methods=['PUT'])
def social_status(id):
    return controllers.social_status(request, id)


@socials.route('/social/<id>', methods=['PUT'])
def update_social(id):
    return controllers.update_social(request, id)


@socials.route('/social/delete/<id>', methods=['DELETE'])
def delete_social(id):
    return controllers.delete_social(request, id)
