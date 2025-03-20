import json
import os
import logging
import requests
import base64

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_URL = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
HEADERS = {"X-Siemens-Auth": "test"}

def lambda_handler(event, context):
    try:
        # Fetch environment variables
        subnet_id = os.getenv("SUBNET_ID")
        name = os.getenv("NAME", "Mayur Jadhav")
        email = os.getenv("EMAIL", "mr.jadhav1205@gmail.com")

        if not subnet_id:
            raise ValueError("Missing SUBNET_ID environment variable")

        # Construct API request payload
        payload = {
            "subnet_id": subnet_id,
            "name": name,
            "email": email
        }

        logger.info(f"Sending request to Siemens API: {payload}")

        # Send POST request
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

#        # Encode API response in Base64 for Jenkins logs
#        log_result = base64.b64encode(response.text.encode()).decode()
#
#        logger.info(f"API Response: {response.status_code} - {response.text}")
#
#        return {
#            "StatusCode": response.status_code,
#            "Body": response.text,
#            "LogResult": log_result  # Base64 encoded for Jenkins
#        }

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            "StatusCode": 500,
            "Body": json.dumps({"error": "Internal Server Error"}),
            "LogResult": base64.b64encode(str(e).encode()).decode()  # Encode error message in Base64
        }
