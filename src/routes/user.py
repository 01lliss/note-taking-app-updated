from flask import Blueprint, jsonify, request
from src.models.user import User
from src.models.database import serialize_doc
from bson.errors import InvalidId

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.list_all()
    return jsonify([serialize_doc(u) for u in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Username and email are required'}), 400

    if User.find_by_username(data['username']) or User.find_by_email(data['email']):
        return jsonify({'error': 'Username or email already exists'}), 400

    user = User.create(data['username'], data['email'])
    return jsonify(serialize_doc(user)), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(serialize_doc(user))
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if 'username' in data and data['username'] != user['username']:
            existing_user = User.find_by_username(data['username'])
            if existing_user and str(existing_user['_id']) != user_id:
                return jsonify({'error': 'Username already taken'}), 400

        if 'email' in data and data['email'] != user['email']:
            existing_user = User.find_by_email(data['email'])
            if existing_user and str(existing_user['_id']) != user_id:
                return jsonify({'error': 'Email already taken'}), 400

        update_data = {}
        if 'username' in data:
            update_data['username'] = data['username']
        if 'email' in data:
            update_data['email'] = data['email']

        from src.models.database import users as users_collection
        users_collection.update_one({'_id': __import__('bson').ObjectId(user_id)}, {'$set': update_data})

        updated_user = User.find_by_id(user_id)
        return jsonify(serialize_doc(updated_user))
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        from src.models.database import users as users_collection
        result = users_collection.delete_one({'_id': __import__('bson').ObjectId(user_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'User not found'}), 404
        return '', 204
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400
