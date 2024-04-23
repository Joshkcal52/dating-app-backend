from flask import jsonify, request

from db import db
from models.events import Events, event_schema, events_schema
from util.reflections import populate_object


def add_event(req):
    req_data = request.form if request.form else request.get_json()

    new_event = Events(**req_data)

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Event created", "event": event_schema.dump(new_event)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create event: {str(e)}"}), 500


def get_events(req):
    event_query = Events.query.all()

    return jsonify({'message': 'Events found', 'events': events_schema.dump(event_query)}), 200


def update_event(req, event_id):
    post_data = request.json
    event_query = Events.query.get(event_id)

    if not event_query:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404

    populate_object(event_query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'Event updated successfully', 'event': event_schema.dump(event_query)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to update event: {str(e)}"}), 500


def delete_event(req, event_id):
    event_query = Events.query.get(event_id)

    if not event_query:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404

    try:
        db.session.delete(event_query)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to delete event: {str(e)}"}), 500
