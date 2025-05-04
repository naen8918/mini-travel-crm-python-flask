from app import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey('invoice.id', ondelete='CASCADE'),
        nullable=False
    )
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # e.g. Credit Card

    invoice = db.relationship(
        'Invoice',
        back_populates='payments',
        passive_deletes=True
    )
