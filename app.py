from flask import Flask, Response, request, redirect, url_for, g
import json
import uuid

from RDBResource import UserResource, AddressResource
from notification import SNSNotificationHandler

app = Flask(__name__)

# -------------------- authentication --------------------
import requests
from flask_cors import CORS
from context import API_GATEWAY_URL
CORS(app)

@app.before_request
def before_request():

    # verify id_token
    id_token = request.headers.get('id_token')
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    response = requests.get(url)
    user_data = response.json()
    email = user_data.get('email')

    # if not verified, return message
    if not email:
        response = Response("Please provide a valid google id_token!", status=200)
        return response

    # if verified
    template = {'email': email}
    result = UserResource.find_by_template(template)

    # check if user exist
    if len(result) == 0:
        user_id = str(uuid.uuid4())
        template = {
            'user_id': user_id,
            'first_name': user_data['given_name'],
            'last_name': user_data['family_name'],
            'nickname': user_data['email'],
            'email': user_data['email'],
        }
        UserResource.create(template)
    else:
        user_id = result[0]['user_id']

    g.user_id = user_id
    g.email = email

# -------------------- notification --------------------

@app.after_request
def after_request(response):
    SNSNotificationHandler.notify_if_any(request)
    return response

# -------------------- GET / --------------------

@app.route('/')
def index():
    response = Response(f'Hello\n {g.email}\n {g.user_id}', status=200)
    return response

# -------------------- GET, POST /api/addresses --------------------

@app.route('/api/addresses', methods = ['GET'])
def get_addresses():
    result = AddressResource.find_all()
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/addresses', methods = ['POST'])
def create_address():
    row_data = request.get_json()
    row_data['addr_id'] = str(uuid.uuid4())
    AddressResource.create(row_data)
    response = Response("Successfully created address!", status=200)
    return response

# -------------------- GET, PUT, DELETE /api/addresses/<addr_id> --------------------

@app.route('/api/addresses/<addr_id>', methods = ['GET'])
def get_address(addr_id):
    template = {"addr_id": addr_id}
    result = AddressResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/addresses/<addr_id>', methods = ['PUT'])
def update_address(addr_id):
    template = {"addr_id": addr_id}
    new_data = request.get_json()
    AddressResource.update(template, new_data)
    response = Response("Successfully updated address!", status=200)
    return response

@app.route('/api/addresses/<addr_id>', methods = ['DELETE'])
def delete_address(addr_id):
    template = {"addr_id": addr_id}
    AddressResource.delete(template)
    response = Response("Successfully deleted address!", status=200)
    return response

# -------------------- GET, POST /api/addresses/<addr_id>/users --------------------

@app.route('/api/addresses/<addr_id>/users', methods = ['GET'])
def retrieve_user_under_address(addr_id):
    template = {"addr_id": addr_id}
    result = UserResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/addresses/<addr_id>/users', methods = ['POST'])
def create_user_under_address(addr_id):
    row_data = request.get_json()
    row_data["addr_id"] = addr_id
    UserResource.create(row_data)
    response = Response("Successfully created user under address!", status=200)
    return response

# -------------------- GET, POST /api/users --------------------

@app.route('/api/users', methods = ['GET'])
def retrieve_users():
    # assume parameter key is either user table column name or field
    template = {}
    field_list = []
    for key in request.args:
        vals = request.args.get(key).split(",")
        if key == "fields":
            field_list.extend(vals)
        else:
            if len(vals) == 1:
                template[key] = vals[0]
            else:
                template[key] = vals
    field_list = field_list if len(field_list) else None
    
    result = UserResource.find_by_template(template, field_list)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/users', methods = ['POST'])
def create_user():
    row_data = request.get_json()
    row_data['user_id'] = str(uuid.uuid4())
    UserResource.create(row_data)
    user_id = row_data['user_id']
    response = Response("Successfully created user!", status=200)
    response.headers['Location'] = f"/api/users/{user_id}"
    response.headers.add('Access-Control-Expose-Headers', 'Location')
    return response

# @app.route('/api/users/search', methods = ['POST'])
# def retrieve_users_with_ids():
    # post body must be 
    # {
    #   "template": {
    #       "user_id": ["aaa", "bbb", "cccc"],
    #       "col_2": list of values
    #       ...
    #   },
    #   "field_list": ["user_id", "nickname"]
    # }

# -------------------- GET, PUT, DELETE /api/users/<user_id> --------------------

@app.route('/api/users/<user_id>', methods = ['GET'])
def retrieve_user(user_id):
    template = {"user_id": user_id}
    fields_str = request.args.get('fields')
    field_list = fields_str.split(",") if fields_str else None
    result = UserResource.find_by_template(template, field_list)
    links = UserResource.get_links(result[0])
    result[0]['links'] = links
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/users/<user_id>', methods = ['PUT'])
def update_user(user_id):
    template = {"user_id": user_id}
    new_data = request.get_json()
    UserResource.update(template, new_data)
    response = Response("Successfully updated user!", status=200)
    return response

@app.route('/api/users/<user_id>', methods = ['DELETE'])
def delete_user(user_id):
    template = {"user_id": user_id}
    UserResource.delete(template)
    response = Response("Successfully deleted user!", status=200)
    return response

# -------------------- GET, POST /api/users/<user_id>/address --------------------

@app.route('/api/users/<user_id>/address', methods = ['GET'])
def get_address_of_user(user_id):
    template = {"user_id": user_id}
    result = UserResource.find_by_template(template)

    addr_id = result[0]["addr_id"]
    template = {"addr_id": addr_id}
    result = AddressResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/users/<user_id>/address', methods = ['POST'])
def create_address_for_user(user_id):
    row_data = request.get_json()
    row_data['addr_id'] = str(uuid.uuid4())
    AddressResource.create(row_data)
    addr_id = row_data['addr_id']

    template = {"user_id": user_id}
    new_data = {"addr_id": addr_id}
    UserResource.update(template, new_data)
    response = Response("Successfully created address for user!", status=200)
    return response

# -------------------- GET, POST /api/users/whoami --------------------
@app.route('/api/users/whoami', methods = ['GET'])
def get_whoami():
    template = {"user_id": g.user_id}
    result = UserResource.find_by_template(template)
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

# ------------------- main function -------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
