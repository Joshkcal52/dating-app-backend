from db import db

contacts_events_association_table = db.Table(
    "contacts_events",
    db.Model.metadata,
    db.Column("contact_id", db.ForeignKey("Contacts.contact_id", ondelete='CASCADE'), primary_key=True),
    db.Column("event_id", db.ForeignKey("Events.event_id", ondelete='CASCADE'), primary_key=True)
)
