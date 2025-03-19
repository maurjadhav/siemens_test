import json
import os
import logging
import requests
from requests.exceptions import RequestException, Timeout

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_URL = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
HEADERS = {'X-Siemens-Auth': 'test'}

def send_request(payload):
    """Send a POST request with retry logic."""
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=5)
            response.raise_for_status()  # Raises HTTPError for 4xx and 5xx responses
            
            logger.info(f"API Response [{response.status_code}]: {response.text}")
            return response

        except (RequestException, Timeout) as err:
            logger.error(f"Attempt {attempt} failed: {err}")
            if attempt == max_retries:
                return None

def lambda_handler(event, context):
    try:
        # Fetch environment variables
        subnet_id = os.getenv("SUBNET_ID")
        name = os.getenv("NAME", "Mayur_Jadhav")
        email = os.getenv("EMAIL", "mr.jadhav1205@gmail.com")

        if not subnet_id:
            raise ValueError("Missing SUBNET_ID in environment variables")

        # Construct the payload
        payload = {
            "subnet_id": subnet_id,
            "name": name,
            "email": email
        }

        logger.info(f"Sending request to Siemens API with payload: {payload}")

        # Send the request with retry logic
        response = send_request(payload)

        if response:
            return {
                "statusCode": response.status_code,
                "body": response.text
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "API request failed after retries"})
            }

    except Exception as e:
        logger.error("Error: %s", str(e), exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }