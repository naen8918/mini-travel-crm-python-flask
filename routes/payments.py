from flask import Blueprint, request, jsonify
from app import db
from models.payment import Payment
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/payments', methods=['POST'])
def create_payment():
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
