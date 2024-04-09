import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Reminder(db.Model):
    __tablename__ = "Reminders"

    reminder_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Events.event_id", ondelete='CASCADE'), nullable=False)
    reminder_datetime = db.Column(db.DateTime(), nullable=False)
    reminder_type = db.Column(db.String(), nullable=False)

    event = db.relationship("Event", backref=db.backref("reminders", cascade="all, delete-orphan"))

    def __init__(self, event_id, reminder_datetime, reminder_type):
        self.event_id = event_id
        self.reminder_datetime = reminder_datetime
        self.reminder_type = reminder_type


class ReminderSchema(ma.Schema):
    class Meta:
        fields = ['reminder_id', 'event_id', 'reminder_datetime', 'reminder_type']


reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)
