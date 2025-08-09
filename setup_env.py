#!/usr/bin/env python3
"""
Setup script to help users migrate from language.json to environment variables.
This script reads the original language.json file and creates a .env file.
"""

import json
import os
from pathlib import Path

def migrate_from_language_json():
    """
    Migrate credentials from config/language.json to .env file.
    """
    language_json_path = Path("config/language.json")
    env_path = Path(".env")
    
    if not language_json_path.exists():
        print("❌ config/language.json not found.")
        print("Please make sure you have the original language.json file.")
        return False
    
    if env_path.exists():
        print("⚠️  .env file already exists.")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            return False
    
    try:
        # Read the language.json file
        with open(language_json_path, 'r') as f:
            credentials = json.load(f)
        
        # Create .env content
        env_content = f"""# Google Cloud Service Account Credentials
# Generated from config/language.json
GOOGLE_CLOUD_TYPE={credentials.get('type', 'service_account')}
GOOGLE_CLOUD_PROJECT_ID={credentials.get('project_id', '')}
GOOGLE_CLOUD_PRIVATE_KEY_ID={credentials.get('private_key_id', '')}
GOOGLE_CLOUD_PRIVATE_KEY="{credentials.get('private_key', '')}"
GOOGLE_CLOUD_CLIENT_EMAIL={credentials.get('client_email', '')}
GOOGLE_CLOUD_CLIENT_ID={credentials.get('client_id', '')}
GOOGLE_CLOUD_AUTH_URI={credentials.get('auth_uri', '')}
GOOGLE_CLOUD_TOKEN_URI={credentials.get('token_uri', '')}
        GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL={credentials.get('auth_provider_x509_cert_url', '')}
        GOOGLE_CLOUD_CLIENT_X509_CERT_URL={credentials.get('client_x509_cert_url', '')}
"""
        
        # Write .env file
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ Successfully created .env file from config/language.json")
        print("🔒 The original config/language.json file can now be safely deleted.")
        
        # Ask if user wants to delete the original file
        response = input("Do you want to delete the original config/language.json file? (y/N): ")
        if response.lower() == 'y':
            language_json_path.unlink()
            print("🗑️  Deleted config/language.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Environment Setup Script")
    print("=" * 40)
    print("This script will help you migrate from config/language.json to .env file.")
    print()
    
    success = migrate_from_language_json()
    
    if success:
        print()
        print("🎉 Setup complete!")
        print("You can now safely commit your code to GitHub.")
        print("The .env file is already in .gitignore and won't be committed.")
    else:
        print()
        print("❌ Setup failed. Please check the error messages above.")
