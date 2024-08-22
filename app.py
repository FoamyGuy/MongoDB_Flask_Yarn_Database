import datetime
import json

from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, request, Response, send_from_directory, render_template
from bson.json_util import dumps

app = Flask(__name__)

def utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)
def get_database(name):
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create / Get the database and return the connection to it.
    return client[name]

@app.route("/", methods=['GET'])
def index():
    return send_from_directory("static", "index.html")


@app.route("/add/yarn", methods=['GET'])
def add_yarn():
    return send_from_directory("static", "add_yarn.html")


@app.route("/edit/yarn/<yarn_id>", methods=['GET', 'POST', 'DELETE'])
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