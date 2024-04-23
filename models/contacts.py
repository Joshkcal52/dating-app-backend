import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Contacts(db.Model):
    __tablename__ = "Contacts"

    contact_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=True)
    notes = db.Column(db.String(), nullable=True)

    user = db.relationship("Users", back_populates="contacts")
    socials = db.relationship("Socials", back_populates="contact")

    def __init__(self, user_id, first_name, last_name, phone_number=None, notes=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.notes = notes


class ContactsSchema(ma.Schema):
    class Meta:
        fields = ['contact_id', 'user_id', 'first_name', 'last_name', 'phone_number', 'notes']


contact_schema = ContactsSchema()
contacts_schema = ContactsSchema(many=True)
