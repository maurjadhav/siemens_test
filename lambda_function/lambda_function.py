import json
import os
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_URL = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
HEADERS = {"X-Siemens-Auth": "test"}

def lambda_handler(event, context):
    try:
        subnet_id = os.getenv("SUBNET_ID")
        name = os.getenv("NAME", "Mayur Jadhav")
        email = os.getenv("EMAIL", "mr.jadhav1205@gmail.com")

        if not subnet_id:
            raise ValueError("Missing SUBNET_ID")

        payload = {"subnet_id": subnet_id, "name": name, "email": email}
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        logger.info(f"API Response: {response.status_code} - {response.text}")

        return {"statusCode": response.status_code, "body": response.text}

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Server Error"})}