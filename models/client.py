from app import db
from models.client_note import ClientNote  # Optional: for type hinting clarity

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))

    # Relationship: A client has many trips
    trips = db.relationship(
        'Trip',
        backref='client',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    # Relationship: A client has many notes
    notes = db.relationship(
        'ClientNote',
        backref='client',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
