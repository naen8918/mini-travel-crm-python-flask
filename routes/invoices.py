from flask import Blueprint, request, jsonify
from app import db
from models.invoice import Invoice
from models.trip import Trip
from datetime import datetime  # Needed to parse dates

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.get_json()

    # Convert string dates to datetime.date objects
    issue_date = datetime.strptime(data['issue_date'], '%Y-%m-%d').date()
    due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

    new_invoice = Invoice(
        trip_id=data['trip_id'],
        issue_date=issue_date,
        due_date=due_date,
        amount=data['amount'],
        status=data.get('status', 'Pending')  # Default to 'Pending' if not provided
    )

    db.session.add(new_invoice)
    db.session.commit()

    return jsonify({'message': 'Invoice created successfully'})

@invoices_bp.route('/invoices/<int:trip_id>', methods=['GET'])
def get_invoices_for_trip(trip_id):
    Trip.query.get_or_404(trip_id)  # Check if trip exists first

    invoices = Invoice.query.filter_by(trip_id=trip_id).all()
    result = [
        {
            'id': inv.id,
            'issue_date': str(inv.issue_date),
            'due_date': str(inv.due_date),
            'amount': inv.amount,
            'status': inv.status
        }
        for inv in invoices
    ]
    return jsonify(result)

# PATCH /invoices/<invoice_id>
@invoices_bp.route('/invoices/<int:invoice_id>', methods=['PATCH'])
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json()

    if 'issue_date' in data:
        invoice.issue_date = datetime.strptime(data['issue_date'], '%Y-%m-%d').date()
    if 'due_date' in data:
        invoice.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    if 'amount' in data:
        invoice.amount = data['amount']
    if 'status' in data:
        invoice.status = data['status']

    db.session.commit()

    return jsonify({'message': 'Invoice updated successfully'})

# DELETE /invoices/<invoice_id>
@invoices_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    db.session.delete(invoice)
    db.session.commit()

    return jsonify({'message': 'Invoice deleted successfully'})

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice_by_id(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    return jsonify({
        'id': invoice.id,
        'trip_id': invoice.trip_id,
        'issue_date': str(invoice.issue_date),
        'due_date': str(invoice.due_date),
        'amount': invoice.amount,
        'status': invoice.status
    })
