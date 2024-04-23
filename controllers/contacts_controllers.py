from flask import jsonify, request

from db import db
from models.contacts import Contacts, contact_schema, contacts_schema
from util.reflections import populate_object


def add_contact(req):
    req_data = request.form if request.form else request.get_json()

    new_contact = Contacts(**req_data)

    try:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact created", "contact": contact_schema.dump(new_contact)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create contact: {str(e)}"}), 500


def get_contacts(req):
    contact_query = Contacts.query.all()

    return jsonify({'message': 'Contacts found', 'contacts': contacts_schema.dump(contact_query)}), 200


def get_contact_by_id(req, contact_id):
    contact_query = Contacts.query.get(contact_id)

    if not contact_query:
        return jsonify({"error": f"Contact with ID {contact_id} not found"}), 404

    return jsonify({'message': 'Contact found', 'contact': contact_schema.dump(contact_query)}), 200


def update_contact(req, contact_id):
    post_data = request.json
    contact_query = Contacts.query.get(contact_id)

    if not contact_query:
        return jsonify({"error": f"Contact with ID {contact_id} not found"}), 404

    populate_object(contact_query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully', 'contact': contact_schema.dump(contact_query)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to update contact: {str(e)}"}), 500


def delete_contact(req, contact_id):
    contact_query = Contacts.query.get(contact_id)

    if not contact_query:
        return jsonify({"error": f"Contact with ID {contact_id} not found"}), 404

    try:
        db.session.delete(contact_query)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to delete contact: {str(e)}"}), 500
