from re import template
from flask import Flask, Response, request
import json

from RDBResource import UserResource, AddressResource

app = Flask(__name__)

@app.route('/')
def index():
    return "index"

# -------------------- GET, POST /addresses --------------------

@app.route('/addresses', methods = ['GET'])
def get_addresses():
    result = AddressResource.find_all()
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/addresses', methods = ['POST'])
def create_address():
    row_data = request.get_json()
    AddressResource.create(row_data)
    response = Response("Successfully created address!", status=200)
    return response

# -------------------- GET, PUT, DELETE /addresses/<addr_id> --------------------

@app.route('/addresses/<addr_id>', methods = ['GET'])
def get_address(addr_id):
    template = {"addr_id": addr_id}
    result = AddressResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/addresses/<addr_id>', methods = ['PUT'])
def update_address(addr_id):
    template = {"addr_id": addr_id}
    new_data = request.get_json()
    AddressResource.update(template, new_data)
    response = Response("Successfully updated address!", status=200)
    return response

@app.route('/addresses/<addr_id>', methods = ['DELETE'])
def delete_address(addr_id):
    template = {"addr_id": addr_id}
    AddressResource.delete(template)
    response = Response("Successfully deleted address!", status=200)
    return response

# -------------------- GET, POST /addresses/<addr_id>/users --------------------

@app.route('/addresses/<addr_id>/users', methods = ['GET'])
def retrieve_user_under_address(addr_id):
    template = {"addr_id": addr_id}
    result = UserResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/addresses/<addr_id>/users', methods = ['POST'])
def create_user_under_address(addr_id):
    row_data = request.get_json()
    row_data["addr_id"] = addr_id
    UserResource.create(row_data)
    response = Response("Successfully created user under address!", status=200)
    return response

# -------------------- GET, POST /users --------------------

@app.route('/users', methods = ['GET'])
def retrieve_users():
    result = UserResource.find_all()
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/users', methods = ['POST'])
def create_user():
    row_data = request.get_json()
    UserResource.create(row_data)
    response = Response("Successfully created user!", status=200)
    return response

# -------------------- GET, PUT, DELETE /users/<user_id> --------------------

@app.route('/users/<user_id>', methods = ['GET'])
def retrieve_user(user_id):
    template = {"user_id": user_id}
    result = UserResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/users/<user_id>', methods = ['PUT'])
def update_user(user_id):
    template = {"user_id": user_id}
    new_data = request.get_json()
    UserResource.update(template, new_data)
    response = Response("Successfully updated user!", status=200)
    return response

@app.route('/users/<user_id>', methods = ['DELETE'])
def delete_user(user_id):
    template = {"user_id": user_id}
    UserResource.delete(template)
    response = Response("Successfully deleted user!", status=200)
    return response

# -------------------- GET, POST /users/<user_id>/address --------------------

@app.route('/users/<user_id>/address', methods = ['GET'])
def get_address_of_user(user_id):
    template = {"user_id": user_id}
    result = UserResource.find_by_template(template)

    addr_id = result[0]["addr_id"]
    template = {"addr_id": addr_id}
    result = AddressResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/users/<user_id>/address', methods = ['POST'])
def create_address_for_user(user_id):
    row_data = request.get_json()
    addr_id = AddressResource.create(row_data)

    template = {"user_id": user_id}
    new_data = {"addr_id": addr_id}
    UserResource.update(template, new_data)
    response = Response("Successfully created address for user!", status=200)
    return response
