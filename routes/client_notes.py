from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from auth.permissions import role_required
from app import db
from models.client_note import ClientNote
from models.client import Client

notes_bp = Blueprint('client_notes', __name__)

# 🔹 Helper to retrieve a client or return 404
def get_client_or_404(client_id):
    client = Client.query.get(client_id)
    if not client:
        return None, jsonify({'error': 'Client not found'}), 404
    return client, None, None

# ------------------------------
# 📌 POST /clients/<id>/notes
# ------------------------------
@notes_bp.route('/clients/<int:client_id>/notes', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def add_note(client_id):
    client, error_response, status = get_client_or_404(client_id)
    if error_response:
        return error_response, status

    data = request.get_json()
    note_text = data.get('note')
    if not note_text or not isinstance(note_text, str):
        return jsonify({'error': 'Valid note text is required'}), 400

    new_note = ClientNote(client_id=client.id, note=note_text.strip())
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note added successfully'}), 201

# ------------------------------
# 📝 PATCH /clients/<id>/notes/<id>
# ------------------------------
@notes_bp.route('/clients/<int:client_id>/notes/<int:note_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin', 'agent')
def update_note(client_id, note_id):
    client, error_response, status = get_client_or_404(client_id)
    if error_response:
        return error_response, status

    note = ClientNote.query.filter_by(id=note_id, client_id=client_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    data = request.get_json()
    new_text = data.get('note')
    if not new_text or not isinstance(new_text, str):
        return jsonify({'error': 'Valid updated note text is required'}), 400

    note.note = new_text.strip()
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'}), 200

# ------------------------------
# 📋 GET /clients/<id>/notes
# ------------------------------
@notes_bp.route('/clients/<int:client_id>/notes', methods=['GET'])
@jwt_required()
@role_required('admin', 'agent', 'analyst')
def get_notes(client_id):
    client, error_response, status = get_client_or_404(client_id)
    if error_response:
        return error_response, status

    notes = ClientNote.query.filter_by(client_id=client_id).all()
    return jsonify([
        {
            'id': note.id,
            'note': note.note,
            'timestamp': note.timestamp.isoformat()
        }
        for note in notes
    ]), 200

# ------------------------------
# ❌ DELETE /clients/<id>/notes/<id>
# ------------------------------
@notes_bp.route('/clients/<int:client_id>/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_note(client_id, note_id):
    client, error_response, status = get_client_or_404(client_id)
    if error_response:
        return error_response, status

    note = ClientNote.query.filter_by(id=note_id, client_id=client_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'}), 200
