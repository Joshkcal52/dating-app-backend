from flask import Blueprint, request
import controllers

event = Blueprint('event', __name__)


@event.route('/event', methods=['POST'])
def create_event_route():
    return controllers.create_event(request)


@event.route('/events', methods=['GET'])
def get_all_events():
    return controllers.create_event(request)


@event.route('/event/<id>', methods=['GET'])
def get_event_by_id(id):
    return controllers.get_event_by_id(id)


@event.route('/event/<id>', methods=['PUT'])
def update_event(id):
    return controllers.update_event(id)


@event.route('/event/delete/<id>')
def delete_event(id):
    return controllers.delete_event(id)
