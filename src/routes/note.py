from flask import Blueprint, jsonify, request
from src.models.note import Note
from src.models.database import serialize_doc
from bson.errors import InvalidId

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    all_notes = Note.list_all()
    # sort locally by updated_at desc if necessary
    try:
        sorted_notes = sorted(all_notes, key=lambda n: n.get('updated_at', None), reverse=True)
    except Exception:
        sorted_notes = all_notes
    return jsonify([serialize_doc(n) for n in sorted_notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400

        note = Note.create(data['title'], data['content'])
        return jsonify(serialize_doc(note)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    try:
        note = Note.find_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(serialize_doc(note))
    except InvalidId:
        return jsonify({'error': 'Invalid note ID'}), 400

@note_bp.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        note = Note.find_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        result = Note.update(note_id, data.get('title', note.get('title')), data.get('content', note.get('content')))
        if result.modified_count == 0:
            return jsonify({'error': 'No changes made'}), 400

        updated_note = Note.find_by_id(note_id)
        return jsonify(serialize_doc(updated_note))
    except InvalidId:
        return jsonify({'error': 'Invalid note ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        result = Note.delete(note_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Note not found'}), 404
        return '', 204
    except InvalidId:
        return jsonify({'error': 'Invalid note ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    from src.models.database import notes as notes_collection
    search_results = notes_collection.find({
        '$or': [
            {'title': {'$regex': query, '$options': 'i'}},
            {'content': {'$regex': query, '$options': 'i'}}
        ]
    })

    return jsonify([serialize_doc(n) for n in search_results])

