from flask import Flask, render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv
from configuration.sqlite import *
from configuration.sendemail import *
from configuration.appconfig import get_access_token
from configuration.api_response import post_response
from configuration.test_api import fetch_users, use_api, test_email
from configuration.submitform import contact_form
import requests

app = Flask(__name__)
load_dotenv()

access_token = get_access_token()

#Fetch users to automatically transfer to database (if successfully connected to API)
if access_token:
    users = fetch_users()
    fetch_users_to_database(users)
    fetch_from_database_to_api(users)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/terms_and_privacy')
def terms_and_privacy_page():
    return render_template("content.html")
    

@app.route('/create_user', methods=['POST'])
def create_user():
    # Get the user data from the request body
    user_data = request.json
    try:
        # Send POST request to the API endpoint
        response = post_response(user_data)

        
        # Check if the user creation was successful
        if response.status_code == 201:
            return jsonify({"message": "User created successfully."}), 201
        else:
            return jsonify({"error": f"Failed to create user: {response.status_code} - {response.text}"}), response.status_code
        

    except requests.ConnectionError:
        return jsonify({"error": "Failed to create user: Unable to connect to the website."}), 500
    except requests.Timeout:
        return jsonify({"error": "Failed to create user: The request timed out."}), 504
    except Exception as e:
        return jsonify({"error": f"Failed to create user: An error occurred: {str(e)}"}), 500

@app.route('/test_create_user')
def test_create_user():
    # Sample data with "John Doe" based on the Blackboard API structure
    sample_data = {
        "userName": "sample",
        "password": "yes",
        "gender": "Male",
        "institutionRoleIds": ["STUDENT"],
        "systemRoleIds": ["User"],
        "availability": {"available": "Yes"},
        "name": {
            "given": "Sample",
            "family": "Text",
            },
        "contact": {
            "email": "micobarrios@gmail.com"
            }
    }
    
    send_user_email(sample_data)
    send_to_database(sample_data)
    
    # Send a request to the /create_user endpoint with this sample data
    with app.test_client() as client:
        response = client.post('/create_user', json=sample_data)
        
        
        # Display the response for debugging purposes
        return response.get_json(), response.status_code

@app.route('/submit_contact_form', methods=["POST"])
def submit_contact_form():
    form = contact_form()
    send_contact_email(form)

    return redirect(url_for('index') + "#contact-section")

# BEYOND THIS POINT ARE ROUTES TO TEST BLACKBOARD API & EMAIL SUBMISSION#
@app.route('/use_api')
def use_api_page():
    return use_api()

@app.route('/fetch_users')
def fetch_users_page():
    return fetch_users()

@app.route('/test_email')
def test_email_page():
    return test_email()

if __name__ == '__main__':
    app.run(debug=True)
