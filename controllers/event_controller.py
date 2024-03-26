from flask import jsonify, request
from db import db
from models.events import Event, event_schema, events_schema


def create_event(req):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    start_datetime = data.get('start_datetime')
    end_datetime = data.get('end_datetime')
    user_id = data.get('user_id')

    if not all([title, start_datetime, end_datetime, user_id]):
        return jsonify({"error": "Title, start_datetime, end_datetime, and user_id are required"}), 400

    try:
        new_event = Event(title=title, description=description, start_datetime=start_datetime, end_datetime=end_datetime, user_id=user_id)
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Event created successfully", "event": event_schema.dump(new_event)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create event: {str(e)}"}), 500


def get_all_events(req):
    events = Event.query.all()
    return jsonify({"message": "Events found", "events": events_schema.dump(events)}), 200


def get_event_by_id(event_id):
    event = Event.query.get(event_id)

    if event:
        return jsonify({"event": event_schema.dump(event)}), 200

    return jsonify({"error": "Event not found"}), 404


def update_event(event_id):
    data = request.json
    event = Event.query.get(event_id)

    if event:
        try:
            for key, value in data.items():
                setattr(event, key, value)
            db.session.commit()
            return jsonify({"message": "Event updated successfully", "event": event_schema.dump(event)}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to update event: {str(e)}"}), 500
    else:
        return jsonify({"error": "Event not found"}), 404


def delete_event(event_id):
    event = Event.query.get(event_id)

    if event:
        try:
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Event deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to delete event: {str(e)}"}), 500

    return jsonify({"error": "Event not found"}), 404
