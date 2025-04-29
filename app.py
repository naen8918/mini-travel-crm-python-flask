from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from models import client
with app.app_context():
    db.create_all()

from routes.clients import clients_bp
app.register_blueprint(clients_bp)
