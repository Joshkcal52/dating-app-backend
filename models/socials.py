import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Socials(db.Model):
    __tablename__ = "Socials"

    social_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contacts.contact_id', ondelete='CASCADE'), nullable=False)
    user_name = db.Column(db.String(), nullable=False)
    platform_name = db.Column(db.String(), nullable=False)

    contact = db.relationship("Contacts", back_populates="socials")

    def __init__(self, contact_id, user_name, platform_name):
        self.contact_id = contact_id
        self.user_name = user_name
        self.platform_name = platform_name


class SocialsSchema(ma.Schema):
    class Meta:
        fields = ['social_id', 'contact_id', 'user_name', 'platform_name']


social_schema = SocialsSchema()
socials_schema = SocialsSchema(many=True)
