from flask import Blueprint, request, jsonify
from app import db
from models.payment import Payment
from models.invoice import Invoice
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.permissions import role_required

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/payments', methods=['POST'])
@jwt_required() 
@role_required('admin', 'agent')
def create_payment():
    current_user = get_jwt_identity()
    print(f"Payment recorded by user: {current_user}")  # Logging user ID

    data = request.get_json()

    payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()

    new_payment = Payment(
        invoice_id=data['invoice_id'],
        payment_date=payment_date,
        amount=data['amount'],
        payment_method=data['payment_method']
    )

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({'message': 'Payment recorded successfully'})

@payments_bp.route('/payments/<int:invoice_id>', methods=['GET'])
def get_payments_for_invoice(invoice_id):
    Invoice.query.get_or_404(invoice_id)  # Ensure it exists

    payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    result = [
        {
            'id': pay.id,
            'payment_date': str(pay.payment_date),
            'amount': pay.amount,
            'payment_method': pay.payment_method
        }
        for pay in payments
    ]
    return jsonify(result)

# PATCH /payments/<payment_id>
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

    return jsonify({'message': 'Payment updated successfully'})

# DELETE /payments/<payment_id>
@payments_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@jwt_required() 
@role_required('admin')
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)

    db.session.delete(payment)
    db.session.commit()

    return jsonify({'message': 'Payment deleted successfully'})

@payments_bp.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    payment = Payment.query.get_or_404(payment_id)

    return jsonify({
        'id': payment.id,
        'invoice_id': payment.invoice_id,
        'payment_date': str(payment.payment_date),
        'amount': payment.amount,
        'payment_method': payment.payment_method
    })
