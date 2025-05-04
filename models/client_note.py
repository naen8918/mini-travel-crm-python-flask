from app import db
from datetime import datetime, timezone

class ClientNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id', ondelete='CASCADE'),
        nullable=False
    )
    note = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship handled via backref in Client model
