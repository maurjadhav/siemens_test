import os
import json
import requests

API_URL = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
HEADERS = {'X-Siemens-Auth': 'test'}

def lambda_handler(event, context):
    payload = {
        "subnet_id": os.getenv("SUBNET_ID"),
        "name": os.getenv("NAME"),
        "email": os.getenv("EMAIL")
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        return {
            "statusCode": response.status_code,
            "body": response.json()
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
