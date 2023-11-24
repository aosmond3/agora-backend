import data_accessor as da

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def hello(): # TODO: delete
    return "Hello, World!"


@app.route("/api/users",  methods=["GET"])
def api_get_users():
    return jsonify(da.get_users())


@app.route("/api/users/groups", methods=["GET"])
def api_get_groups_for_user():
    username = request.args.get("username")
    return jsonify(da.get_groups_for_user(username))


@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form["username"]
    password = request.form["password"]

    password_response = da.get_user_password(username)
    if not password_response:
        return jsonify({"status": "fail: username not found"})

    if (password != password_response["password"]):
        return jsonify({"status": "fail: incorrect password"})

    return jsonify({"status": "success"})