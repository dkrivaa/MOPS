import requests
import json


def annual_request(data, ):
    url = 'https://dannykrivaa.wixsite.com/mops/_functions/AnnualBudgetData'
    # Headers to specify the request format (JSON)
    headers = {
        'Content-Type': 'application/json'
    }
    # Sending the POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # Check if the request was successful
        if response.status_code == 200:
            print("Success! Data received:", response.json())
            return response.status_code
        else:
            print(f"Failed with status code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print(f"Error sending request: {e}")


def total_requests(data):
    url = 'https://dannykrivaa.wixsite.com/mops/_functions/AnnualBudgetData'
    data = data
