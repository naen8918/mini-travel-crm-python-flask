from flask import Blueprint, request, jsonify
from app import db
from models.client import Client

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()

    new_client = Client(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        company=data.get('company')
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({'message': 'Client created successfully'})
