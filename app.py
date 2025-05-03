from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
app.config.from_object(Config)

app.debug = True 

db = SQLAlchemy(app)
jwt = JWTManager(app)  #  Enable JWT handling

# Import and register Blueprints
from routes.clients import clients_bp
from routes.trips import trips_bp
from routes.invoices import invoices_bp
from routes.payments import payments_bp
from routes.reports import reports_bp
from auth.routes import auth_bp  #  New auth blueprint

app.register_blueprint(clients_bp)
app.register_blueprint(trips_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(auth_bp)  # Register auth routes

# Import models to create tables
from models.client import Client
from models.trip import Trip
from models.invoice import Invoice
from models.payment import Payment
from auth.models import User  #  Include User model for table creation

# Ensure tables are created
with app.app_context():
    db.create_all()
