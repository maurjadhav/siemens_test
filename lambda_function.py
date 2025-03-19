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
            raise ValueError("Missing SUBNET_ID in environment variables")

        # Create request payload
        payload = {"subnet_id": subnet_id, "name": name, "email": email}

        # Send POST request
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        
        # Log API response
        logger.info(f"API Response: {response.text}")

        # Decode base64 LogResult (Bonus Requirement)
        log_result = base64.b64encode(response.text.encode()).decode()

        return {
            "statusCode": response.status_code,
            "body": response.text,
            "logResult": log_result  # Base64 encoded log output for Jenkins
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"error": "Internal Server Error"})}
