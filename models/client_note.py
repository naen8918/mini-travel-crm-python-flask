from app import db
from datetime import datetime, timezone

class ClientNote(db.Model):
    __tablename__ = 'client_note'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id', ondelete='CASCADE'),
        nullable=False
    )
    note = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship is handled on the Client side with backref
