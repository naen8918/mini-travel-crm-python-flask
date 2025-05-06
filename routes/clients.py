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


# GET /clients (with filtering)
@clients_bp.route('/clients', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')  # Controls who can view clients
def get_clients():
    # Get optional search parameters
    name_query = request.args.get('name')
    email_query = request.args.get('email')
    phone_query = request.args.get('phone')
    company_query = request.args.get('company')

    # Start building the query
    query = Client.query

    # Apply filters only if parameters are provided
    if name_query:
        query = query.filter(Client.name.ilike(f"%{name_query}%"))
    if email_query:
        query = query.filter(Client.email.ilike(f"%{email_query}%"))
    if phone_query:
        query = query.filter(Client.phone.ilike(f"%{phone_query}%"))
    if company_query:
        query = query.filter(Client.company.ilike(f"%{company_query}%"))

    # Run the query
    clients = query.all()

    # Convert to JSON
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

    return jsonify(result), 200


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
@role_required('admin')
def delete_client(client_id):

    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    db.session.delete(client)
    db.session.commit()
    
    return jsonify({'message': 'Client deleted successfully'}), 200


@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent')  # Controls who can view clients
def get_client_by_id(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'company': client.company
    })
