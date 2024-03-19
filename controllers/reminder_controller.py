from flask import jsonify, request
from db import db
from models.reminder import Reminder, reminder_schema, reminders_schema


def create_reminder(req):
    data = request.json
    event_id = data.get('event_id')
    reminder_datetime = data.get('reminder_datetime')
    reminder_type = data.get('reminder_type')

    if not all([event_id, reminder_datetime, reminder_type]):
        return jsonify({"error": "Event ID, reminder_datetime, and reminder_type are required"}), 400

    try:
        new_reminder = Reminder(event_id=event_id, reminder_datetime=reminder_datetime, reminder_type=reminder_type)
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify({"message": "Reminder created successfully", "reminder": reminder_schema.dump(new_reminder)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create reminder: {str(e)}"}), 500


def get_all_reminders():
    reminders = Reminder.query.all()
    return jsonify({"message": "Reminders found", "reminders": reminders_schema.dump(reminders)}), 200


def get_reminder_by_id(reminder_id):
    reminder = Reminder.query.get(reminder_id)

    if reminder:
        return jsonify({"reminder": reminder_schema.dump(reminder)}), 200

    return jsonify({"error": "Reminder not found"}), 404


def update_reminder(reminder_id):
    data = request.json
    reminder = Reminder.query.get(reminder_id)

    if reminder:
        try:
            for key, value in data.items():
                setattr(reminder, key, value)
            db.session.commit()
            return jsonify({"message": "Reminder updated successfully", "reminder": reminder_schema.dump(reminder)}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to update reminder: {str(e)}"}), 500
    else:
        return jsonify({"error": "Reminder not found"}), 404


def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)

    if reminder:
        try:
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({"message": "Reminder deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to delete reminder: {str(e)}"}), 500

    return jsonify({"error": "Reminder not found"}), 404
