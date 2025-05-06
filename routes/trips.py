from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth.permissions import role_required
from app import db
from models.trip import Trip
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

    try:
        new_trip = Trip(
            destination=data['destination'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            price=data['price'],
            notes=data.get('notes'),
            client_id=data['client_id']
        )
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400

    db.session.add(new_trip)
    db.session.commit()

    return jsonify({'message': 'Trip created successfully'}), 201

# ------------------------
# LIST TRIPS WITH FILTERS
# ------------------------
@trips_bp.route('/trips', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')
def get_trips():
    # Optional filters
    destination = request.args.get('destination')
    client_id = request.args.get('client_id', type=int)
    start_date = request.args.get('start_date')  # YYYY-MM-DD

    query = Trip.query

    if destination:
        query = query.filter(Trip.destination.ilike(f"%{destination}%"))
    if client_id:
        query = query.filter(Trip.client_id == client_id)
    if start_date:
        try:
            start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Trip.start_date >= start_date_parsed)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format (expected YYYY-MM-DD)'}), 400

    trips = query.all()

    return jsonify([
        {
            'id': trip.id,
            'destination': trip.destination,
            'start_date': str(trip.start_date),
            'end_date': str(trip.end_date),
            'price': trip.price,
            'notes': trip.notes,
            'client_id': trip.client_id
        }
        for trip in trips
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
        trip.price = data['price']
    if 'notes' in data:
        trip.notes = data['notes']
    if 'client_id' in data:
        trip.client_id = data['client_id']

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
