import pandas as pd
import urllib.request
import io
import csv
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()
# EPC API details
token = os.getenv("EPC_API")
base_url = 'https://epc.opendatacommunities.org/api/v1/domestic/search'
headers = {
    'Accept': 'text/csv',
    'Authorization': f'Basic {token}'
}

# Function to get EPC data for a property
def get_latest_epc(postcode, house_number_or_name):
    print("Fetching")
    address = house_number_or_name.strip()

    params = {
        'postcode': postcode,
        'address': address,
        'size': 1,  # Fetch only the most recent EPC record
        'page': 1
    }
    encoded_params = urlencode(params)
    full_url = f"{base_url}?{encoded_params}"

    try:
        with urllib.request.urlopen(urllib.request.Request(full_url, headers=headers)) as response:
            response_body = response.read().decode()
            csv_data = list(csv.reader(io.StringIO(response_body)))
            headers1 = csv_data[0]  # First row as headers
            values = csv_data[1]   # Second row as values
            epc_df = pd.DataFrame([values], columns=headers1)
            return epc_df
    except Exception as e:
        print(f"Error fetching EPC data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
