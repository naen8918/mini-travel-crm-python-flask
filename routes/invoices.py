from flask import Blueprint, request, jsonify
from app import db
from models.invoice import Invoice
from models.trip import Trip
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.permissions import role_required

invoices_bp = Blueprint('invoices', __name__)

# Allowed invoice statuses
VALID_STATUSES = {'Pending', 'Paid', 'Overdue'}

# Create a new invoice
@invoices_bp.route('/invoices', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def create_invoice():
    print(f"Invoice created by user: {get_jwt_identity()}")
    data = request.get_json()

    required_fields = ['trip_id', 'issue_date', 'due_date', 'amount']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        trip_id = int(data['trip_id'])
        amount = float(data['amount'])
        issue_date = datetime.strptime(data['issue_date'], '%Y-%m-%d').date()
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data format or type'}), 400

    status = data.get('status', 'Pending')
    if status not in VALID_STATUSES:
        return jsonify({'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"}), 400

    if not Trip.query.get(trip_id):
        return jsonify({'error': 'Trip not found'}), 404

    invoice = Invoice(
        trip_id=trip_id,
        issue_date=issue_date,
        due_date=due_date,
        amount=amount,
        status=status
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({'message': 'Invoice created successfully'}), 201


# Get all invoices for a trip
@invoices_bp.route('/invoices/<int:trip_id>', methods=['GET'])
def get_invoices_for_trip(trip_id):
    Trip.query.get_or_404(trip_id)
    invoices = Invoice.query.filter_by(trip_id=trip_id).all()

    return jsonify([
        {
            'id': inv.id,
            'issue_date': str(inv.issue_date),
            'due_date': str(inv.due_date),
            'amount': inv.amount,
            'status': inv.status
        } for inv in invoices
    ]), 200


# Get invoice by ID
@invoices_bp.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_invoice_by_id(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    return jsonify({
        'id': inv.id,
        'trip_id': inv.trip_id,
        'issue_date': str(inv.issue_date),
        'due_date': str(inv.due_date),
        'amount': inv.amount,
        'status': inv.status
    }), 200


# Update invoice
@invoices_bp.route('/invoices/<int:invoice_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin', 'agent')
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json()

    allowed_fields = {'issue_date', 'due_date', 'amount', 'status'}
    unknown_fields = [key for key in data if key not in allowed_fields]
    if unknown_fields:
        return jsonify({'error': f"Unknown or unauthorized fields: {', '.join(unknown_fields)}"}), 400

    if 'issue_date' in data:
        try:
            invoice.issue_date = datetime.strptime(data['issue_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid issue date format (expected YYYY-MM-DD)'}), 400

    if 'due_date' in data:
        try:
            invoice.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid due date format (expected YYYY-MM-DD)'}), 400

    if 'amount' in data:
        try:
            invoice.amount = float(data['amount'])
        except ValueError:
            return jsonify({'error': 'Amount must be a number'}), 400

    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return jsonify({'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"}), 400
        invoice.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Invoice updated successfully'}), 200


# Delete invoice
@invoices_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice deleted successfully'}), 200
