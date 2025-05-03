from flask import Blueprint, request, jsonify
from app import db
from auth.models import User
from auth.utils import hash_password, verify_password
from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 409

    user = User(
        username=data['username'],
        role=data.get('role', 'agent')  # Default to 'agent'
    )
    user.password_hash = hash_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not verify_password(data['password'], user.password_hash):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(
    identity=str(user.id),  #  identity must be a string
    additional_claims={"role": user.role})  #  attach role to token payload


    return jsonify({'access_token': access_token})

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    jwt_data = get_jwt()
    return jsonify({
        'user_id': current_user,
        'role': jwt_data.get('role')
    })