from app import db

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    invoices = db.relationship('Invoice', back_populates='trip', cascade="all, delete-orphan")
