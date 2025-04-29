from app import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Paid', 'Overdue'

    trip = db.relationship('Trip', back_populates='invoices')
    payments = db.relationship('Payment', back_populates='invoice', cascade="all, delete-orphan")

# Import Trip AFTER the class definition
from models.trip import Trip
