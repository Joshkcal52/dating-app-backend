from flask import jsonify, request
from db import db
from models.category import EventCategory, event_category_schema, event_categories_schema


def create_category(req):
    category_name = request.json.get('category_name')

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    existing_category = EventCategory.query.filter_by(category_name=category_name).first()
    if existing_category:
        return jsonify({"error": "Category name already exists"}), 400

    try:
        new_category = EventCategory(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category added", "category": event_category_schema.dump(new_category)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create category: {str(e)}"}), 500


def get_all_categories():
    categories = EventCategory.query.all()
    return jsonify({'message': 'Categories found', 'categories': event_categories_schema.dump(categories)}), 200


def get_category_by_id(category_id):
    category = EventCategory.query.get(category_id)

    if category:
        return jsonify({'category': event_category_schema.dump(category)}), 200

    return jsonify({'error': 'Category not found'}), 404


def update_category(category_id):
    data = request.json
    category = EventCategory.query.get(category_id)

    if category:
        category_name = data.get('category_name')

        if not category_name:
            return jsonify({'error': 'Category name is required'}), 400

        existing_category = EventCategory.query.filter(EventCategory.category_name == category_name, EventCategory.id != category_id).first()
        if existing_category:
            return jsonify({"error": "Category name already exists"}), 400

        category.category_name = category_name

        try:
            db.session.commit()
            return jsonify({'message': 'Category updated successfully', 'category': event_category_schema.dump(category)}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f"Failed to update category: {str(e)}"}), 500
    else:
        return jsonify({'error': 'Category not found'}), 404


def delete_category(category_id):
    category = EventCategory.query.get(category_id)

    if category:
        try:
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Category deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f"Failed to delete category: {str(e)}"}), 500

    return jsonify({'error': 'Category not found'}), 404
