import json
import os
import logging
import requests
import base64

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# API details
API_URL = "https://bc1yy8dzsg.execute-api.eu-west-1.amazonaws.com/v1/data"
HEADERS = {"X-Siemens-Auth": "test"}

def lambda_handler(event, context):
    try:
        # Get environment variables
        subnet_id = os.getenv("SUBNET_ID")
        name = os.getenv("NAME", "Mayur Jadhav")
        email = os.getenv("EMAIL", "mr.jadhav1205@gmail.com")

        if not subnet_id:
            logger.error("Missing SUBNET_ID in environment variables")
            return {
                "statusCode": 400,  # Use 400 for client errors
                "body": json.dumps({"error": "Missing SUBNET_ID"}),
            }

        # Create request payload
        payload = {"subnet_id": subnet_id, "name": name, "email": email}

        # Send POST request
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "API request failed"}),
            }

        # Log API response
        logger.info(f"API Response: {response.text}")

        # Decode base64 LogResult (Bonus Requirement)
        log_result = base64.b64encode(response.text.encode()).decode()

        return {
            "statusCode": response.status_code,
            "body": response.text,
            "logResult": log_result,  # Base64 encoded log output for Jenkins
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
        }