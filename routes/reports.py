from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required
from auth.permissions import role_required
from app import db
from models.client import Client
from models.trip import Trip
from models.invoice import Invoice
from models.payment import Payment
from sqlalchemy import func, extract
from datetime import date
import csv
from io import StringIO

reports_bp = Blueprint('reports', __name__)

# --------- Utility ---------

def export_csv(filename, header, rows):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(header)
    writer.writerows(rows)
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={
        'Content-Disposition': f'attachment; filename={filename}'
    })

# --------- Reports (JSON) ---------

@reports_bp.route('/reports/unpaid-invoices', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def unpaid_invoices():
    invoices = Invoice.query.filter(Invoice.status != 'Paid').all()
    return jsonify([
        {
            'invoice_id': inv.id,
            'trip_id': inv.trip_id,
            'issue_date': str(inv.issue_date),
            'due_date': str(inv.due_date),
            'amount': inv.amount,
            'status': inv.status
        } for inv in invoices
    ])


@reports_bp.route('/reports/monthly-revenue', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def monthly_revenue():
    year = request.args.get('year', type=int)
    destination = request.args.get('destination', type=str)

    query = db.session.query(
        func.strftime('%Y', Payment.payment_date).label('year'),
        func.strftime('%m', Payment.payment_date).label('month'),
        Trip.destination,
        func.sum(Payment.amount).label('total')
    ).select_from(Payment)\
     .join(Invoice, Payment.invoice_id == Invoice.id)\
     .join(Trip, Invoice.trip_id == Trip.id)

    if year:
        query = query.filter(func.strftime('%Y', Payment.payment_date) == str(year))
    if destination:
        query = query.filter(Trip.destination.ilike(f'%{destination}%'))

    results = query.group_by('year', 'month', Trip.destination).order_by('year', 'month').all()

    return jsonify([
        {
            'year': r.year,
            'month': r.month,
            'destination': r.destination,
            'total_revenue': round(r.total, 2)
        } for r in results
    ])



@reports_bp.route('/reports/revenue-by-client', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def revenue_by_client():
    results = db.session.query(
        Client.id, Client.name, func.sum(Payment.amount).label('total_revenue')
    ).join(Trip).join(Invoice).join(Payment).group_by(Client.id, Client.name)\
     .order_by(func.sum(Payment.amount).desc()).all()

    return jsonify([
        {
            'client_id': row.id,
            'client_name': row.name,
            'total_revenue': round(row.total_revenue, 2)
        } for row in results
    ])


@reports_bp.route('/reports/invoice-summary', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def invoice_summary():
    today = date.today()
    invoices = Invoice.query.all()

    paid = [i.id for i in invoices if i.status == 'Paid']
    overdue = [i.id for i in invoices if i.status != 'Paid' and i.due_date < today]
    pending = [i.id for i in invoices if i.status != 'Paid' and i.due_date >= today]

    return jsonify({
        "total_paid": len(paid),
        "paid_invoice_ids": paid,
        "total_pending": len(pending),
        "pending_invoice_ids": pending,
        "total_overdue": len(overdue),
        "overdue_invoice_ids": overdue
    })

# --------- Reports (CSV Export) ---------

@reports_bp.route('/reports/unpaid-invoices/export', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def export_unpaid_invoices():
    invoices = Invoice.query.filter(Invoice.status != 'Paid').all()
    rows = [
        [inv.id, inv.trip_id, inv.amount, inv.issue_date, inv.due_date, inv.status]
        for inv in invoices
    ]
    return export_csv('unpaid_invoices.csv',
        ['Invoice ID', 'Trip ID', 'Amount', 'Issue Date', 'Due Date', 'Status'], rows)


@reports_bp.route('/reports/monthly-revenue/export', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def export_monthly_revenue():
    year = request.args.get('year', type=int)
    destination = request.args.get('destination', type=str)

    query = db.session.query(
        func.strftime('%Y', Payment.payment_date).label('year'),
        func.strftime('%m', Payment.payment_date).label('month'),
        Trip.destination,
        func.sum(Payment.amount).label('total')
    ).select_from(Payment)\
     .join(Invoice, Payment.invoice_id == Invoice.id)\
     .join(Trip, Invoice.trip_id == Trip.id)

    if year:
        query = query.filter(func.strftime('%Y', Payment.payment_date) == str(year))
    if destination:
        query = query.filter(Trip.destination.ilike(f'%{destination}%'))

    results = query.group_by('year', 'month', Trip.destination).order_by('year', 'month').all()

    rows = [[r.year, r.month, r.destination, round(r.total, 2)] for r in results]

    return export_csv('monthly_revenue.csv',
        ['Year', 'Month', 'Destination', 'Total Revenue'], rows)



@reports_bp.route('/reports/revenue-by-client/export', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def export_revenue_by_client():
    results = db.session.query(
        Client.id, Client.name, func.sum(Payment.amount)
    ).join(Trip).join(Invoice).join(Payment)\
     .group_by(Client.id, Client.name).order_by(func.sum(Payment.amount).desc()).all()

    rows = [[r.id, r.name, round(r[2], 2)] for r in results]

    return export_csv('revenue_by_client.csv',
        ['Client ID', 'Client Name', 'Total Revenue'], rows)


@reports_bp.route('/reports/invoice-summary/export', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def export_invoice_summary():
    today = date.today()
    invoices = Invoice.query.all()

    paid = [i.id for i in invoices if i.status == 'Paid']
    overdue = [i.id for i in invoices if i.status != 'Paid' and i.due_date < today]
    pending = [i.id for i in invoices if i.status != 'Paid' and i.due_date >= today]

    rows = [
        ['Paid', ", ".join(map(str, paid)), len(paid)],
        ['Pending', ", ".join(map(str, pending)), len(pending)],
        ['Overdue', ", ".join(map(str, overdue)), len(overdue)],
    ]

    return export_csv('invoice_summary.csv',
        ['Status', 'Invoice IDs', 'Total Count'], rows)
