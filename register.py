import argparse
import getpass
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

from models import User

def get_database(name):
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create / Get the database and return the connection to it.
    return client[name]

parser = argparse.ArgumentParser()
parser.add_argument("--username", type=str, required=True, help="Username for the new user")

args = parser.parse_args()
password = getpass.getpass(prompt="Password: ", stream=None)

db = get_database("yarn_databus")
users_db = db["users"]
try:
    user = User(users_db, args.username)
    user["password_hash"] = generate_password_hash(password)
except ValueError:
    User.create_user(users_db, args.username, password)
