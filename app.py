import datetime
import json
import os

from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, request, Response, send_from_directory, render_template, redirect, session
from bson.json_util import dumps
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from models import User

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY").encode("utf-8")

login = LoginManager(app)
login.login_view = 'login'

def utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)
def get_database(name):
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create / Get the database and return the connection to it.
    return client[name]

@login.user_loader
def load_user(user_id):
    print(f"user_id: {user_id}")
    db = get_database("yarn_databus")
    users_db = db["users"]
    user = User(users_db, user_id)
    return user

@app.route("/", methods=['GET'])
@login_required
def index():

    return send_from_directory("static", "index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return send_from_directory("static", "login.html")

    elif request.method == 'POST':
        print(request.form['username'])
        username = request.form['username']
        incoming_password = request.form['password']
        db = get_database("yarn_databus")
        users_db = db["users"]
        try:
            user = User(users_db, username)
        except ValueError:
            return Response("Incorrect Username or Password", status=401)

        if user.check_password(incoming_password):
            login_user(user)
            return redirect("/")
        else:
            return Response("Incorrect Username or Password", status=401)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/add/yarn", methods=['GET'])
@login_required
def add_yarn():
    return send_from_directory("static", "add_yarn.html")


@app.route("/edit/yarn/<yarn_id>", methods=['GET', 'POST', 'DELETE'])
@login_required
def edit_yarn(yarn_id):
    db = get_database("yarn_databus")
    yarn_data = db["yarns"]
    found_yarn = yarn_data.find_one({"_id": ObjectId(yarn_id)})
    if found_yarn is None:
        return Response(status=404)

    if request.method == "GET":
        #print(yarn_id)
        found_yarn["hex_color"] = hex(found_yarn["color"])[2:].zfill(6)

        return render_template("edit_yarn.html", yarn_obj=found_yarn)
    elif request.method == "POST":
        json_data = request.get_json()
        required_fields = ["color", "amount"]
        missing_fields = []
        for field in required_fields:
            if field not in json_data:
                missing_fields.append(field)
        if len(missing_fields) > 0:
            return json.dumps({"error": "Missing fields: {}".format(missing_fields)})

        result = yarn_data.update_one({"_id": ObjectId(yarn_id)}, {"$set": json_data})
        return json.dumps({"result": str(result)})
    elif request.method == "DELETE":
        json_data = request.get_json()
        required_fields = ["yarn_id"]
        missing_fields = []
        for field in required_fields:
            if field not in json_data:
                missing_fields.append(field)
        if len(missing_fields) > 0:
            return json.dumps({"error": "Missing fields: {}".format(missing_fields)})
        if yarn_id != json_data["yarn_id"]:
            return json.dumps({"error": "Yarn ID mismatch"})
        result = yarn_data.delete_one({"_id": ObjectId(yarn_id)})
        return json.dumps({"result": str(result)})
@app.route("/yarn", methods=['GET', 'POST'])
@login_required
def yarn():
    """
    URL: /yarn
    Methods: GET, POST

    Fetch or Insert Yarn data.

    GET Args:


    POST Content-Type: application/json
    POST Args (JSON Body):
      color (string): The color of the yarn.
      amount (string): How many are available. Units can be specified i.e. 3 scanes
    """
    db = get_database("yarn_databus")
    yarn_data = db["yarns"]
    if request.method == 'GET':
        all_yarn_data = yarn_data.find()
        return Response(dumps(all_yarn_data), content_type="application/json")

    if request.method == 'POST':
        json_data = request.get_json()
        required_fields = ["color", "amount"]
        missing_fields = []
        for field in required_fields:
            if field not in json_data:
                missing_fields.append(field)
        if len(missing_fields) > 0:
            return json.dumps({"error": "Missing fields: {}".format(missing_fields)})
        result = yarn_data.insert_one(json_data)
        return json.dumps({"result": str(result)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)