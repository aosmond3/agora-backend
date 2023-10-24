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


@app.route("/api/users/groups", methods=["GET"])
def api_get_groups_for_user():
    pass



# @app.route("/api/users/join/group", methods=["POST"]) # TODO: probably need to modify how I am receiving inputs
# def api_user_join_group(user_uuid: int, group_id: int, group_password: str):
#     # validate password
#     return jsonify(da.get_group_password())

@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form["username"]
    password = request.form["password"]

    password_response = da.get_user_password(username)
    if not password_response:
        # TODO: error handling
        print("username not found")
        return jsonify({"logged in": "fail: username not found"})

    if (password != password_response["password"]):
        # TODO: error handling
        print("incorrect password")
        return jsonify({"logged in": "fail: incorr pass"})

    return jsonify({"logged in": "succ"})
#  Consider: maybe succ login returns a secret key that is
# needed to query groups and everything for the user

# or maybe unsucc login just prevents user from reaching other webpage
# so we dont need to worry about secret key


