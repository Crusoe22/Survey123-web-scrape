import requests
from openpyxl import Workbook
from datetime import datetime
import pandas as pd



def grab_data():
    
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
            # Create a new workbook
            wb = Workbook()
            # Get the active worksheet
            ws = wb.active

            # Add headers to the worksheet
            data = response.json()
            headers = data["fields"]
            header_names = [header["name"] for header in headers]
            ws.append(header_names)

            # Extract and write data to the worksheet
            for feature in data.get("features", []):
                attributes = feature.get("attributes", {})
                row_data = []
                for header_name in header_names:
                    value = attributes.get(header_name, "")
                    # Convert timestamp to readable format if it's a date field
                    if header_name.endswith("EditDate") and isinstance(value, int):
                        value = datetime.fromtimestamp(value / 1000).strftime("%Y-%m-%d %H:%M:%S")
                    row_data.append(value)
                ws.append(row_data)

            # Save workbook to Excel file
            file_path = r"C:\Users\Nolan\Documents\ExcelSheets\Survey123-FuelConsumption.xlsx"
            wb.save(file_path)
            print("Data has been written to", file_path)
        else:
            print("Failed to retrieve data from API. Status code:", response.status_code)
    else:
        print("Login failed. Status code:", login_response.status_code)

def format_excel():
    
    df = pd.read_excel(r"C:\Users\Nolan\Documents\ExcelSheets\Survey123-FuelConsumption.xlsx")

    df.rename(columns={'objectid': 'ObjectID', 'EditDate': 'Edit Date', 'fuel_type': 'Fuel Type', 'name': 'Name', 'vehicle_number': 'Vehicle Number',
                        'gallons_used': 'Gallons Used', 'odometer_reading': 'Odometer Reading', 'vehicle_n_other': 'Vehicle Other'}, inplace=True)
    
    df.drop(columns=["globalid", "CreationDate", "Creator", "Editor"], inplace=True)

    df.to_excel(r"C:\Users\Nolan\Documents\ExcelSheets\Survey123-FuelConsumption.xlsx", index=False,header=True)

grab_data()
format_excel()