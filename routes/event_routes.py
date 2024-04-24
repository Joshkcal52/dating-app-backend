from flask import Blueprint, request
import controllers

event = Blueprint('event', __name__)


@event.route('/event', methods=['POST'])
def add_event():
    return controllers.add_event(request)


@event.route('/events', methods=['GET'])
def get_events():
    return controllers.get_events(request)


@event.route('/event/status/<id>', methods=['PUT'])
def event_status(id):
    return controllers.event_status(request, id)


@event.route('/event/<id>', methods=['PUT'])
def update_event(id):
    return controllers.update_event(request, id)


@event.route('/event/delete/<id>', methods=['DELETE'])
def delete_event(id):
    return controllers.delete_event(request, id)
