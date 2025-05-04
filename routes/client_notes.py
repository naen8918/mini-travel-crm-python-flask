from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from auth.permissions import role_required
from app import db
from models.client_note import ClientNote
from models.client import Client


notes_bp = Blueprint('client_notes', __name__)

# Create a note
@notes_bp.route('/clients/<int:client_id>/notes', methods=['POST'])
@jwt_required()
@role_required('admin', 'agent')
def add_note(client_id):
    # Validate that the client exists
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    data = request.get_json()
    text = data.get('note')
    if not text:
        return jsonify({'error': 'Note text is required'}), 400

    new_note = ClientNote(client_id=client_id, note=text)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note added successfully'}), 201


# Update a note
@notes_bp.route('/clients/<int:client_id>/notes/<int:note_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin', 'agent')
def update_note(client_id, note_id):
    # Ensure client exists
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    note = ClientNote.query.filter_by(id=note_id, client_id=client_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    data = request.get_json()
    new_text = data.get('note')
    if not new_text:
        return jsonify({'error': 'Updated note text is required'}), 400

    note.note = new_text
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'}), 200


# Delete a note
@notes_bp.route('/clients/<int:client_id>/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_note(client_id, note_id):
    
    # Ensure client exists
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404


    note = ClientNote.query.filter_by(id=note_id, client_id=client_id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404


    db.session.delete(note)
    db.session.commit()
    
    return jsonify({'message': 'Note deleted successfully'}), 200
