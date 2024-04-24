from flask import jsonify, request

from db import db
from models.category import Category, category_schema, categories_schema
from util.reflections import populate_object


def add_category(req):
    req_data = request.form if request.form else request.get_json()

    new_category = Category(**req_data)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category created", "category": category_schema.dump(new_category)}), 201
    except:
        db.session.rollback()
        return jsonify({"message": "Failed to create category"}), 500


def get_categories(req):
    category_query = Category.query.all()

    return jsonify({'message': 'Categories found', 'categories': categories_schema.dump(category_query)}), 200


def get_category_by_id(req, category_id):
    category_query = Category.query.get(category_id)

    if not category_query:
        return jsonify({"message": "Category not found"}), 404

    return jsonify({'message': 'Category found', 'category': category_schema.dump(category_query)}), 200


def activate_category(req, category_id):
    category_query = Category.query.get(category_id)

    if not category_query:
        return jsonify({"message": "Category not found"}), 404

    category_query.active = True

    try:
        db.session.commit()
        return jsonify({'message': 'Category activated successfully', 'category': category_schema.dump(category_query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to activate category"}), 500


def deactivate_category(req, category_id):
    category_query = Category.query.get(category_id)

    if not category_query:
        return jsonify({"message": "Category not found"}), 404

    category_query.active = False

    try:
        db.session.commit()
        return jsonify({'message': 'Category deactivated successfully', 'category': category_schema.dump(category_query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to deactivate category"}), 500


def update_category(req, category_id):
    post_data = request.json
    category_query = Category.query.get(category_id)

    if not category_query:
        return jsonify({"message": "Category not found"}), 404

    populate_object(category_query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'Category updated successfully', 'category': category_schema.dump(category_query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to update category"}), 500


def delete_category(req, category_id):
    category_query = Category.query.get(category_id)

    if not category_query:
        return jsonify({"message": "Category not found"}), 404

    try:
        db.session.delete(category_query)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to delete category"}), 500
