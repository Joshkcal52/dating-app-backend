from flask import Blueprint, request
import controllers

event = Blueprint('events', __name__)


@event.route('/event', methods=['POST'])
def create_event_route():
    return controllers.create_event(request)
