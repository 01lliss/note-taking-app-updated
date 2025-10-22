import os
import logging
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Read configuration from environment with sensible fallbacks for local dev
MONGO_URI = os.getenv('MONGO_URI', "mongodb+srv://llisslucky_db_user:Lss010201A@cluster0.kdqcht3.mongodb.net/")
DATABASE_NAME = os.getenv('DATABASE_NAME', 'note_taking_app')

# Create client and database
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    # Collections
    users = db.users
    notes = db.notes
except Exception:
    logging.exception('Failed to initialize MongoDB client with provided MONGO_URI')
    # Provide placeholders so module import doesn't crash; operations will still fail if used
    client = None
    db = None
    users = None
    notes = None

def serialize_doc(doc):
    """Convert a MongoDB document to JSON-serializable dict and add `id` alias for `_id`."""
    if doc is None:
        return None

    def convert(v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, datetime):
            return v.isoformat()
        if isinstance(v, dict):
            return {k: convert(val) for k, val in v.items()}
        if isinstance(v, list):
            return [convert(x) for x in v]
        return v

    result = {k: convert(val) for k, val in doc.items()}
    # Ensure `id` is present as a string (frontend expects note.id)
    if '_id' in result and result['_id'] is not None:
        result['id'] = result['_id']
    elif '_id' in doc:
        # fallback to stringifying original ObjectId value
        result['id'] = str(doc.get('_id'))

    return result
