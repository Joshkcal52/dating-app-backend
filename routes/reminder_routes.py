from flask import Blueprint, request
import controllers

reminder = Blueprint('reminder', __name__)


@reminder.route('/reminder', methods=['POST'])
def create_reminder():
    return controllers.create_reminder(request)


@reminder.route('/reminders', methods=['GET'])
def get_all_reminders():
    return controllers.get_all_reminders()


@reminder.route('/reminder/<id>', methods=['GET'])
def get_reminder_by_id(reminder_id):
    return controllers.get_reminder_by_id(reminder_id)


@reminder.route('/reminder/<id>', methods=['PUT'])
def update_reminder(reminder_id):
    return controllers.update_reminder(reminder_id)


@reminder.route('/reminder/delete/<id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    return controllers.delete_reminder(reminder_id)
