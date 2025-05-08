from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.permissions import role_required
from app import db
from models.trip import Trip
from models.client import Client
from datetime import datetime

trips_bp = Blueprint('trips', __name__)

# ------------------------
# CREATE A NEW TRIP
# ------------------------
@trips_bp.route('/trips', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def create_trip():
    user_id = get_jwt_identity()
    print(f"Trip created by user: {user_id}")

    data = request.get_json()

    required_fields = ['destination', 'start_date', 'end_date', 'price', 'client_id']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        price = float(data['price'])
        client_id = int(data['client_id'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data format for date, price, or client_id'}), 400

    # Check if client exists
    if not Client.query.get(client_id):
        return jsonify({'error': 'Client not found'}), 404

    trip = Trip(
        destination=data['destination'],
        start_date=start_date,
        end_date=end_date,
        price=price,
        notes=data.get('notes'),
        client_id=client_id
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify({'message': 'Trip created successfully'}), 201


# ------------------------
# LIST TRIPS WITH FILTERS
# ------------------------
@trips_bp.route('/trips', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')
def get_trips():
    destination = request.args.get('destination')
    client_id = request.args.get('client_id', type=int)
    start_date = request.args.get('start_date')  # Format: YYYY-MM-DD

    query = Trip.query

    if destination:
        query = query.filter(Trip.destination.ilike(f"%{destination}%"))
    if client_id:
        query = query.filter(Trip.client_id == client_id)
    if start_date:
        try:
            parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Trip.start_date >= parsed)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format (expected YYYY-MM-DD)'}), 400

    trips = query.all()

    return jsonify([
        {
            'id': t.id,
            'destination': t.destination,
            'start_date': str(t.start_date),
            'end_date': str(t.end_date),
            'price': t.price,
            'notes': t.notes,
            'client_id': t.client_id
        } for t in trips
    ]), 200


# ------------------------
# UPDATE TRIP
# ------------------------
@trips_bp.route('/trips/<int:trip_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin', 'agent')
def update_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    allowed_fields = {'destination', 'start_date', 'end_date', 'price', 'notes', 'client_id'}
    unknown = [key for key in data if key not in allowed_fields]
    if unknown:
        return jsonify({'error': f"Invalid field(s): {', '.join(unknown)}"}), 400

    if 'destination' in data:
        trip.destination = data['destination']
    if 'start_date' in data:
        try:
            trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid start_date format'}), 400
    if 'end_date' in data:
        try:
            trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid end_date format'}), 400
    if 'price' in data:
        try:
            trip.price = float(data['price'])
        except ValueError:
            return jsonify({'error': 'Price must be a number'}), 400
    if 'notes' in data:
        trip.notes = data['notes']
    if 'client_id' in data:
        try:
            client_id = int(data['client_id'])
        except ValueError:
            return jsonify({'error': 'client_id must be an integer'}), 400
        if not Client.query.get(client_id):
            return jsonify({'error': 'Client not found'}), 404
        trip.client_id = client_id

    db.session.commit()
    return jsonify({'message': 'Trip updated successfully'}), 200


# ------------------------
# DELETE TRIP
# ------------------------
@trips_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    db.session.delete(trip)
    db.session.commit()

    return jsonify({'message': 'Trip deleted successfully'}), 200
