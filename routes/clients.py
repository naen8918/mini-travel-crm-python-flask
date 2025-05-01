from flask import Blueprint, request, jsonify
from app import db
from models.client import Client

clients_bp = Blueprint('clients', __name__)

# POST /clients
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

# GET /clients
@clients_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    result = [
        {
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
            'company': client.company
        }
        for client in clients
    ]
    return jsonify(result)

# PATCH /clients/<id>
@clients_bp.route('/clients/<int:client_id>', methods=['PATCH'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()

    if 'name' in data:
        client.name = data['name']
    if 'email' in data:
        client.email = data['email']
    if 'phone' in data:
        client.phone = data['phone']
    if 'company' in data:
        client.company = data['company']

    db.session.commit()

    return jsonify({'message': 'Client updated successfully'})

# DELETE /clients/<id>
@clients_bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)

    db.session.delete(client)
    db.session.commit()

    return jsonify({'message': 'Client deleted successfully'})

