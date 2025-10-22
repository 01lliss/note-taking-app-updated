from src.models.database import notes
from datetime import datetime
from bson import ObjectId

class Note:
    @staticmethod
    def create(title, content):
        note = {
            'title': title,
            'content': content,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = notes.insert_one(note)
        note['_id'] = result.inserted_id
        return note

    @staticmethod
    def find_by_id(note_id):
        return notes.find_one({'_id': ObjectId(note_id)})

    @staticmethod
    def update(note_id, title, content):
        return notes.update_one({'_id': ObjectId(note_id)}, {'$set': {'title': title, 'content': content, 'updated_at': datetime.utcnow()}})

    @staticmethod
    def delete(note_id):
        return notes.delete_one({'_id': ObjectId(note_id)})

    @staticmethod
    def list_all():
        return list(notes.find())

