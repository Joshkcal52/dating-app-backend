import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    events = db.relationship("Event", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'username', 'email']
