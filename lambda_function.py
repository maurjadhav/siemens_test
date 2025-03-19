import json
import os
import logging
import base64
import requests

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Constants
API_URL = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
HEADERS = {'X-Siemens-Auth': 'test'}

def lambda_handler(event, context):
    """
    AWS Lambda function to invoke Siemens API from a private subnet.
    
    Returns:
        dict: API response with status code and body.
    """
    try:
        # Fetching environment variables from Terraform
        subnet_id = os.getenv("SUBNET_ID")
        name = os.getenv("NAME", "Mayur Jadhav")
        email = os.getenv("EMAIL", "mr.jadhav1205@gmail.com")

        if not subnet_id:
            raise ValueError("SUBNET_ID environment variable is missing")

        # Payload for API request
        payload = {
            "subnet_id": subnet_id,
            "name": name,
            "email": email
        }

        logger.info("Sending POST request to Siemens API...")
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        # Decode Base64 log output (for Jenkins)
        log_result = base64.b64encode(response.text.encode()).decode()

        # Return API response
        return {
            "statusCode": response.status_code,
            "body": response.text,
            "logResult": log_result  # Base64 encoded log output for Jenkins
        }

    except Exception as e:
        logger.error("Error: %s", str(e), exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
        }
