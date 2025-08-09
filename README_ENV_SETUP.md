# Environment Setup Guide

This guide explains how to set up environment variables for the Audio Captioning API.

## Google Cloud Credentials Setup

### 1. Create a .env file

Copy the example environment file:

```bash
cp env.example .env
```

### 2. Fill in your Google Cloud credentials

Edit the `.env` file and replace the placeholder values with your actual Google Cloud service account credentials:

```env
GOOGLE_CLOUD_TYPE=service_account
GOOGLE_CLOUD_PROJECT_ID=your-actual-project-id
GOOGLE_CLOUD_PRIVATE_KEY_ID=your-actual-private-key-id
GOOGLE_CLOUD_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour actual private key here\n-----END PRIVATE KEY-----\n"
GOOGLE_CLOUD_CLIENT_EMAIL=your-actual-service-account@your-project.iam.gserviceaccount.com
GOOGLE_CLOUD_CLIENT_ID=your-actual-client-id
GOOGLE_CLOUD_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_CLOUD_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLOUD_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
GOOGLE_CLOUD_UNIVERSE_DOMAIN=googleapis.com
```

### 3. How to get Google Cloud credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Speech-to-Text API
4. Go to "IAM & Admin" > "Service Accounts"
5. Create a new service account or select an existing one
6. Create a new key (JSON format)
7. Download the JSON file and extract the values to your `.env` file

### 4. Security Notes

- **NEVER commit your `.env` file to version control**
- The `.env` file is already in `.gitignore`
- The original `config/language.json` file has been moved to environment variables
- Credentials are automatically generated in the `credentials/` directory when the app starts

### 5. Running the application

Once you have set up your `.env` file, you can run the application:

```bash
cd backend
uvicorn main:app --reload
```

The application will automatically:

1. Load environment variables from `.env`
2. Create the credentials file in `credentials/google_credentials.json`
3. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### 6. Troubleshooting

If you see warnings about missing credentials:

- Check that your `.env` file exists and contains all required variables
- Verify that your Google Cloud project has the Speech-to-Text API enabled
- Ensure your service account has the necessary permissions
