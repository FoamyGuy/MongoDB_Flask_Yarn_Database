
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, dict):
    def __init__(self, db_client, username):

        found_user = db_client.find_one({'username': username})
        if found_user is None:
            raise ValueError("User Not Found")

        super().__init__()

        self.db_client = db_client
        for key, value in found_user.items():
            self[key] = value

    def set_password(self, password):
        self['password_hash'] = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self['password_hash'], password)

    def save(self):
        self.db_client.update_one({"_id": self["_id"]}, {"$set": self})

    def get_id(self):
        return self['username']

    @staticmethod
    def create_user(db_client, username, password):
        db_client.insert_one({'username': username, 'password_hash': generate_password_hash(password)})
