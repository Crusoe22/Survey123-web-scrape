# Survey123-web-scrape

 Survey123 Fuel Consumption Data Fetcher

This Python script retrieves fuel consumption data from an ArcGIS online survey using the Survey123 API and saves it to an Excel file for further analysis.

## Prerequisites

- Python 3.x
- `requests`
- `openpyxl`
- `pandas`

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repository
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Modify the script with your ArcGIS online username and password:

    ```python
    username = "Your_ArcGIS_Username"
    password = "Your_ArcGIS_Password"
    ```

5. Run the script:

    ```bash
    python main.py
    ```

## Functions

### 1. `grab_data(excel_sheet)`

- Fetches data from the ArcGIS online survey using the Survey123 API.
- Saves the data to an Excel file.

### 2. `format_excel(excel_sheet)`

- Formats the Excel file, renames columns, and drops unnecessary columns.

### 3. `update_width(excel_sheet)`

- Updates the column width of the Excel file for better readability.

### 4. `remove_rows_by_date(file_path, sheet_name, date_threshold)`

- Removes rows from the Excel file based on a specified date threshold.

## Example

```python
excel_sheet = "Survey123-FuelConsumption.xlsx"

grab_data(excel_sheet)
format_excel(excel_sheet)
update_width(excel_sheet)