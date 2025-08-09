import os
import json
from pathlib import Path

def create_google_credentials():
    """
    Create Google Cloud credentials file from environment variables.
    This allows us to keep sensitive credentials out of the codebase.
    """
    credentials = {
        "type": os.getenv("GOOGLE_CLOUD_TYPE", "service_account"),
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_CLOUD_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_CLOUD_PRIVATE_KEY"),
        "client_email": os.getenv("GOOGLE_CLOUD_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLOUD_CLIENT_ID"),
        "auth_uri": os.getenv("GOOGLE_CLOUD_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_CLOUD_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("GOOGLE_CLOUD_CLIENT_X509_CERT_URL")
    }
    
    # Create credentials directory if it doesn't exist
    creds_dir = Path("credentials")
    creds_dir.mkdir(exist_ok=True)
    
    # Write credentials to file
    creds_file = creds_dir / "google_credentials.json"
    with open(creds_file, "w") as f:
        json.dump(credentials, f, indent=2)
    
    # Set environment variable for Google Cloud SDK
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(creds_file.absolute())
    
    return str(creds_file.absolute())

def check_credentials():
    """
    Check if all required Google Cloud credentials are available.
    """
    required_vars = [
        "GOOGLE_CLOUD_PROJECT_ID",
        "GOOGLE_CLOUD_PRIVATE_KEY_ID", 
        "GOOGLE_CLOUD_PRIVATE_KEY",
        "GOOGLE_CLOUD_CLIENT_EMAIL",
        "GOOGLE_CLOUD_CLIENT_ID"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True
