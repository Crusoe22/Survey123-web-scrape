import requests
from openpyxl import Workbook
from datetime import datetime
import pandas as pd
from datetime import date
import openpyxl


def grab_data(excel_sheet):
    
    # ArcGIS online username and password
    username = "Nolan_HUD"
    password = "nolanm1%HUD"

    # URL of the API endpoint to fetch data (Ctrl+Shift+I on webpage)
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
            file_path = excel_sheet
            wb.save(file_path)
            print("Data has been written to", file_path)
        else:
            print("Failed to retrieve data from API. Status code:", response.status_code)
    else:
        print("Login failed. Status code:", login_response.status_code)

def format_excel(excel_sheet):
    
    df = pd.read_excel(excel_sheet)

    df.rename(columns={'objectid': 'Object ID', 'EditDate': 'Edit Date', 'fuel_type': 'Fuel Type', 'name': 'Name', 'vehicle_number': 'Vehicle Number',
                        'gallons_used': 'Gallons Used', 'odometer_reading': 'Odometer Reading', 'vehicle_n_other': 'Vehicle Other'}, inplace=True)
    
    df.drop(columns=["globalid", "CreationDate", "Creator", "Editor"], inplace=True)

    df.to_excel(excel_sheet, index=False,header=True)

def remove_rows_by_date(file_path, sheet_name, date_threshold):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Convert "Edit Date" column to datetime if it's not already
    if df['Edit Date'].dtype != 'datetime64[ns]':
        df['Edit Date'] = pd.to_datetime(df['Edit Date'])

    # Filter rows where "EditDate" is greater than the threshold date
    df = df[df['Edit Date'] <= date_threshold]

    # Write the filtered DataFrame back to the Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def update_width(excel_sheet): 

    try:
        wb = openpyxl.load_workbook(excel_sheet) 
        # Get workbook active sheet   
        # from the active attribute.  
        ws = wb.active 
        
        # Set the width of all columns to 22
        for col in ws.columns:
            col_width = 22
            col[0].column_letter
            ws.column_dimensions[col[0].column_letter].width = col_width
            # Save the workbook

        wb.save(excel_sheet)

        print("Width updated successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':

    todays_date = date.today()
    current_month = todays_date.month

    excel_sheet = r"\\VSERVER22\ForEveryone\Nolan\Fuel-Consumption\Fuel-Consumption-Survey-Data.xlsx"

    grab_data(excel_sheet)
    format_excel(excel_sheet)
    update_width(excel_sheet)
    #remove_rows_by_date(r"C:\Users\Nolan\Documents\ExcelSheets\Survey123-FuelConsumption.xlsx", "Sheet1", pd.to_datetime(current_month))