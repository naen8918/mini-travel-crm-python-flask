from flask import Blueprint, request, jsonify
from app import db
from auth.models import User
from auth.utils import hash_password, verify_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from config import VALID_ROLES


auth_bp = Blueprint('auth', __name__)

# This route will allow frontend to dynamically fetch roles
@auth_bp.route('/roles', methods=['GET'])
def get_valid_roles():
    from config import VALID_ROLES
    return jsonify(sorted(VALID_ROLES)), 200


# ---------------------
# Register Endpoint
# ---------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400

    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'agent')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if role not in VALID_ROLES:
        return jsonify({'error': f'Invalid role. Must be one of {list(VALID_ROLES)}'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    user = User(username=username, role=role)
    user.password_hash = hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# ---------------------
# Login Endpoint
# ---------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({'access_token': token}), 200

# ---------------------
# Current User Info
# ---------------------
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'role': user.role
    })

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():

    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({'error': 'Admins only'}), 403

    users = User.query.all()
    user_list = [
        {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
        for user in users
    ]
    return jsonify(user_list), 200
