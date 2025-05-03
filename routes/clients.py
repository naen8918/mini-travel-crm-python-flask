from flask import Blueprint, request, jsonify
from app import db
from models.client import Client
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from auth.permissions import role_required


clients_bp = Blueprint('clients', __name__)

# POST /clients
@clients_bp.route('/clients', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def create_client():
    user_id = get_jwt_identity()
    jwt_data = get_jwt()
    role = jwt_data.get("role")

    data = request.get_json()
    print("[DEBUG] Incoming request data:", data)

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')

    if not name or not email or not phone:
        return jsonify({'error': 'Missing required client data'}), 400

    # Check if email already exists
    if Client.query.filter_by(email=email).first():
        return jsonify({'error': 'A client with this email already exists'}), 409

    print(f"Client added by user: {user_id} with role: {role}")

    new_client = Client(
        name=name,
        email=email,
        phone=phone,
        company=company
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({'message': 'Client created successfully'}), 201 

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
@jwt_required()
@role_required('admin', 'agent')
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
@jwt_required()
@role_required('admin')  # Only admins can delete
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)

    db.session.delete(client)
    db.session.commit()

    return jsonify({'message': 'Client deleted successfully'})

@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'company': client.company
    })
