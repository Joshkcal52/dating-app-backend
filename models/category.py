import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class EventCategory(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), nullable=False)
    category_color = db.Column(db.String())

    def __init__(self, category_name, category_color=None):
        self.category_name = category_name
        self.category_color = category_color


class EventCategorySchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'category_name', 'category_color']


event_category_schema = EventCategorySchema()
event_categories_schema = EventCategorySchema(many=True)
