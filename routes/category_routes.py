from flask import Blueprint, request
import controllers

category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def add_category():
    return controllers.add_category(request)


@category.route('/category', methods=['GET'])
def get_categories():
    return controllers.get_categories(request)


@category.route('/category/<id>', methods=['GET'])
def get_category_by_id(id):
    return controllers.get_category_by_id(request, id)


@category.route('/category/activate/<id>', methods=['PUT'])
def activate_category(id):
    return controllers.activate_category(request, id)


@category.route('/category/deactivate/<id>', methods=['PUT'])
def deactivate_category(id):
    return controllers.deactivate_category(request, id)


@category.route('/category/<id>', methods=['PUT'])
def update_category(id):
    return controllers.update_category(request, id)


@category.route('/category/delete/<id>', methods=['DELETE'])
def delete_category_by_id(id):
    return controllers.delete_category(request, id)
