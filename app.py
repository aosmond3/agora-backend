import data_accessor as da

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # TODO: research this more

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello(): # TODO: delete
    return "Hello, World!"

@app.route("/api/users",  methods=["GET"])
def api_get_users():
    return jsonify(da.get_users())

# @app.route("/api/users/join/group", methods=["POST"]) # TODO: probably need to modify how I am receiving inputs
# def api_user_join_group(user_uuid: int, group_id: int, group_password: str):
#     # validate password
#     return jsonify(da.get_group_password())

@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form["username"]
    password = request.form["password"]
    print(username, password)


