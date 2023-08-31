import requests, os
import json
from dotenv import load_dotenv

# save list of errors in a dictionary
with open('values.json', 'r') as json_file:
    error_list = json.load(json_file)

#  WAVE api key
load_dotenv()
api_key = os.getenv("API_KEY")
url = os.getenv("URL")

# get data from WAVE api in json format

def pretty_print(url):

    # store general error
    errors_array = []

    # store contrast errors
    contrast_errors_array = []

    # store other alerts
    alerts_array = []
    
    response = requests.get(f'https://wave.webaim.org/api/request?key={api_key}&reporttype=2&url={url}')
    if response.ok:
        data = response.json()
        
        # credits remaining
        print("Credits Remaining:")
        print(data['statistics']['creditsremaining'])

        # STORE GENERAL ERRORS
        errors = data["categories"]["error"]["items"]
        for type, item in errors.items():
            error_item = {
                "id": error_list[item["id"]],
                "count": item["count"]
            }
            errors_array.append(error_item)

        # STORE CONTRAST ERRORS
        contrast_errors = data["categories"]["contrast"]["items"]
        for type, item in contrast_errors.items():
            error_item = {
                "id": error_list[item["id"]],
                "count": item["count"]
            }
            contrast_errors_array.append(error_item)

        # STORE ALERTS
        alerts = data["categories"]["alert"]["items"]
        for type, item in alerts.items():
            error_item = {
                "id": error_list[item["id"]],
                "count": item["count"]
            }
            alerts_array.append(error_item)

    return errors_array, contrast_errors_array, alerts_array