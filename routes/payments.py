from flask import Blueprint, request, jsonify
from app import db
from models.payment import Payment
from models.invoice import Invoice
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.permissions import role_required

payments_bp = Blueprint('payments', __name__)

# Create a new payment
@payments_bp.route('/payments', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def create_payment():
    print(f"Payment recorded by user: {get_jwt_identity()}")
    data = request.get_json()

    payment = Payment(
        invoice_id=data['invoice_id'],
        payment_date=datetime.strptime(data['payment_date'], '%Y-%m-%d').date(),
        amount=data['amount'],
        payment_method=data['payment_method']
    )

    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment recorded successfully'}), 201

# Get all payments for an invoice
@payments_bp.route('/payments/<int:invoice_id>', methods=['GET'])
def get_payments_for_invoice(invoice_id):
    Invoice.query.get_or_404(invoice_id)
    payments = Payment.query.filter_by(invoice_id=invoice_id).all()

    return jsonify([
        {
            'id': pay.id,
            'payment_date': str(pay.payment_date),
            'amount': pay.amount,
            'payment_method': pay.payment_method
        }
        for pay in payments
    ]), 200

# Get payment by ID
@payments_bp.route('/payment/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    pay = Payment.query.get_or_404(payment_id)
    return jsonify({
        'id': pay.id,
        'invoice_id': pay.invoice_id,
        'payment_date': str(pay.payment_date),
        'amount': pay.amount,
        'payment_method': pay.payment_method
    }), 200

# Update payment
@payments_bp.route('/payments/<int:payment_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin', 'agent')
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()

    if 'payment_date' in data:
        payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
    if 'amount' in data:
        payment.amount = data['amount']
    if 'payment_method' in data:
        payment.payment_method = data['payment_method']

    db.session.commit()
    return jsonify({'message': 'Payment updated successfully'}), 200

# Delete payment
@payments_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'}), 200
