# Environment Variables Guide

This document explains the environment variables used in the Audio Captioning API.

## 🔑 Required Environment Variables

### Google Cloud Service Account Credentials

These variables are required for Google Cloud Speech-to-Text and Storage services:

```env
# Service account type (always "service_account")
GOOGLE_CLOUD_TYPE=service_account

# Your Google Cloud project ID
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# Private key details from your service account JSON
GOOGLE_CLOUD_PRIVATE_KEY_ID=your-private-key-id
GOOGLE_CLOUD_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"

# Service account email
GOOGLE_CLOUD_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com

# Client ID from service account
GOOGLE_CLOUD_CLIENT_ID=your-client-id

# OAuth endpoints (these are standard Google endpoints)
GOOGLE_CLOUD_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_CLOUD_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLOUD_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
```

## 🚫 Removed Variables

The following variables were removed as they are not needed:

- `GOOGLE_CLOUD_UNIVERSE_DOMAIN` - Not used by Speech-to-Text or Storage
- `GOOGLE_APPLICATION_CREDENTIALS` - We use environment variables directly instead of file paths

## 📋 How to Get These Values

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select your project**
3. **Go to IAM & Admin → Service Accounts**
4. **Create a new service account or select existing one**
5. **Create a new key (JSON format)**
6. **Download the JSON file**
7. **Copy values from the JSON to your `.env` file**

## 🔧 Setup Process

1. **Copy the template:**

   ```bash
   cp env.example .env
   ```

2. **Edit `.env` with your actual values**

3. **Test the setup:**
   ```bash
   python setup_env.py
   ```

## 🚀 Deployment

For Render deployment, add these environment variables in the Render dashboard:

1. Go to your service settings
2. Add each variable from your `.env` file
3. Make sure to properly escape the private key with quotes

## 🔒 Security Notes

- ✅ Never commit `.env` files to version control
- ✅ Use different service accounts for development and production
- ✅ Rotate service account keys regularly
- ✅ Grant minimum required permissions to service accounts

## 🐛 Troubleshooting

**"Credentials not found" error:**

- Check all required variables are set
- Verify private key format (should be in quotes with `\n` for newlines)
- Ensure service account has proper permissions

**"Permission denied" error:**

- Verify service account has Speech-to-Text and Storage permissions
- Check project ID is correct
- Ensure billing is enabled for the project
