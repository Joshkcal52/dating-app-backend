import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Event(db.Model):
    __tablename__ = "Events"

    event_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    start_datetime = db.Column(db.DateTime(), nullable=False)
    end_datetime = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id", ondelete='CASCADE'), nullable=False)

    user = db.relationship("User", foreign_keys="[Event.user_id]", back_populates='events')

    def __init__(self, title, description, start_datetime, end_datetime, user_id):
        self.title = title
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.user_id = user_id


class EventSchema(ma.Schema):
    class Meta:
        fields = ['event_id', 'title', 'description', 'start_datetime', 'end_datetime', 'user']
    user = ma.fields.Nested('UserSchema', exclude=['events'])


event_schema = EventSchema()
events_schema = EventSchema(many=True)
