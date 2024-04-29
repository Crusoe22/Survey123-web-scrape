import requests

# Your ArcGIS username and password
username = "Nolan_HUD"
password = "nolanm1%HUD"

# URL of the API endpoint to fetch data
api_url = "https://services.arcgis.com/B1yJ6W2oC1kUrC5J/arcgis/rest/services/survey123_bf52e82786ca4d93a5751cc6b0e3833c/FeatureServer/0/query"

# Parameters for the API request
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "json",
    "token": None  # Token will be added later
}

# Perform login to get token
login_url = "https://www.arcgis.com/sharing/rest/generateToken"
login_data = {
    "f": "json",
    "username": username,
    "password": password,
    "referer": "https://survey123.arcgis.com",
    "expiration": 60,
    "client": "referer",
    "grant_type": "password"
}

login_response = requests.post(login_url, data=login_data)

# Check if login was successful
if login_response.status_code == 200:
    # Get the token from the response
    token = login_response.json()["token"]
    # Add token to API request parameters
    params["token"] = token

    # Send request to fetch data
    response = requests.get(api_url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extracting and printing data
        for feature in data.get("features", []):
            attributes = feature.get("attributes", {})
            print(attributes)
    else:
        print("Failed to retrieve data from API. Status code:", response.status_code)
else:
    print("Login failed. Status code:", login_response.status_code)