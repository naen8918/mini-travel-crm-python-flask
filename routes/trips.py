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
