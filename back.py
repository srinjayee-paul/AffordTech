import requests

# API Endpoints
REGISTRATION_URL = "http://20.244.56.144/evaluation-service/register"
AUTH_URL = "http://20.244.56.144/evaluation-service/auth"

# Registration Data
registration_data = {
    "email": "2229075@kiit.ac.in",
    "name": "Srinjayee Paul",
    "mobileNo": "9654352012",
    "githubUsername": "srinjayee-paul",
    "rollNo": "2229075",
    "collegeName": "Kalinga Institute of Industrial Technologies",
    "accessCode": "nwpwrZ"
}

# Step 1: Register with the test server
response = requests.post(REGISTRATION_URL, json=registration_data)

if response.status_code == 200:
    credentials = response.json()
    print("Registration Successful!")
    print(credentials)

    # Extract client credentials
    client_id = credentials["clientID"]
    client_secret = credentials["clientSecret"]
    email = credentials["email"]
    name = credentials["name"]
    roll_no = credentials["rollNo"]
    access_code = credentials["accessCode"]

    # Step 2: Get Authorization Token
    auth_data = {
        "email": email,
        "name": name,
        "rollNo": roll_no,
        "accessCode": access_code,
        "clientID": client_id,
        "clientSecret": client_secret
    }

    auth_response = requests.post(AUTH_URL, json=auth_data)

    if auth_response.status_code == 200:
        auth_token = auth_response.json()
        print("Authorization Token Obtained Successfully!")
        print(auth_token)
    else:
        print("Failed to obtain authorization token:", auth_response.text)
else:
    print("Registration Failed:", response.text)
