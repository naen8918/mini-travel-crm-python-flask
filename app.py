from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from dotenv import load_dotenv
import sqlite3
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Load environment variables
load_dotenv()

# Initialize app and config
app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Enable SQLite foreign key constraints
@event.listens_for(Engine, "connect")
def enforce_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Import and register Blueprints
from routes.clients import clients_bp
from routes.trips import trips_bp
from routes.invoices import invoices_bp
from routes.payments import payments_bp
from routes.reports import reports_bp
from routes.client_notes import notes_bp
from auth.routes import auth_bp

app.register_blueprint(notes_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(trips_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(auth_bp)

# Import models for table creation
from models.client import Client
from models.trip import Trip
from models.invoice import Invoice
from models.payment import Payment
from models.client_note import ClientNote
from auth.models import User

# Ensure all tables exist
with app.app_context():
    db.create_all()
