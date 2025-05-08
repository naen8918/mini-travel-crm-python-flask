from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from auth.permissions import role_required
from app import db
from models.client import Client
import csv
from io import StringIO

clients_bp = Blueprint('clients', __name__)

# ----------------------------
# 🔧 Helper: Serialize client
# ----------------------------
def serialize_client(client):
    return {
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'company': client.company
    }

# ----------------------------
# ✅ POST /clients
# ----------------------------
@clients_bp.route('/clients', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def create_client():
    data = request.get_json()
    required_fields = ['name', 'email', 'phone']
    missing = [f for f in required_fields if f not in data or not data[f]]

    if missing:
        return jsonify({'error': f"Missing required field(s): {', '.join(missing)}"}), 400

    if Client.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'A client with this email already exists'}), 409

    new_client = Client(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        company=data.get('company')
    )
    db.session.add(new_client)
    db.session.commit()

    return jsonify({'message': 'Client created successfully'}), 201

# ----------------------------
# 🔍 GET /clients (with filters)
# ----------------------------
@clients_bp.route('/clients', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')
def get_clients():
    query = Client.query
    filters = {
        'name': Client.name,
        'email': Client.email,
        'phone': Client.phone,
        'company': Client.company
    }

    for param, column in filters.items():
        value = request.args.get(param)
        if value:
            query = query.filter(column.ilike(f"%{value}%"))

    return jsonify([serialize_client(c) for c in query.all()]), 200

# ----------------------------
# 🛠️ PATCH /clients/<id>
# ----------------------------
@clients_bp.route('/clients/<int:client_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin', 'agent')
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()

    allowed_fields = {'name', 'email', 'phone', 'company'}
    unknown = [key for key in data if key not in allowed_fields]
    if unknown:
        return jsonify({'error': f"Invalid field(s): {', '.join(unknown)}"}), 400

    if 'email' in data:
        existing = Client.query.filter(Client.email == data['email'], Client.id != client_id).first()
        if existing:
            return jsonify({'error': 'Email already in use by another client'}), 409

    for field in allowed_fields:
        if field in data:
            setattr(client, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Client updated successfully'})

# ----------------------------
# ❌ DELETE /clients/<id>
# ----------------------------
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

# ----------------------------
# 🔍 GET /clients/<id>
# ----------------------------
@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent')
def get_client_by_id(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(serialize_client(client))

# ----------------------------
# 📋 GET /clients/<id>/details
# ----------------------------
@clients_bp.route('/clients/<int:client_id>/details', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')
def get_client_details(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    trips_data = []
    for trip in client.trips:
        trip_info = {
            'id': trip.id,
            'destination': trip.destination,
            'start_date': str(trip.start_date),
            'end_date': str(trip.end_date),
            'price': trip.price,
            'notes': trip.notes,
            'invoices': []
        }
        for invoice in trip.invoices:
            invoice_info = {
                'id': invoice.id,
                'issue_date': str(invoice.issue_date),
                'due_date': str(invoice.due_date),
                'amount': invoice.amount,
                'status': invoice.status,
                'payments': [
                    {
                        'id': p.id,
                        'amount': p.amount,
                        'payment_method': p.payment_method,
                        'payment_date': str(p.payment_date)
                    } for p in invoice.payments
                ]
            }
            trip_info['invoices'].append(invoice_info)
        trips_data.append(trip_info)

    notes_data = [
        {
            'id': note.id,
            'note': note.note,
            'timestamp': note.timestamp.isoformat()
        }
        for note in client.notes
    ]

    return jsonify({
        **serialize_client(client),
        'trips': trips_data,
        'notes': notes_data
    }), 200

# ----------------------------
# 📤 /clients/<id>/details/export
# ----------------------------
@clients_bp.route('/clients/<int:client_id>/details/export', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')
def export_client_details(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['Client Info'])
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Company'])
    writer.writerow([client.id, client.name, client.email, client.phone, client.company])
    writer.writerow([])

    writer.writerow(['Notes'])
    writer.writerow(['Note ID', 'Text', 'Timestamp'])
    for note in client.notes:
        writer.writerow([note.id, note.note, note.timestamp])
    writer.writerow([])

    for trip in client.trips:
        writer.writerow(['Trip'])
        writer.writerow(['ID', 'Destination', 'Start', 'End', 'Price', 'Notes'])
        writer.writerow([trip.id, trip.destination, trip.start_date, trip.end_date, trip.price, trip.notes])
        for invoice in trip.invoices:
            writer.writerow(['Invoice'])
            writer.writerow(['ID', 'Amount', 'Status', 'Issue Date', 'Due Date'])
            writer.writerow([invoice.id, invoice.amount, invoice.status, invoice.issue_date, invoice.due_date])
            writer.writerow(['Payments'])
            writer.writerow(['ID', 'Amount', 'Method', 'Date'])
            for payment in invoice.payments:
                writer.writerow([payment.id, payment.amount, payment.payment_method, payment.payment_date])
        writer.writerow([])

    output.seek(0)
    return Response(output, mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=client_{client_id}_details.csv'}
    )

# ----------------------------
# 📤 /clients/export
# ----------------------------
@clients_bp.route('/clients/export', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def export_all_clients():
    clients = Client.query.all()
    output = StringIO()
    writer = csv.writer(output)

    for client in clients:
        writer.writerow(['Client Info'])
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Company'])
        writer.writerow([client.id, client.name, client.email, client.phone, client.company])
        writer.writerow([])

        writer.writerow(['Notes'])
        writer.writerow(['Note ID', 'Text', 'Timestamp'])
        for note in client.notes:
            writer.writerow([note.id, note.note, note.timestamp.strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])

        for trip in client.trips:
            writer.writerow(['Trip'])
            writer.writerow(['ID', 'Destination', 'Start', 'End', 'Price', 'Notes'])
            writer.writerow([trip.id, trip.destination, trip.start_date, trip.end_date, trip.price, trip.notes])
            for invoice in trip.invoices:
                writer.writerow(['Invoice'])
                writer.writerow(['ID', 'Amount', 'Status', 'Issue Date', 'Due Date'])
                writer.writerow([invoice.id, invoice.amount, invoice.status, invoice.issue_date, invoice.due_date])
                writer.writerow(['Payments'])
                writer.writerow(['ID', 'Amount', 'Method', 'Date'])
                for payment in invoice.payments:
                    writer.writerow([payment.id, payment.amount, payment.payment_method, payment.payment_date])
            writer.writerow([])
        writer.writerow(['=========='])
        writer.writerow([])

    output.seek(0)
    return Response(output, mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=all_clients_export.csv'}
    )
