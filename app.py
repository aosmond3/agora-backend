import data_accessor as da

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # TODO: research this more

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello(): # TODO: delete
    return "Hello, World!"

@app.route("/api/users",  methods=['GET'])
def api_get_users():
    return jsonify(da.get_users())
