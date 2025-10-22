from src.models.database import users
from bson import ObjectId

class User:
    @staticmethod
    def create(username, email):
        user = {'username': username, 'email': email}
        result = users.insert_one(user)
        user['_id'] = result.inserted_id
        return user

    @staticmethod
    def find_by_id(user_id):
        return users.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def find_by_username(username):
        return users.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        return users.find_one({'email': email})

    @staticmethod
    def list_all():
        return list(users.find())
