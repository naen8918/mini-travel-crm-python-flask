from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import routes
from routes.clients import clients_bp
from routes.trips import trips_bp
from routes.invoices import invoices_bp
from routes.payments import payments_bp

# Register Blueprints
app.register_blueprint(clients_bp)
app.register_blueprint(trips_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(payments_bp)

# Import models
from models.client import Client
from models.trip import Trip
from models.invoice import Invoice
from models.payment import Payment

from routes.reports import reports_bp
app.register_blueprint(reports_bp)

with app.app_context():
    db.create_all()
