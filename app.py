from flask import Flask, Response, request, redirect, url_for
from flask_cors import CORS
from flask_dance.contrib.google import google, make_google_blueprint
import json
import os

from RDBResource import UserResource, AddressResource
from context import get_google_blueprint_info
from security import check_authentication
from notification import SNSNotificationHandler

app = Flask(__name__)

# -------------------- authentication --------------------

CORS(app)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
app.secret_key = "e6156"
google_blueprint_info = get_google_blueprint_info()
google_blueprint = make_google_blueprint(
    client_id = google_blueprint_info["client_id"],
    client_secret = google_blueprint_info["client_secret"],
    scope = ["profile", "email"]
)
app.register_blueprint(google_blueprint, url_prefix="/login")
# google_blueprint = app.blueprints.get("google")

@app.before_request
def before_request():
    is_authenticated = check_authentication(request, google)
    if not is_authenticated:
        return redirect(url_for('google.login'))

# -------------------- notification --------------------

@app.after_request
def after_request(response):
    SNSNotificationHandler.notify_if_any(request)
    return response

# -------------------- GET / --------------------

@app.route('/')
def index():
    google_data = google.get("/oauth2/v2/userinfo").json()
    user_email = google_data.get("email", None)
    if user_email:
        response = Response(f"Welcome, {user_email}", status=200)
    else:
        response = Response("index", status=200)
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
    result = UserResource.find_all()
    response = Response(json.dumps(result), status=200, content_type="application/json")
    return response

@app.route('/api/users', methods = ['POST'])
def create_user():
    row_data = request.get_json()
    user_id = UserResource.create(row_data)
    response = Response("Successfully created user!", status=200)
    response.headers['Location'] = f"/api/users/{user_id}"
    response.headers.add('Access-Control-Expose-Headers', 'Location')
    return response

# -------------------- GET, PUT, DELETE /api/users/<user_id> --------------------

@app.route('/api/users/<user_id>', methods = ['GET'])
def retrieve_user(user_id):
    template = {"user_id": user_id}
    fields_str = request.args.get('fields')
    field_list = fields_str.split(",") if fields_str else None
    result = UserResource.find_by_template(template, field_list)
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
    addr_id = AddressResource.create(row_data)

    template = {"user_id": user_id}
    new_data = {"addr_id": addr_id}
    UserResource.update(template, new_data)
    response = Response("Successfully created address for user!", status=200)
    return response

# ------------------- main function -------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
