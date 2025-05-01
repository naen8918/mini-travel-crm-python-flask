# routes/reports.py

from flask import Blueprint, jsonify
from app import db
from models.client import Client
from models.trip import Trip
from models.invoice import Invoice
from models.payment import Payment
from sqlalchemy import func
from sqlalchemy import extract
from flask import request

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/revenue-by-client', methods=['GET'])
def revenue_by_client():
    # Step 1: Join Payment -> Invoice -> Trip -> Client
    results = db.session.query(
        Client.id,
        Client.name,
        func.sum(Payment.amount).label('total_revenue')
    ).join(Trip, Trip.client_id == Client.id)\
     .join(Invoice, Invoice.trip_id == Trip.id)\
     .join(Payment, Payment.invoice_id == Invoice.id)\
     .group_by(Client.id, Client.name)\
     .order_by(func.sum(Payment.amount).desc())\
     .all()

    # Step 2: Convert to JSON
    data = [
        {
            'client_id': row.id,
            'client_name': row.name,
            'total_revenue': round(row.total_revenue, 2)
        }
        for row in results
    ]

    return jsonify(data)

@reports_bp.route('/reports/unpaid-invoices', methods=['GET'])
def unpaid_invoices():
    invoices = Invoice.query.filter(Invoice.status != 'Paid').all()

    data = [
        {
            'invoice_id': inv.id,
            'trip_id': inv.trip_id,
            'issue_date': str(inv.issue_date),
            'due_date': str(inv.due_date),
            'amount': inv.amount,
            'status': inv.status
        }
        for inv in invoices
    ]

    return jsonify(data)

@reports_bp.route('/reports/monthly-revenue', methods=['GET'])
def monthly_revenue():
    year_filter = request.args.get('year', type=int)
    destination_filter = request.args.get('destination', type=str)

    query = db.session.query(
        extract('year', Payment.payment_date).label('year'),
        extract('month', Payment.payment_date).label('month'),
        Trip.destination.label('destination'),
        func.sum(Payment.amount).label('total')
    ).join(Invoice, Invoice.id == Payment.invoice_id)\
     .join(Trip, Trip.id == Invoice.trip_id)

    # Apply filters if present
    if year_filter:
        query = query.filter(extract('year', Payment.payment_date) == year_filter)
    if destination_filter:
        query = query.filter(Trip.destination.ilike(f'%{destination_filter}%'))

    results = query.group_by('year', 'month', 'destination')\
                   .order_by('year', 'month', 'destination')\
                   .all()

    data = [
        {
            'year': int(row.year),
            'month': int(row.month),
            'destination': row.destination,
            'total_revenue': round(row.total, 2)
        }
        for row in results
    ]

    return jsonify(data)
