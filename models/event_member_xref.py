from db import db

event_members_association_table = db.Table(
    'event_members',
    db.Column('event_id', db.ForeignKey('events.event_id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
)
