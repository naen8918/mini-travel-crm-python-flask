from flask import Blueprint, request, jsonify
from app import db
from models.trip import Trip
from datetime import datetime  # import datetime

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/trips', methods=['POST'])
def create_trip():
    data = request.get_json()

    # Convert string dates to Python date objects
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    new_trip = Trip(
        destination=data['destination'],
        start_date=start_date,  # use parsed date
        end_date=end_date,      # use parsed date
        price=data['price'],
        notes=data.get('notes'),
        client_id=data['client_id']
    )

    db.session.add(new_trip)
    db.session.commit()

    return jsonify({'message': 'Trip created successfully'})

# GET /trips
@trips_bp.route('/trips', methods=['GET'])
def get_trips():
    trips = Trip.query.all()
    result = [
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
    ]
    return jsonify(result)

# PATCH /trips/<trip_id>
@trips_bp.route('/trips/<int:trip_id>', methods=['PATCH'])
def update_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    if 'destination' in data:
        trip.destination = data['destination']
    if 'start_date' in data:
        trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    if 'end_date' in data:
        trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    if 'price' in data:
        trip.price = data['price']
    if 'notes' in data:
        trip.notes = data['notes']
    if 'client_id' in data:
        trip.client_id = data['client_id']

    db.session.commit()
    return jsonify({'message': 'Trip updated successfully'})

# DELETE /trips/<trip_id>
@trips_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    db.session.delete(trip)
    db.session.commit()

    return jsonify({'message': 'Trip deleted successfully'})
