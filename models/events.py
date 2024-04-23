import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Events(db.Model):
    __tablename__ = "Events"

    event_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    start_datetime = db.Column(db.String(), nullable=False)
    end_datetime = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Category.category_id'), nullable=True)

    user = db.relationship("Users", back_populates="events")
    category = db.relationship("Category")

    def __init__(self, user_id, title, start_datetime, end_datetime, description=None, category_id=None):
        self.user_id = user_id
        self.title = title
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.description = description
        self.category_id = category_id


class EventsSchema(ma.Schema):
    class Meta:
        fields = ['event_id', 'user_id', 'title', 'start_datetime', 'end_datetime', 'description', 'category_id']


event_schema = EventsSchema()
events_schema = EventsSchema(many=True)
