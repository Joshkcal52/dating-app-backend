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
    except:
        db.session.rollback()
        return jsonify({"message": "Failed to create contact"}), 500


def get_contacts(req):
    contact_query = Contacts.query.all()

    return jsonify({'message': 'Contacts found', 'contacts': contacts_schema.dump(contact_query)}), 200


def get_contact_by_id(req, contact_id):
    contact_query = Contacts.query.get(contact_id)

    if not contact_query:
        return jsonify({"message": "Contact not found"}), 404

    return jsonify({'message': 'Contact found', 'contact': contact_schema.dump(contact_query)}), 200


def contact_status(contact_id):
    try:
        contact = db.session.query(Contacts).filter(Contacts.contact_id == contact_id).first()
        if contact:
            contact.active = not contact.active
            db.session.commit()
            return jsonify({'message': 'Contact status updated successfully', 'result': contact_schema.dump(contact)}), 200
        return jsonify({'message': 'Contact not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Unable to update contact status', 'error': str(e)}), 400


def update_contact(req, contact_id):
    post_data = request.json
    contact_query = Contacts.query.get(contact_id)

    if not contact_query:
        return jsonify({"message": "Contact not found"}), 404

    populate_object(contact_query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully', 'contact': contact_schema.dump(contact_query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to update contact"}), 500


def delete_contact(req, contact_id):
    contact_query = Contacts.query.get(contact_id)

    if not contact_query:
        return jsonify({"message": "Contact not found"}), 404

    try:
        db.session.delete(contact_query)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': "Failed to delete contact"}), 500
