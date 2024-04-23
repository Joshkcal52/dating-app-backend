import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Category(db.Model):
    __tablename__ = "Category"

    category_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    color = db.Column(db.String(), nullable=False)

    def __init__(self, name, color):
        self.name = name
        self.color = color


class CategorySchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'name', 'color']


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
