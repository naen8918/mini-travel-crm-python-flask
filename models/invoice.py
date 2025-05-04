from app import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(
        db.Integer,
        db.ForeignKey('trip.id', ondelete='CASCADE'),
        nullable=False
    )
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Paid', etc.

    trip = db.relationship(
        'Trip',
        back_populates='invoices',
        passive_deletes=True
    )

    payments = db.relationship(
        'Payment',
        back_populates='invoice',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
