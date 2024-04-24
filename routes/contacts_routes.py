from flask import Blueprint, request
import controllers

contacts = Blueprint('contacts', __name__)


@contacts.route("/contact", methods=['POST'])
def add_contact():
    return controllers.add_contact(request)


@contacts.route("/contacts", methods=['GET'])
def get_contacts():
    return controllers.get_contacts(request)


@contacts.route('/contact/<id>', methods=['GET'])
def get_contact_by_id(id):
    return controllers.get_contact_by_id(request, id)


@contacts.route('/contact/status/<id>', methods=['PUT'])
def contact_status(id):
    return controllers.contact_status(request, id)


@contacts.route('/contact/<id>', methods=['PUT'])
def update_contact(id):
    return controllers.update_contact(request, id)


@contacts.route('/contact/delete/<id>', methods=['DELETE'])
def delete_contact(id):
    return controllers.delete_contact(request, id)
