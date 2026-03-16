from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from __init__ import db
from model.note import Note

note_bp  = Blueprint('note', __name__)
note_api = Api(note_bp)


class NoteListAPI(Resource):
    def get(self):
        """Return all notes, newest first."""
        notes = db.session.query(Note).order_by(Note.id.desc()).all()
        return [n.to_dict() for n in notes], 200

    def post(self):
        """Create a new note."""
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400

        content = (data.get('content') or '').strip()
        if not content:
            return {'error': 'Content is required'}, 400

        note = Note(
            author     = (data.get('author') or 'Anonymous').strip(),
            content    = content,
            image_data = data.get('image_data'),
            image_type = data.get('image_type'),
        )
        result = note.create()
        if not result:
            return {'error': 'Failed to save note'}, 500
        return result.to_dict(), 201


class NoteDetailAPI(Resource):
    def delete(self, note_id):
        """Delete a note by id."""
        note = db.session.query(Note).filter_by(id=note_id).first()
        if not note:
            return {'error': 'Note not found'}, 404
        note.delete()
        return {'message': 'Deleted'}, 200


class NoteLikeAPI(Resource):
    def post(self, note_id):
        """Like a note."""
        note = db.session.query(Note).filter_by(id=note_id).first()
        if not note:
            return {'error': 'Note not found'}, 404
        note.likes += 1
        db.session.commit()
        return {'likes': note.likes}, 200


note_api.add_resource(NoteListAPI,   '/api/notes')
note_api.add_resource(NoteDetailAPI, '/api/notes/<int:note_id>')
note_api.add_resource(NoteLikeAPI,   '/api/notes/<int:note_id>/like')